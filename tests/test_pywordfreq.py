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
            second=335698206,
        )
        self.assertEqual(
            first=pywordfreq.WordFrequency.full_frequency('The'),
            second=335698206,
        )
        self.assertEqual(
            first=pywordfreq.WordFrequency.full_frequency('cuarny'),
            second=46,
        )
        self.assertEqual(
            first=pywordfreq.WordFrequency.full_frequency('Cuarny'),
            second=46,
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
            second=1650215434,
        )
        self.assertEqual(
            first=pywordfreq.WordFrequency.partial_frequency('the'),
            second=65945880,
        )
        self.assertEqual(
            first=pywordfreq.WordFrequency.partial_frequency('The'),
            second=65945880,
        )
        self.assertEqual(
            first=pywordfreq.WordFrequency.partial_frequency('cuarny'),
            second=0,
        )
        self.assertEqual(
            first=pywordfreq.WordFrequency.partial_frequency('Cuarny'),
            second=0,
        )
