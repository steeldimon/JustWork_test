import importlib

from celery import shared_task


# @shared_task
def async_counter_increase(object_name, instance_id):
    # TODO: Сейчас есть только один route для сelery с concurency 1 для того, чтобы counter увеличивался атомарно
    #       В Продакшен нужно сделать для counter одлеьный celery route, для других задач можно будет использовать
    #       необходимы для нее настройки
    api_app_models = importlib.import_module("api_app.models")
    model = getattr(api_app_models, object_name)
    instance = model.objects.get(pk=instance_id)
    instance.counter += 1
    instance.save()

# TODO: Также можно сделать отдельную задачу, которая будет выполнять любое сохранение в БД через Celery
