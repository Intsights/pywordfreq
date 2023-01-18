import importlib.resources
import sys

from . import pywordfreq

PY_VERSION_MAJOR = sys.version_info.major
PY_VERSION_MINOR = sys.version_info.minor


def lazy_full_frequency(
    word,
):
    if PY_VERSION_MAJOR >= 3 and PY_VERSION_MINOR >= 11:
        with importlib.resources.files(
            __package__,
        ).joinpath(
            'word_frequencies.gz',
        ).open(
            'rb',
        ) as _word_frequencies_binary:
            word_frequencies_binary = _word_frequencies_binary.read()
    else:
        word_frequencies_binary = importlib.resources.read_binary(
            package=__package__,
            resource='word_frequencies.gz',
        )

    pywordfreq.load_dictionary(
        word_frequencies_binary
    )

    global full_frequency
    global partial_frequency

    full_frequency = pywordfreq.full_frequency
    partial_frequency = pywordfreq.partial_frequency

    return pywordfreq.full_frequency(
        word
    )


def lazy_partial_frequency(
    pattern,
):
    if PY_VERSION_MAJOR >= 3 and PY_VERSION_MINOR >= 11:
        with importlib.resources.files(
            __package__,
        ).joinpath(
            'word_frequencies.gz',
        ).open(
            'rb',
        ) as _word_frequencies_binary:
            word_frequencies_binary = _word_frequencies_binary.read()
    else:
        word_frequencies_binary = importlib.resources.read_binary(
            package=__package__,
            resource='word_frequencies.gz',
        )

    pywordfreq.load_dictionary(
        word_frequencies_binary
    )

    global full_frequency
    global partial_frequency

    full_frequency = pywordfreq.full_frequency
    partial_frequency = pywordfreq.partial_frequency

    return pywordfreq.partial_frequency(
        pattern
    )


full_frequency = lazy_full_frequency
partial_frequency = lazy_partial_frequency
