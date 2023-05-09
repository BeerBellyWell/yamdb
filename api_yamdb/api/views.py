from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title
from users.models import CustomUser
from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import (AdminOnly, AuthorModeratorAdminOrReadOnly,
                          ReadOrAdminOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignUpSerializer,
                          TitleReadOnlySerializer, TitleSerializer,
                          TokenSerializer, UserSerializer)


class UserViewSet(ModelViewSet):
    """Получение списка пользователей,
    создание, удаление отдельных объектов админом."""
    http_method_names = ['get', 'post', 'patch', 'delete', ]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ['username']
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'put', 'patch'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        """Дополнительный маршрут 'me' для редактирования
        текущим пользователем своих данных."""
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)

            return Response(serializer.data)

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)

        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def send_confirmation_code(request):
    """Отправка письма с кодом подтверждения."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    user, _ = CustomUser.objects.get_or_create(
        username=username,
        email=email
    )
    user.confirmation_code = default_token_generator.make_token(user)
    user.save()
    send_mail(
        'Код подверждения', user.confirmation_code,
        settings.DEFAULT_FROM_EMAIL, (email, ), fail_silently=False
    )

    return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def get_jwt_token(request):
    """Сравнение кода подтверждения и получение токена."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        CustomUser,
        username=serializer.validated_data['username']
    )
    if default_token_generator.check_token(
        user, serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)

        return Response({'token': str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenreViewSet(ListCreateDestroyViewSet):
    """Получение списка жанров произведений.
    Создание, удаление отдельных объектов админом."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(ListCreateDestroyViewSet):
    """Получение списка категорий.
    Создание, удаление отдельных объектов админом."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(ModelViewSet):
    """Получение списка произведений.
    Создание, редактирование,
    удаление отдельной записи о произвед."""
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = [ReadOrAdminOnly, ]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):

            return TitleReadOnlySerializer

        return TitleSerializer


class ReviewViewSet(ModelViewSet):
    """Получение списка отзывов.
    Получение, создание, редактирование,
    удаление отдельного отзыва."""
    serializer_class = ReviewSerializer
    permission_classes = (AuthorModeratorAdminOrReadOnly,)

    def get_permissions(self):
        """Разрешение анонимам получать информацию
        об отдельном объекте."""
        if self.action == 'retrieve':

            return (AllowAny(),)

        return super().get_permissions()

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))

        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))

        return serializer.save(author=self.request.user,
                               title_id=title.id)


class CommentViewSet(ModelViewSet):
    """Получение списка комментариев к отзыву.
    Получение, создание, редактирование,
    удаление отдельного комментария."""
    serializer_class = CommentSerializer
    permission_classes = (AuthorModeratorAdminOrReadOnly,)

    def get_permissions(self):
        """Разрешение анонимам получать информацию
        об отдельном объекте."""
        if self.action == 'retrieve':

            return (AllowAny(),)

        return super().get_permissions()

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))

        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))

        return serializer.save(author=self.request.user,
                               review_id=review.id)
