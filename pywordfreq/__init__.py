import importlib.resources

from . import pywordfreq


def lazy_full_frequency(
    word,
):
    pywordfreq.load_dictionary(
        importlib.resources.read_binary(
            package=__package__,
            resource='word_frequencies.gz',
        )
    )

    global full_frequency
    global partial_frequency

    full_frequency = pywordfreq.full_frequency
    partial_frequency = pywordfreq.partial_frequency

    return pywordfreq.full_frequency(word)


def lazy_partial_frequency(
    pattern,
):
    pywordfreq.load_dictionary(
        importlib.resources.read_binary(
            package=__package__,
            resource='word_frequencies.gz',
        )
    )

    global full_frequency
    global partial_frequency

    full_frequency = pywordfreq.full_frequency
    partial_frequency = pywordfreq.partial_frequency

    return pywordfreq.partial_frequency(pattern)


full_frequency = lazy_full_frequency
partial_frequency = lazy_partial_frequency
