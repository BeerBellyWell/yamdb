from django.contrib import admin

from reviews.models import (Title, Category, Genre, GenreTitle,
                            Review, Comment)
from users.models import CustomUser


class GenreTitleInline(admin.TabularInline):
    model = GenreTitle
    extra = 1


class TitleAdmin(admin.ModelAdmin):
    inlines = [GenreTitleInline]
    list_display = ('id', 'description', 'name', 'year', 'category', )

    def get_genres(self, obj):
        return '\n'.join([g.genre for g in obj.genre.all()])


class GenreAdmin(admin.ModelAdmin):
    inlines = [GenreTitleInline]
    list_display = ('id', 'name', 'slug')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(GenreTitle)
admin.site.register(CustomUser)
admin.site.register(Review)
admin.site.register(Comment)
