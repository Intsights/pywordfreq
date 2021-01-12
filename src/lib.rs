use pyo3::prelude::*;
use std::collections::{HashMap, HashSet};
use suffix::SuffixTable;

const NUMBER_OF_WORDS: usize = 1_178_632;
const TOTAL_WORDS_TEXT_LEN: usize = 10_276_353;

static mut WORDS_TEXT: String = String::new();

#[pyclass]
#[text_signature = "(word_frequencies, /)"]
struct WordFrequency {
    suffix_table: SuffixTable<'static, 'static>,
    word_frequencies: HashMap<&'static str, usize>,
}

#[pymethods]
impl WordFrequency {
    #[new]
    fn new(
        word_frequencies_text: &str,
    ) -> Self {
        let mut word_frequencies = HashMap::<&'static str, usize>::with_capacity(NUMBER_OF_WORDS);
        let suffix_table: SuffixTable;
        unsafe {
            WORDS_TEXT.reserve(TOTAL_WORDS_TEXT_LEN);
            WORDS_TEXT.push('\n');

            word_frequencies_text
                .lines()
                .filter(|line| !line.is_empty())
                .for_each(
                    |line| {
                        let splitted_line: Vec<&str> = line.split(';').collect();
                        let word: &str = splitted_line[0];
                        let frequency: usize = splitted_line[1].parse().unwrap();

                        WORDS_TEXT.push_str(word);
                        WORDS_TEXT.push('\n');
                        let end_of_word = WORDS_TEXT.len() - 1;
                        let start_of_word = WORDS_TEXT.len() - 1 - word.len();

                        let word_slice = &WORDS_TEXT[start_of_word..end_of_word];

                        word_frequencies.insert(
                            word_slice,
                            frequency,
                        );
                    }
                );

                suffix_table = SuffixTable::new(WORDS_TEXT.as_str());
            }

            WordFrequency { suffix_table, word_frequencies }
        }

    #[text_signature = "(word, /)"]
    fn full_frequency(
        &self,
        word: &str,
    ) -> usize {
        self.word_frequencies.get(word.to_ascii_lowercase().as_str()).unwrap_or(&0).to_owned()
    }

    #[text_signature = "(pattern, /)"]
    fn partial_frequency(
        &self,
        pattern: &str,
    ) -> usize {
        let mut cumulative_frequency = 0usize;
        let mut found_words = HashSet::<&str>::new();

        let word_lowered = pattern.to_ascii_lowercase();

        self.suffix_table.positions(word_lowered.as_str())
            .iter()
            .for_each(
                |suffix_index| {
                    let start_index: usize = match &self.suffix_table.text()[..*suffix_index as usize].rfind('\n') {
                        Some(start_index) => start_index + 1,
                        None => 0,
                    };
                    let end_index: usize = match &self.suffix_table.text()[*suffix_index as usize..].find('\n') {
                        Some(end_index) => *suffix_index as usize + end_index,
                        None => self.suffix_table.text().len(),
                    };
                    let full_word = &self.suffix_table.text()[start_index..end_index];
                    if full_word != word_lowered && found_words.insert(full_word) {
                        cumulative_frequency += *self.word_frequencies.get(full_word).unwrap_or(&0);
                    }
                }
            );

        cumulative_frequency
    }
}

#[pymodule]
fn pywordfreq(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<WordFrequency>()?;

    Ok(())
}
