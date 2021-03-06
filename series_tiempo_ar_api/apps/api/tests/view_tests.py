#! coding: utf-8
import json
import csv

from django.conf import settings
from django.http import JsonResponse
from django.test import TestCase, Client
from django.urls import reverse

SERIES_NAME = settings.TEST_SERIES_NAME.format('month')


class ViewTests(TestCase):

    client = Client()
    endpoint = reverse('api:series:series')

    @classmethod
    def setUpClass(cls):
        super(ViewTests, cls).setUpClass()

    def test_series_returs_json_by_default(self):
        response = self.client.get(self.endpoint, data={'ids': SERIES_NAME})
        self.assertTrue(response.json())

    def test_series_empty_args(self):
        response = json.loads(self.client.get(self.endpoint).content)

        self.assertTrue(response['errors'])

    def test_csv_ignore_case(self):
        response = self.client.get(self.endpoint,
                                   data={'ids': SERIES_NAME, 'format': 'csv'})
        response_upper = self.client.get(self.endpoint,
                                         data={'ids': SERIES_NAME, 'format': 'CSV'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, response_upper.content)

    def test_collapse_agg_ignore_case(self):
        response = self.client.get(self.endpoint,
                                   data={'ids': SERIES_NAME,
                                         'collapse_aggregation': 'sum'})
        response_upper = self.client.get(self.endpoint,
                                         data={'ids': SERIES_NAME,
                                               'collapse_aggregation': 'SUM'})

        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(response.content, response_upper.content)

    def test_rep_mode_ignore_case(self):
        response = self.client.get(self.endpoint,
                                   data={'ids': SERIES_NAME,
                                         'representation_mode': 'percent_change'})
        response_upper = self.client.get(self.endpoint,
                                         data={'ids': SERIES_NAME,
                                               'representation_mode': 'PERCENT_change'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, response_upper.content)

    def test_sort_ignore_case(self):
        response = self.client.get(self.endpoint,
                                   data={'ids': SERIES_NAME,
                                         'sort': 'desc'})
        response_upper = self.client.get(self.endpoint,
                                         data={'ids': SERIES_NAME,
                                               'sort': 'DESC'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, response_upper.content)

    def test_metadata_ignore_case(self):
        response = self.client.get(self.endpoint,
                                   data={'ids': SERIES_NAME,
                                         'metadata': 'none'})
        response_upper = self.client.get(self.endpoint,
                                         data={'ids': SERIES_NAME,
                                               'metadata': 'None'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, response_upper.content)

    def test_csv_delimiter(self):
        response = self.client.get(self.endpoint,
                                   data={'ids': SERIES_NAME, 'format': 'csv', 'sep': ';'})

        # CSV de sólo números, la única manera que haya ';' es que sea el delimiter
        self.assertIn(b';', response.content)

    def test_csv_decimal_char(self):
        decimal = ','
        response = self.client.get(self.endpoint,
                                   data={'ids': SERIES_NAME, 'format': 'csv', 'decimal': decimal})

        reader = csv.reader(str(response.content).splitlines())

        for line in reader:
            self.assertTrue(len(line), 2)

    def test_csv_decimal_and_delimiter(self):
        delim = ';'
        response = self.client.get(self.endpoint,
                                   data={'ids': SERIES_NAME, 'format': 'csv',
                                         'decimal': ',',
                                         'sep': delim})

        reader = csv.reader(str(response.content).splitlines(), delimiter=delim)

        for line in reader:
            self.assertTrue(len(line), 2)

    def test_start_over_limit_returns_400(self):
        response = self.client.get(self.endpoint,
                                   data={'ids': SERIES_NAME,
                                         'start': '999999'})

        self.assertEqual(response.status_code, 400)

    def test_start_of_max_offset_returns_200(self):
        # Max offset: start + limit == 10000
        response = self.client.get(self.endpoint,
                                   data={'ids': SERIES_NAME,
                                         'start': '9899',
                                         'limit': '100'})

        self.assertEqual(response.status_code, 200)
