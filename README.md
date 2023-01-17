<p align="center">
    <a href="https://github.com/intsights/pywordfreq">
        <img src="https://raw.githubusercontent.com/intsights/pywordfreq/master/images/logo.png" alt="Logo">
    </a>
    <h3 align="center">
        Word frequency checker based on Wikipedia corpus written in Rust
    </h3>
</p>


![license](https://img.shields.io/badge/MIT-License-blue)
![Python](https://img.shields.io/badge/Python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)
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

Rust library for checking against the Wikipedia word frequency corpus. The library is fast, memory efficient, and secure.
The data structure used to do full lookups is the Hashmap. A Suffix Array data structure [suffix](https://github.com/BurntSushi/suffix) is used to perform quick lookups of sub-patterns over the dictionary.


### Built With

* [pyo3](https://github.com/PyO3/pyo3)
* [suffix](https://github.com/BurntSushi/suffix)
* [ahash](https://github.com/tkaitchuck/ahash)


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
pywordfreq.full_frequency(
    word="the",
)
# This function checks the frequency of the word "inter" as a pattern
# in other words of the dictionary.
pywordfreq.partial_frequency(
    pattern="inter",
)
```


## License

Distributed under the MIT License. See `LICENSE` for more information.


## Contact

Gal Ben David - gal@intsights.com

Project Link: [https://github.com/intsights/pywordfreq](https://github.com/intsights/pywordfreq)
