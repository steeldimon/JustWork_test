from django.contrib import admin

from pages_app.utils import snake_case_to_camel_case
from .import models


class ContentTabularInline(admin.TabularInline):
    extra = 1
    exclude = ['counter']
    search_fields = ['title']
    parent = models.Page

    @classmethod
    def get_inlines_list(cls):
        related_content = [attr for attr in dir(cls.parent) if 'content_' in attr]
        related_models = []

        for content in related_content:
            model = getattr(cls.parent, content).field.model
            related_models.append(type(snake_case_to_camel_case(f"{content}_{cls.__name__}"), (cls,), {"model": model}))
        return related_models


class PageAdmin(admin.ModelAdmin):
    exclude = ['videos', 'audios', 'texts']
    search_fields = ['title']
    inlines = ContentTabularInline.get_inlines_list()

    class Meta:
        models = models.Page


admin.site.register(models.Page, PageAdmin)


# TODO: Если нужна загрузка ручная таблица можно использовать ручную загрузку в админку конет таблица
#       admin.site.register(models.Video)
#       admin.site.register(models.Audio)
#       admin.site.register(models.Text)

# TODO: Если нужна динамическая загрузка можно использовать следующий код:
#       from django.apps import apps
#       app = apps.get_app_config('api_app')
#       for model_name, model in app.models.items():
#           admin.site.register(model)
