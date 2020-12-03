from time import sleep
from django.test import TestCase, Client

client = Client()


class URLApiAppTest(TestCase):
    fixtures = ['init_data.json', ]

    def test_api_url(self):
        response = client.get('/api/')
        self.assertEquals(response.status_code, 200, 'Код страницы должен быть 200')

    def test_page_url(self):
        response = client.get('/api/page/')
        self.assertEquals(response.status_code, 200, 'Код страницы должен быть 200')

    def test_page_1_detail_url(self):
        response = client.get('/api/page/1/')
        self.assertEquals(response.status_code, 200, 'Код страницы должен быть 200')

    def test_page_1_detail_sorting(self):
        response = client.get('/api/page/1/', HTTP_ACCEPT='application/json')
        content_list = response.json().get('content')
        if content_list:
            last_sort_field = 0
            for content in content_list:
                sort_field = content.get('sort_field')
                if sort_field < last_sort_field:
                    self.fail('Не верный порядок')
                last_sort_field = sort_field
        self.assertEquals(response.status_code, 200, 'Код страницы должен быть 200')


class ContentCounterTest(TestCase):
    fixtures = ['init_data.json', ]

    def test_page_1_detail_content_counter_url(self):
        client.get('/api/page/1/')
        response = client.get('/api/page/1/')
        # sleep(1)

        content_list = response.json().get('content')

        if content_list:
            for content in content_list:
                if content.get('counter') != 1:
                    self.fail('Не верный счетчик')
        self.assertEquals(response.status_code, 200, 'Код страницы должен быть 200')
