from django.db import models

from api_app.tasks import async_counter_increase


# TODO: Для простого добавления контента без перезапуска сервера можно также использовать таблицу со списком типов
#  контента Таблицу с полями по типу данных, или полем JSON, и связями через нее и Page, тогда создание нового вида
#  контента можно будет выполнять созданием новой записи в БД


class PageAndContentMixin(models.Model):
    """
    Абстрактный класс с полями, общими для страницы и контента, если нужно расширить список доступных полей,
    Необходимо добавить их сюда и сделать миграцию
    """
    title = models.CharField(max_length=255, verbose_name='Заголовок')

    class Meta:
        abstract = True


class ContentMixin(models.Model):
    """
    Абстрактный класс с полями, для всего конетнта, при создании общих специфических полей для всех видов контента,
    Необходимо добавить их сюда и сделать миграцию
    Связь со страницей в данном случае генерируется динамически и имеет префикс "content_"
    """
    counter = models.PositiveIntegerField(verbose_name='Счетчик просмотров', default=0)
    sort_field = models.IntegerField(verbose_name='Порядковый номер', default=0)
    page = models.ForeignKey('Page', related_name='content_%(class)ss', on_delete=models.CASCADE)

    def increase_counter(self):
        async_counter_increase(object_name=self._meta.object_name, instance_id=self.pk)
        # async_counter_increase.delay(object_name=self._meta.object_name, instance_id=self.pk)

    class Meta:
        abstract = True


class Page(PageAndContentMixin):

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'


class Video(PageAndContentMixin, ContentMixin):
    url_to_video = models.URLField(verbose_name='Ссылка на видеофайл')
    url_to_subtitle = models.URLField(verbose_name='Ссылка на файл субтитров', blank=True, default='')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'


class Audio(PageAndContentMixin, ContentMixin):
    bitrate = models.FloatField(verbose_name='Битрейт', help_text='Битрейт в количестве бит в секунду')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Аудио'
        verbose_name_plural = 'Аудио'


class Text(PageAndContentMixin, ContentMixin):
    text = models.TextField(verbose_name='Текстовое поле', help_text='Поле для хранения текста произвольной длинны')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Текст'
        verbose_name_plural = 'Текст'
