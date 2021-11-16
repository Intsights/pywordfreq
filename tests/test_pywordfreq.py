import unittest

import pywordfreq


class WordFrequencyTestCase(
    unittest.TestCase,
):
    def test_full_frequency(
        self,
    ):
        self.assertEqual(
            first=pywordfreq.full_frequency('asdkjflasd'),
            second=0,
        )
        self.assertEqual(
            first=pywordfreq.full_frequency('a'),
            second=0,
        )
        self.assertEqual(
            first=pywordfreq.full_frequency('the'),
            second=175007854,
        )
        self.assertEqual(
            first=pywordfreq.full_frequency('The'),
            second=175007854,
        )
        self.assertEqual(
            first=pywordfreq.full_frequency('belayneh'),
            second=25,
        )

    def test_partial_frequency(
        self,
    ):
        self.assertEqual(
            first=pywordfreq.partial_frequency('asdkjflasd'),
            second=0,
        )
        self.assertEqual(
            first=pywordfreq.partial_frequency('a'),
            second=858839773,
        )
        self.assertEqual(
            first=pywordfreq.partial_frequency('the'),
            second=34241408,
        )
        self.assertEqual(
            first=pywordfreq.partial_frequency('The'),
            second=34241408,
        )
        self.assertEqual(
            first=pywordfreq.partial_frequency('belayneh'),
            second=0,
        )
        self.assertEqual(
            first=pywordfreq.partial_frequency('belayneh'),
            second=0,
        )
