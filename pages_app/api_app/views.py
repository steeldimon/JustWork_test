from rest_framework import viewsets

from . import models, serializer


class PageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Page.objects.all()
    serializer_class = serializer.PageSerializer
    serializers = {
        # Сериализатор для детального вида страницы, с отображением related content
        'retrieve': serializer.PageDetailSerializer,
    }

    def get_serializer_class(self):
        # Добавляем возможность указать для разных action отдельный класс сериализатора, или использовать по умолчанию
        return self.serializers.get(self.action, self.serializer_class)
