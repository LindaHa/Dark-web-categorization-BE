from typing import List

from django.test import TestCase

from api.models import Page
from api.tests.helpers import make_group, make_meta_group, make_multiple_models, make_page
from api.utils.convertors import convert_groups_to_meta_groups, get_first_members, get_number_of_domains


class ConvertorsTestCase(TestCase):
    def test_convert_groups_to_meta_groups(self):
        """Groups are correctly converted to MetaGroups"""
        group_id_one = '0.2'
        group_one = make_group(group_id_one)
        m_group_one = make_meta_group(group_id_one)
        expected = [m_group_one]

        actual = convert_groups_to_meta_groups([group_one])

        self.assertEqual(len(expected), len(actual))
        self.assertEqual(expected[0].members_count, actual[0].members_count)
        self.assertEqual(expected[0].id, actual[0].id)
        self.assertEqual(len(expected[0].first_members), len(actual[0].first_members))

    def test_get_first_members(self):
        """Gets the correct number of first members"""
        number_of_first_members = 30
        members: List[Page] = make_multiple_models(40, '2.0', make_page)
        expected = number_of_first_members

        actual = get_first_members({m.url: m for m in members})

        self.assertEqual(expected, len(actual))

    def test_get_number_of_domains(self):
        """Gets the correct number of domains"""
        members: List[Page] = make_multiple_models(3, 'one.onion', make_page)
        expected = 3

        actual = get_number_of_domains({m.url: m for m in members})

        self.assertEqual(expected, actual)
