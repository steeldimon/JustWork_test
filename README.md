# Тестовое задание JustWork
Полный текст задания можно посмотреть в файле "Тестовое задание Django.pdf" в корне

## Запуск прилоежния
Для запуска Тестов нужно выполнить в корневой директории

`docker-compose run autotests`

Для запуска Django runserver

`docker-compose run runserver`
Сам сервер будет доступен только внутри контейнера, для работы проброса портов неоходимо выполнить: 
`docker-compose run --service-ports runserver`

Сервис:

````
    pages_app:
        image: pages_app:latest
        build: .
        container_name: pages_app_dc
        restart: always
        ports:
            - 0.0.0.0:8000:8000
        env_file: .env
        links:
            - database:dbserver
        depends_on:
            - database
            - rabbit
            - worker
        volumes:
            - ./pages_app:/home/pages_app/pages_app:rw
````

Отвечает за wsgi gunicorn версию проекта с выполенением только миграций для production (закоментировано)

## Пути проекта

По умолчанию корень ведет редирект в /admin/

### Django admin

Путь /admin/

Пароль для superuser создается автоматически из fixtures для тестового сервреа: admin:admin

В Админке можно добавлять страницы и контент к ним, для этого в разделе **APP_API** добавляем новую страницу

Поиск осуществляется по полю title

Связанный контент автоматически выводится в виде inline блоков

Счетчик просмотров добавляется только при выводе в api

Для всех Inline блоков есть поле sort_field, сортировка всего контента осуществляется по этому полю


### Api

Путь /api/

По умолчанию создан только один Readonly путь внутри /api/ - page `/api/page/`

Он отображает Title созданных страниц и url для подробного вида страницы с отсортированным контентом

В Детальном виде контента ID = 1 `/api/page/1/` отображается блок `content` в виде списка смешанного контента, 
отсортированного по полю **sort_field**

### Добавление нового типа контента

Для создания нового типа контента, необходимо создать для него модель со всеми специфичным для него полями, а также 
выполнить наследования от `PageAndContentMixin` для добавления общий полей **Страницы** и **Контента**, 
а также `ContentMixin` для создания общий для всего контента полей и методов, таких как поле сортировки, 
поля количества просмотров, связи со страницей и асинхронной функции увеличения счетчика просмотров, создать новую 
миграцию `python manage.py makemigrations api_app`

Далее имя обратной связи для таблицы `Page` создается автоматически с префиксом **content_**, по нему динамически 
добавляются все API и Admin.