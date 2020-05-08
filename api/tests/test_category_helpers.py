from typing import List

from django.test import TestCase

from api.models import Page, Category
from api.tests.helpers import make_multiple_models, make_page
from api.utils.graph_helpers.category_helpers import create_categories_for_nodes


class CategoryHelpersTestCase(TestCase):
    def test_create_categories_for_nodes(self):
        """Creates categories with correct occurrences for group members"""
        members: List[Page] = make_multiple_models(3, 'one.onion', make_page)
        expected = [Category(name='Social', occurrence=3)]

        actual = create_categories_for_nodes(members)

        self.assertEqual(len(expected), len(actual))
        self.assertEqual(expected[0].name, actual[0].name)
        self.assertEqual(expected[0].occurrence, actual[0].occurrence)
