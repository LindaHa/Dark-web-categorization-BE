from django.test import TestCase

from api.models import Link, Category
from api.tests.helpers import make_custom_page, make_custom_group
from api.utils.graph_helpers.graph_helpers import get_edges, get_linked_groups_from_ids


class GraphHelpersTestCase(TestCase):
    def test_get_edges(self):
        """Gets edge source and destination pairs"""
        page_aliases = {
            0: [0, 1, 2, 3],
            1: [0, 3],
            2: [2],
            3: []
        }
        expected = [
            (0, 0), (0, 1), (0, 2), (0, 3),
            (1, 0), (1, 3),
            (2, 2),
        ]
        actual = get_edges(page_aliases)

        self.assertEqual(expected, actual)

    def test_get_linked_groups_from_ids(self):
        """Returns groups with links pages"""
        url_zero = 'zero.onion'
        url_one = 'one.onion'
        url_two = 'two.onion'
        url_three = 'three.onion'
        links_zero = [url_zero, url_one, url_two, url_three]
        links_one = [url_zero, url_three]
        links_two = [url_two]
        links_three = []
        page_one = make_custom_page(url=url_one, links=links_one)
        page_zero = make_custom_page(url=url_zero, links=links_zero)
        page_two = make_custom_page(url=url_two, links=links_two)
        page_three = make_custom_page(url=url_three, links=links_three)
        pages = {url_zero: page_zero, url_one: page_one, url_two: page_two, url_three: page_three}
        group_id_one = 1
        group_id_two = 2
        partition = {url_zero: group_id_one, url_one: group_id_one, url_two: group_id_two, url_three: group_id_one}
        parent_group_id = '0.2'
        expected = [
            make_custom_group(
                group_id=parent_group_id + '.' + str(group_id_one),
                links=[Link(link='0.2.2', name='')],
                categories=[Category(name='Social', occurrence=3)],
                pages={url_zero: page_zero, url_one: page_one, url_three: page_three}
            ),
            make_custom_group(
                group_id=parent_group_id + '.' + str(group_id_two),
                links=[],
                categories=[Category(name='Social', occurrence=1)],
                pages={url_two: page_two}
            )]

        actual = get_linked_groups_from_ids(pages, partition, parent_group_id)

        self.assertEqual(len(expected), len(actual))
        self.assertEqual(expected[0].id, actual[0].id)
        self.assertEqual(expected[0].categories[0].name, actual[0].categories[0].name)
        self.assertEqual(expected[0].categories[0].occurrence, actual[0].categories[0].occurrence)
        self.assertEqual(len(expected[0].links), len(actual[0].links))
        self.assertEqual(len(expected[1].members), len(actual[1].members))
        self.assertEqual(expected[1].id, actual[1].id)
        self.assertEqual(expected[1].categories[0].name, actual[1].categories[0].name)
        self.assertEqual(expected[1].categories[0].occurrence, actual[1].categories[0].occurrence)
        self.assertEqual(len(expected[1].links), len(actual[1].links))
        self.assertEqual(len(expected[1].members), len(actual[1].members))
