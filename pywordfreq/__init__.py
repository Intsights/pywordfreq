import importlib.resources
import typing
import gzip

from . import pywordfreq


class WordFrequency:
    '''
    WordFrequency class is a wrapper against Wikipedia word frequency
    corpus. It includes two functions to check words/patterns against
    this dictionary. The library is written in Rust to achieve its
    performance and safety guarantees.
    '''
    engine: typing.Optional[pywordfreq.WordFrequency] = None

    @staticmethod
    def load_dictionary() -> None:
        if WordFrequency.engine is None:
            word_frequencies_compressed_data = importlib.resources.read_binary(
                package=__package__,
                resource='word_frequencies.gz',
            )
            word_frequencies_data = gzip.decompress(word_frequencies_compressed_data)
            WordFrequency.engine = pywordfreq.WordFrequency(
                word_frequencies_text=word_frequencies_data.decode(),
                min_frequency=50,
            )

    @staticmethod
    def full_frequency(
        word: str,
    ) -> int:
        '''
        Return the word frequency according to a Wikipedia corpus of
        occurrences of words.

        Args:
            word(str): a word to check against the dictionary

        Returns:
            int: the number of occurrences of the word

        Raises:
            None
        '''
        if WordFrequency.engine is None:
            WordFrequency.load_dictionary()

        return WordFrequency.engine.full_frequency(word)

    @staticmethod
    def partial_frequency(
        pattern: str,
    ) -> int:
        '''
        Iterating over all the existing dictionary words,
        and checking if the pattern exists in these words. Every
        matched word is accumulated by its frequency.

        Args:
            pattern(str): a pattern to check against the dictionary

        Returns:
            int: the sum of frequencies over all the words the pattern matches

        Raises:
            None
        '''
        if WordFrequency.engine is None:
            WordFrequency.load_dictionary()

        return WordFrequency.engine.partial_frequency(pattern)
