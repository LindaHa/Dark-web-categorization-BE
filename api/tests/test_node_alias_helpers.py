from django.test import TestCase

from api.tests.helpers import make_custom_page
from api.utils.graph_helpers.node_alias_helpers import create_hash_tables, get_node_aliases, \
    get_original_node_key_group_pairs

url_zero = 'zero.onion'
url_one = 'one.onion'
url_two = 'two.onion'
url_three = 'three.onion'
links_zero = [url_zero, url_one, url_two, url_three]
links_one = [url_zero, url_three]
links_two = [url_two]
links_three = []
page_zero = make_custom_page(url=url_zero, links=links_zero)
page_one = make_custom_page(url=url_one, links=links_one)
page_two = make_custom_page(url=url_two, links=links_two)
page_three = make_custom_page(url=url_three, links=links_three)
pages = {url_zero: page_zero, url_one: page_one, url_two: page_two, url_three: page_three}


class NodeAliasHelpersTestCase(TestCase):
    def test_create_hash_tables(self):
        """Returns the partition of pages by category"""
        table_to_alias = {
            url_zero: 0,
            url_one: 1,
            url_two: 2,
            url_three: 3,
        }
        table_to_original = {value: key for key, value in table_to_alias.items()}
        expected = (table_to_alias, table_to_original)

        actual = create_hash_tables(pages)

        self.assertEqual(len(expected), len(actual))
        self.assertDictEqual(expected[0], actual[0])
        self.assertDictEqual(expected[1], actual[1])

    def test_get_node_aliases(self):
        """Returns the pages and their links as aliases"""
        table_to_alias = {
            url_zero: 0,
            url_one: 1,
            url_two: 2,
            url_three: 3,
        }
        expected = {
            0: [0, 1, 2, 3],
            1: [0, 3],
            2: [2],
            3: []
        }

        actual = get_node_aliases(pages, table_to_alias)

        self.assertDictEqual(expected, actual)

    def test_get_original_node_key_group_pairs(self):
        """Returns the original page ids and their assigned group id"""
        table_to_original = {
            0: url_zero,
            1: url_one,
            2: url_two,
            3: url_three,
        }
        partition = {
            0: 0,
            1: 0,
            2: 1,
            3: 0,
        }

        expected = {
            url_zero: 0,
            url_one: 0,
            url_two: 1,
            url_three: 0,
        }

        actual = get_original_node_key_group_pairs(partition=partition, table_to_original=table_to_original)

        self.assertDictEqual(expected, actual)
