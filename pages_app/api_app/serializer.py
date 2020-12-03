from django.forms.models import model_to_dict
from rest_framework import serializers
from . import models


class PageDetailSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        """
        Переопределяем вывод related_name объектов страницы в отсортированный список по полу sort_field
        :param instance: Текущий сериализуемый объект
        :return: OrderedDict - данные для сериализации и отображения в API
        """
        # TODO: Добавить вывод verbose_name в к контенту, чтобы понимать его тип

        # Получаем изначальные данные
        data = super(PageDetailSerializer, self).to_representation(instance)

        # Получаем все поля с related_name начинающимся с прифекса "content_*"
        content_attrs = [attr for attr in dir(instance) if 'content_' in attr]
        mixed_content = []

        # Конвертируем queryset в list для и объекдиняем для всех типов контента в один список для дальнейшей сортировки
        for content in content_attrs:
            mixed_content += list(getattr(instance, content).all())
        for content in mixed_content:
            content.increase_counter()
        # Сортируем список по полю sort_field
        sorted_mixed_content = sorted(mixed_content, key=lambda i: i.sort_field)

        # Конвертируем объектыв в словарь для подготовки к сериализации данных
        sorted_mixed_content = [model_to_dict(content) for content in sorted_mixed_content]

        # Добавляем отсортированный раздел сontent к странице
        data.update([('content', sorted_mixed_content)])

        return data

    class Meta:
        model = models.Page
        exclude = ()


class PageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Page
        fields = ['url', 'title']
