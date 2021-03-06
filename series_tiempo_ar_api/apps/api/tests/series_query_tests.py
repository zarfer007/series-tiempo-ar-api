import json

import iso8601
from django.test import TestCase

from django_datajsonar.models import Field
from series_tiempo_ar_api.apps.api.query import constants
from series_tiempo_ar_api.apps.api.query.series_query import SeriesQuery
from series_tiempo_ar_api.apps.api.tests.helpers import get_series_id
from series_tiempo_ar_api.apps.management import meta_keys
from series_tiempo_ar_api.apps.metadata.models import SeriesUnits


class SeriesQueryTests(TestCase):
    single_series = get_series_id('month')

    def setUp(self):
        self.field = Field.objects.get(identifier=self.single_series)
        self.field_description = "Mi descripción"
        self.units = 'my_units'
        self.field.metadata = json.dumps({'description': self.field_description,
                                          'units': self.units})
        self.serie = SeriesQuery(self.field, constants.VALUE)

    def test_get_periodicity(self):
        periodicity = self.serie.periodicity()
        self.assertEqual(periodicity, 'month')

    def test_get_periodicity_reads_from_distribution_if_serie_has_none(self):
        self.field.enhanced_meta.all().delete()
        periodicity = SeriesQuery(self.field, constants.VALUE).periodicity()
        self.assertEqual(periodicity, 'month')

    def test_get_metadata_has_values_for_all_levels(self):
        meta = self.serie.get_metadata()

        self.assertIn('catalog', meta)
        self.assertIn('dataset', meta)
        self.assertIn('distribution', meta)
        self.assertIn('field', meta)

    def test_get_metadata_flatten_has_description_in_first_level(self):
        meta = self.serie.get_metadata(flat=True)
        self.assertIn('field_description', meta)
        self.assertNotIn('field', meta)

    def test_enhanced_meta_not_in_metadata_if_query_is_simple(self):
        meta = self.serie.get_metadata(simple=True)

        self.assertNotIn('available', meta['field'])

    def test_get_identifiers(self):
        ids = self.serie.get_identifiers()

        self.assertEqual(ids['id'], self.field.identifier)
        self.assertEqual(ids['distribution'], self.field.distribution.identifier)
        self.assertEqual(ids['dataset'], self.field.distribution.dataset.identifier)

    def test_get_title(self):
        title = self.serie.title()
        self.assertEqual(title, self.field.title)

    def test_get_description(self):
        description = self.serie.description()
        self.assertEqual(description, self.field_description)

    def test_get_description_no_description_set(self):
        self.field.metadata = json.dumps({})
        description = SeriesQuery(self.field, constants.VALUE).description()
        self.assertEqual(description, '')

    def test_get_start_date(self):
        start_date = meta_keys.get(self.field, meta_keys.INDEX_START)
        start_date = iso8601.parse_date(start_date)
        self.assertEqual(self.serie.start_date(), start_date.date())

    def test_get_start_date_none_if_not_set(self):
        self.field.enhanced_meta.all().delete()
        self.assertEqual(self.serie.start_date(), None)

    def test_metadata_is_percentage_default_rep_mode(self):
        meta = self.serie.get_metadata(simple=False)
        self.assertFalse(meta['field']['is_percentage'])

    def test_metadata_is_percentage_with_percentage_rep_mode(self):
        meta = SeriesQuery(self.field, constants.PCT_CHANGE).get_metadata(simple=False)
        self.assertTrue(meta['field']['is_percentage'])

    def test_metadata_is_percentage_with_flat_metadata(self):
        meta = SeriesQuery(self.field, constants.PCT_CHANGE).get_metadata(simple=False, flat=True)
        self.assertTrue(meta['field_is_percentage'])

    def test_metadata_is_not_percentage_with_flat_metadata(self):
        meta = self.serie.get_metadata(simple=False, flat=True)
        self.assertFalse(meta['field_is_percentage'])

    def test_metadata_rep_mode(self):
        rep_mode = self.serie.get_metadata()['field']['representation_mode']
        self.assertEqual(rep_mode, constants.VALUE)

    def test_metadata_rep_mode_flat(self):
        meta = self.serie.get_metadata(flat=True)
        self.assertEqual(meta['field_representation_mode'], constants.VALUE)

    def test_metadata_rep_mode_units_copy_of_units_if_value(self):
        meta = self.serie.get_metadata()
        self.assertEqual(meta['field']['units'], meta['field']['representation_mode_units'])

    def test_metadata_rep_mode_units_copy_of_units_if_value_flat(self):
        meta = self.serie.get_metadata(flat=True)
        self.assertEqual(meta['field_units'], meta['field_representation_mode_units'])

    def test_metadata_rep_mode_units_none_if_no_units_set(self):
        self.field.metadata = json.dumps({})
        meta = SeriesQuery(self.field, constants.VALUE).get_metadata()
        self.assertIsNone(meta['field']['representation_mode_units'])

    def test_metadata_rep_mode_units_for_percentage_rep_mode(self):
        meta = SeriesQuery(self.field, constants.PCT_CHANGE).get_metadata()
        self.assertEqual(constants.VERBOSE_REP_MODES[constants.PCT_CHANGE],
                         meta['field']['representation_mode_units'])

    def test_percentage_metadata_not_available_if_simple(self):
        simple_meta = self.serie.get_metadata()
        self.assertNotIn('is_percentage', simple_meta['field'])

    def test_percentage_metadata_not_available_if_simple_and_flat(self):
        simple_meta = self.serie.get_metadata(flat=True)
        self.assertNotIn('field_is_percentage', simple_meta)

    def test_percentage_metadata_is_false_if_no_series_units_model(self):
        meta = self.serie.get_metadata(simple=False, flat=False)
        self.assertFalse(meta['field']['is_percentage'])

    def test_percentage_metadata_false_if_no_units_field(self):
        self.field.metadata = '{}'
        self.field.save()
        meta = self.serie.get_metadata(simple=False, flat=False)
        self.assertFalse(meta['field']['is_percentage'])

    def test_percentage_metadata_false_if_units_arent_percentage(self):
        SeriesUnits.objects.create(name=self.units, percentage=False)

        meta = self.serie.get_metadata(simple=False, flat=False)
        self.assertFalse(meta['field']['is_percentage'])

    def test_percent_metadata_true_if_units_are_percentage(self):
        SeriesUnits.objects.create(name=self.units, percentage=True)

        meta = self.serie.get_metadata(simple=False, flat=False)
        self.assertTrue(meta['field']['is_percentage'])

    def test_percentage_metadata_if_units_are_percentage_and_rep_mode_is_percentage(self):
        SeriesUnits.objects.create(name=self.units, percentage=True)
        meta = SeriesQuery(self.field, constants.PCT_CHANGE).get_metadata(simple=False)
        self.assertTrue(meta['field']['is_percentage'])
