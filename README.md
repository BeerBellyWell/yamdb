# yamdb_final
yamdb_final
![workflow](https://github.com/beerbellywell/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

Проект представляет собой API для проекта Reviews.

# api_yamdb
>API Reviews - это API без лишних деталей. Благодаря этому его легко освоить и доработать. Через приложение уже можно читать информацию о разных произведениях,оставлять отзывы и комментарии к отзывам. Эту основу легко расширить, добавляя новые возможности.

#### Как запустить проект:

+ клонируем репозиторий `git clone`
`https://github.com/sabina-045/api_yamdb.git`
+ переходим в него `cd api_yamdb`
    + разворачиваем виртуальное окружение
    `python3 -m venv env` (Windows: `python -m venv env`)
    + активируем его
    `source env/bin/activate` (Windows: `source env/scripts/activate`)
    + устанавливаем зависимости из файла requirements.txt
    `pip install -r requirements.txt`
+ выполняем миграции
`python3 manage.py migrate` (Windows: `python manage.py migrate`)
+ запускаем проект
`python3 manage.py runserver` (Windows: `python manage.py runserver).
И вперед!

# Запускаем проект в докере
+ `docker-compose up -d --build` - собираем и запускаем контейнеры
+ Теперь в контейнере web нужно выполнить миграции, создать суперпользователя и собрать статику. Команды внутри контейнеров выполняют посредством подкоманды `docker-compose exec`. Выполните по очереди команды:
    + docker-compose exec web python manage.py migrate
    + docker-compose exec web python manage.py createsuperuser
    + docker-compose exec web python manage.py collectstatic --no-input
+ Теперь проект доступен по адресу http://localhost/.

# Инструкции и примеры

>Основные эндпойнты `/api/v1/`:

/titles/ - список произведений, создается админом.

/titles/{title_id}/ - информация об отдельном произведении.

/titles/{title_id}/reviews/ - список отзывов к отдельному произведению, создание отзыва.

/titles/{title_id}/reviews/comments/{comment_id}/ - информация об отдельном комментарии, изменение комментария автором или модератором.

</br>

>Для доступа к API необходимо получить токен:

Нужно выполнить POST-запрос http://127.0.0.1:8000/api/v1/auth/signup/ передав поля username и email.
На указанный адрес придет письмо с confirmation_code.
Нужно отправить POST-запрос http://127.0.0.1:8000/api/v1/auth/token/ передав поля username и confirmation_code.

Полученный токен передаем в заголовке Authorization: Bearer <токен>

</br>


> Команда создателей:
Яндекс Практикум, Максим Габчак, Андрей Чернышев, Сабина Гаджиева

> Вопросы и пожелания по адресу:
sabina_045@mail.ru