from django.test import TestCase
from api.utils.parsers import get_hits, get_scroll_id, get_total_in_db, taken_from_db, get_links_from_json, is_url_valid


class ParsersTestCase(TestCase):
    def test_get_hits(self):
        """Gets hits from the db response"""
        message = 'OK'
        json = {'hits': {'hits': message}}

        actual = get_hits(json)

        self.assertEqual(message, actual)

    def test_get_scroll_id(self):
        """Gets the scroll_id from the db response"""
        message = 'OK'
        json = {'_scroll_id': message}

        actual = get_scroll_id(json)

        self.assertEqual(message, actual)

    def test_get_total_in_db(self):
        """Gets the total response count from the db"""
        count = '100'
        json = {'hits': {'total': count}}

        actual = get_total_in_db(json)

        self.assertEqual(count, actual)

    def test_taken_from_db(self):
        """Gets the total shards count from the db response"""
        count = '100'
        json = {'shards': {'total': count}}

        actual = taken_from_db(json)

        self.assertEqual(count, actual)

    def test_get_links_from_json(self):
        """Gets pages from the db response"""

        json = [
            {'link': 'link.onion', 'link_name': 'link onion name'},
            {'link': 'link2.onion', 'link_name': 'second link onion name'},
        ]

        actual = get_links_from_json(json)
        # actual = 5
        self.assertEqual(2, len(actual))

    def test_is_url_valid(self):
        """Decides whether a url is valid"""
        url_valid_one = 'zero.onion'
        url_valid_two = 'zero.onion.valid'
        url_valid_three = 'zero.onion/valid'
        url_invalid_one = 'one.on'
        url_invalid_two = 'threeonion'

        self.assertTrue(is_url_valid(url_valid_one))
        self.assertTrue(is_url_valid(url_valid_two))
        self.assertTrue(is_url_valid(url_valid_three))
        self.assertFalse(is_url_valid(url_invalid_one))
        self.assertFalse(is_url_valid(url_invalid_two))


