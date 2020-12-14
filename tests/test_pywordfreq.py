import unittest

import pywordfreq


class WordFrequencyTestCase(
    unittest.TestCase,
):
    def test_full_frequency(
        self,
    ):
        self.assertEqual(
            first=pywordfreq.WordFrequency.full_frequency('asdkjflasd'),
            second=0,
        )
        self.assertEqual(
            first=pywordfreq.WordFrequency.full_frequency('a'),
            second=0,
        )
        self.assertEqual(
            first=pywordfreq.WordFrequency.full_frequency('the'),
            second=151983633,
        )
        self.assertEqual(
            first=pywordfreq.WordFrequency.full_frequency('The'),
            second=151983633,
        )
        self.assertEqual(
            first=pywordfreq.WordFrequency.full_frequency('cuarny'),
            second=20,
        )
        self.assertEqual(
            first=pywordfreq.WordFrequency.full_frequency('Cuarny'),
            second=20,
        )

    def test_partial_frequency(
        self,
    ):
        self.assertEqual(
            first=pywordfreq.WordFrequency.partial_frequency('asdkjflasd'),
            second=0,
        )
        self.assertEqual(
            first=pywordfreq.WordFrequency.partial_frequency('a'),
            second=712062214,
        )
        self.assertEqual(
            first=pywordfreq.WordFrequency.partial_frequency('the'),
            second=29454783,
        )
        self.assertEqual(
            first=pywordfreq.WordFrequency.partial_frequency('The'),
            second=29454783,
        )
        self.assertEqual(
            first=pywordfreq.WordFrequency.partial_frequency('cuarny'),
            second=0,
        )
        self.assertEqual(
            first=pywordfreq.WordFrequency.partial_frequency('Cuarny'),
            second=0,
        )
