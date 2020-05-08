from django.test import TestCase

from api.utils.graph_helpers.partition_helpers import reverse_partition


class PartitionHelpersTestCase(TestCase):
    def test_reverse_partition(self):
        """Returns the reversed partition correctly"""
        url_zero = 'zero.onion'
        url_one = 'one.onion'
        url_two = 'two.onion'
        url_three = 'three.onion'
        partition = {
            url_zero: 0,
            url_one: 0,
            url_two: 1,
            url_three: 0,
        }
        expected = {0: [url_zero, url_one, url_three], 1: [url_two]}

        actual = reverse_partition(partition)

        self.assertEqual(expected, actual)
