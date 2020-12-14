<p align="center">
    <a href="https://github.com/intsights/pywordfreq">
        <img src="https://raw.githubusercontent.com/intsights/pywordfreq/master/images/logo.png" alt="Logo">
    </a>
    <h3 align="center">
        Word frequency checker based on Wikipedia corpus written in Rust
    </h3>
</p>


![license](https://img.shields.io/badge/MIT-License-blue)
![Python](https://img.shields.io/badge/Python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue)
![OS](https://img.shields.io/badge/OS-Mac%20%7C%20Linux%20%7C%20Windows-blue)
![Build](https://github.com/intsights/pywordfreq/workflows/Build/badge.svg)
[![PyPi](https://img.shields.io/pypi/v/pywordfreq.svg)](https://pypi.org/project/pywordfreq/)

## Table of Contents

- [Table of Contents](#table-of-contents)
- [About The Project](#about-the-project)
  - [Built With](#built-with)
  - [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Contact](#contact)


## About The Project

A library written in Rust to check against Wikipedia word frequency corpus. The library is very fast, memory efficient, and safe.
Full lookups are done using a Hashmap data structure. Partial frequency searches are based on a Suffix Array data structure [suffix](https://github.com/BurntSushi/suffix) to perform quick sub-patterns lookups over the dictionary.


### Built With

* [pyo3](https://github.com/PyO3/pyo3)
* [suffix](https://github.com/BurntSushi/suffix)


### Installation

```sh
pip3 install pywordfreq
```


## Usage

```python
import pywordfreq


# On the first use of library, the engine is loaded with the dictionary.
# It is worth to mention that there is a significant ammount
# of memory overhead for the engine.

# This function checks the frequency of the word "the" in the corpus
pywordfreq.WordFrequency.full_frequency(
    word="the",
)
# This function checks the frequency of the word "inter" as a pattern
# in other words of the dictionary.
pywordfreq.WordFrequency.partial_frequency(
    pattern="inter",
)
```


## License

Distributed under the MIT License. See `LICENSE` for more information.


## Contact

Gal Ben David - gal@intsights.com

Project Link: [https://github.com/intsights/pywordfreq](https://github.com/intsights/pywordfreq)
