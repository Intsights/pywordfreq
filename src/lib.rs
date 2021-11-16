use ahash::{AHashMap, AHashSet};
use flate2::read::GzDecoder;
use once_cell::unsync::Lazy;
use pyo3::prelude::*;
use pyo3::types::PyUnicode;
use std::io::prelude::*;
use suffix::SuffixTable;

static mut WORDS_TEXT: String = String::new();
static mut SUFFIX_TABLE: Lazy<SuffixTable<'static, 'static>> = Lazy::new(
    || unsafe {
        SuffixTable::new(WORDS_TEXT.as_str())
    }
);
static mut WORD_FREQUENCIES: Lazy<AHashMap<&'static str, usize>> = Lazy::new(
    || {
        AHashMap::new()
    }
);
static mut WORD_FREQUENCIES_BY_START_INDEX: Lazy<AHashMap<usize, usize>> = Lazy::new(
    || {
        AHashMap::new()
    }
);
static mut FOUND_WORDS_START_INDEX: Lazy<AHashSet<usize>> = Lazy::new(
    || {
        AHashSet::with_capacity(1000)
    }
);


#[pymodule]
fn pywordfreq(_py: Python, m: &PyModule) -> PyResult<()> {
    #[pyfn(m)]
    fn load_dictionary(
        dictionary_compressed: &[u8],
    ) {
        let mut dictionary_decoder = GzDecoder::new(dictionary_compressed);
        let mut word_frequencies_text = String::new();
        dictionary_decoder.read_to_string(&mut word_frequencies_text).unwrap();

        let mut number_of_words = 0;
        let mut total_words_text_len = 0;
        for line in word_frequencies_text.lines() {
            number_of_words += 1;
            total_words_text_len += line.rfind(';').unwrap() + 1;
        }

        unsafe {
            WORD_FREQUENCIES.reserve(number_of_words);
            WORDS_TEXT.reserve(total_words_text_len);

            for line in word_frequencies_text.lines() {
                if let Some((word, frequency)) = line.rsplit_once(';') {
                    let frequency: usize = frequency.parse().unwrap();
                    let start_of_word = WORDS_TEXT.len();
                    WORDS_TEXT.push_str(word);
                    WORDS_TEXT.push('\n');

                    WORD_FREQUENCIES.insert(
                        WORDS_TEXT.get_unchecked(start_of_word..start_of_word + word.len()),
                        frequency,
                    );
                    WORD_FREQUENCIES_BY_START_INDEX.insert(
                        start_of_word,
                        frequency,
                    );
                }
            }
        }
    }

    #[pyfn(m)]
    fn full_frequency(
        word: &PyUnicode,
    ) -> usize {
        unsafe {
            match WORD_FREQUENCIES.get(word.to_string_lossy().to_ascii_lowercase().as_str()) {
                Some(frequency) => {
                    *frequency
                },
                None => 0
            }
        }
    }

    #[pyfn(m)]
    fn partial_frequency(
        pattern: &str,
    ) -> usize {
        let word_lowered = pattern.to_ascii_lowercase();
        let mut cumulative_frequency = 0usize;

        unsafe {
            FOUND_WORDS_START_INDEX.clear();
            let suffix_table_text = SUFFIX_TABLE.text();

            for suffix_index in SUFFIX_TABLE.positions(word_lowered.as_str()) {
                let start_index: usize = match suffix_table_text.get_unchecked(..*suffix_index as usize).rfind('\n') {
                    Some(start_index) => start_index + 1,
                    None => 0,
                };
                if FOUND_WORDS_START_INDEX.insert(start_index) {
                    cumulative_frequency += WORD_FREQUENCIES_BY_START_INDEX.get(&start_index).unwrap_or(&0);
                }
            }

            cumulative_frequency -= WORD_FREQUENCIES.get(word_lowered.as_str()).unwrap_or(&0);
        }

        cumulative_frequency
    }

    Ok(())
}
