import pathlib
import typing

from . import pywordfreq


class WordFrequency:
    '''
    WordFrequency class is a wrapper against Wikipedia word frequency
    corpus. It includes two functions to check words/patterns against
    this dictionary. The library is written in Rust to achieve its
    performance and safety guarantees.
    '''
    word_frequency_engine: typing.Optional[pywordfreq.WordFrequency] = None

    def __init__(
        self,
    ) -> None:
        if WordFrequency.word_frequency_engine is None:
            current_folder_path = pathlib.Path(__file__).parent.absolute()
            word_frequencies_file_path = current_folder_path.joinpath('word_frequencies.gz').absolute()
            WordFrequency.word_frequency_engine = pywordfreq.WordFrequency(
                word_frequencies_file_path=str(word_frequencies_file_path),
            )

    def word_frequency(
        self,
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
        return self.word_frequency_engine.word_frequency(word)

    def word_partial_frequency(
        self,
        pattern: str,
    ) -> int:
        '''
        Return the word frequency existing as a substring of other words.
        The way it works is by iterating over all the existing words in the
        dictionary, and check if the pattern exists in these words. Every
        positive word is accumulated to a single frequency value.

        Args:
            pattern(str): a pattern to check against the dictionary

        Returns:
            int: the sum of frequencies over all the words the pattern matches

        Raises:
            None
        '''
        return self.word_frequency_engine.word_partial_frequency(pattern)
