from django.test import TestCase

from api.tests.helpers import make_custom_page
from api.utils.graph_helpers.group_by_helpers import get_partition_by_category


class GraphHelpersTestCase(TestCase):
    def test_get_partition_by_category(self):
        """Returns the partition of pages by category"""
        url_zero = 'zero.onion'
        url_one = 'one.onion'
        url_two = 'two.onion'
        url_three = 'three.onion'
        cat_zero = 'Social'
        cat_one = 'Social'
        cat_two = 'Gambling'
        cat_three = 'Other'
        page_zero = make_custom_page(url=url_zero, category=cat_zero)
        page_one = make_custom_page(url=url_one, category=cat_one)
        page_two = make_custom_page(url=url_two, category=cat_two)
        page_three = make_custom_page(url=url_three, category=cat_three)
        pages = {url_zero: page_zero, url_one: page_one, url_two: page_two, url_three: page_three}
        expected = {
            url_zero: 8,
            url_one: 8,
            url_two: 1,
            url_three: 7,
        }

        actual = get_partition_by_category(pages)

        self.assertDictEqual(expected, actual)