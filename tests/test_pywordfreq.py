import unittest

import pywordfreq


class WordFrequencyTestCase(
    unittest.TestCase,
):
    def test_word_frequency(
        self,
    ):
        word_frequency_calculator = pywordfreq.WordFrequency()

        self.assertEqual(
            first=word_frequency_calculator.word_frequency('asdkjflasd'),
            second=0,
        )
        self.assertEqual(
            first=word_frequency_calculator.word_frequency('a'),
            second=0,
        )
        self.assertEqual(
            first=word_frequency_calculator.word_frequency('the'),
            second=151983633,
        )
        self.assertEqual(
            first=word_frequency_calculator.word_frequency('The'),
            second=151983633,
        )
        self.assertEqual(
            first=word_frequency_calculator.word_frequency('cuarny'),
            second=20,
        )
        self.assertEqual(
            first=word_frequency_calculator.word_frequency('Cuarny'),
            second=20,
        )

    def test_word_partial_frequency(
        self,
    ):
        word_frequency_calculator = pywordfreq.WordFrequency()

        self.assertEqual(
            first=word_frequency_calculator.word_partial_frequency('asdkjflasd'),
            second=0,
        )
        self.assertEqual(
            first=word_frequency_calculator.word_partial_frequency('a'),
            second=712062214,
        )
        self.assertEqual(
            first=word_frequency_calculator.word_partial_frequency('the'),
            second=29454783,
        )
        self.assertEqual(
            first=word_frequency_calculator.word_partial_frequency('The'),
            second=29454783,
        )
        self.assertEqual(
            first=word_frequency_calculator.word_partial_frequency('cuarny'),
            second=0,
        )
        self.assertEqual(
            first=word_frequency_calculator.word_partial_frequency('Cuarny'),
            second=0,
        )
