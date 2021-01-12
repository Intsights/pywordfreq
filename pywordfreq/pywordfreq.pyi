class WordFrequency:
    @staticmethod
    def load_dictionary() -> None: ...

    @staticmethod
    def full_frequency(
        word: str,
    ) -> int: ...

    @staticmethod
    def partial_frequency(
        pattern: str,
    ) -> int: ...
