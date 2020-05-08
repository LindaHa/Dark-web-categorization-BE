from django.test import TestCase
from api.tests.helpers import make_page, make_details_options, make_page_details
from api.utils.graph_helpers.details_helpers import get_page_details


class DetailsHelpersTestCase(TestCase):
    def test_get_page_details(self):
        """Returns the correct details"""
        detail_options = make_details_options()
        url = 'url.onion'
        page = make_page(url)
        expected = make_page_details(page)

        actual = get_page_details(page, detail_options, {})

        self.assertEqual(len(expected.links), len(actual.links))
        self.assertEqual(expected.title, actual.title)
        self.assertEqual(expected.url, actual.url)
        self.assertEqual(expected.content, actual.content)
        self.assertEqual(expected.category, actual.category)

