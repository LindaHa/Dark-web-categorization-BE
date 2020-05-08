from django.test import TestCase

from api.utils.graph_helpers.url_helpers import get_domain_from_url


class UrlHelpersTestCase(TestCase):
    def test_get_domain_from_url(self):
        """Returns the reversed partition correctly"""
        url_one = 'one.onion'
        url_two = 'two.onion.end'
        url_three = 'three.onion/end'

        self.assertEqual('one', get_domain_from_url(url_one))
        self.assertEqual('two', get_domain_from_url(url_two))
        self.assertEqual('three', get_domain_from_url(url_three))
