"""Character tokenizer."""

from abc import ABC

import regex


class Tokenizer(ABC):
    """Abstract interface for a tokenizer."""

    def encode(self, string: str) -> list[int]:
        """Convert a string to a sequence of integers (tokens)."""
        raise NotImplementedError

    def decode(self, indices: list[int]) -> str:
        """Convert a sequence of integers (tokens) to a string."""
        raise NotImplementedError

    def get_compression_ratio(self, string: str, indices: list[int]) -> float:
        """Given `string` that has been tokenized into `indices` returns the compression ratio."""
        num_bytes = len(bytes(string, encoding="utf-8"))
        num_tokens = len(indices)
        return num_bytes / num_tokens


class CharacterTokenizer(Tokenizer):
    """Represent a string as a sequence of Unicode code points."""

    def encode(self, string: str) -> list[int]:
        indices = list(map(ord, string))
        return indices

    def decode(self, indices: list[int]) -> str:
        string = "".join(list(map(chr, indices)))
        return string


class ByteTokenizer(Tokenizer):
    """Represent a string as a sequence of bytes."""

    def encode(self, string: str) -> list[int]:
        string_bytes = string.encode("utf-8")
        indices = list(map(int, string_bytes))
        return indices

    def decode(self, indices: list[int]) -> str:
        string_bytes = bytes(indices)
        string = string_bytes.decode("utf-8")
        return string


class WordTokenizer(Tokenizer):
    """Split a string into words (usually on spaces)."""

    def __init__(self):
        # This regular expression keeps all alphanumeric characters together (words).
        self.regex_pattern = r"\w+|."

        # GPT2_TOKENIZER_REGEX
        # https://github.com/openai/tiktoken/blob/main/tiktoken_ext/openai_public.py#L23
        self.regex_pattern = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""

    def encode(self, string: str) -> list[str]:
        segments = regex.findall(self.regex_pattern, string)
        return segments

    def decode(self, segments: list[str]) -> str:
        string = "".join(segments)
        return string


if __name__ == "__main__":

    string = "Hello, 🌍! 你好!"
    print(string)

    tokenizers = []
    tokenizers.append(CharacterTokenizer())
    tokenizers.append(ByteTokenizer())
    tokenizers.append(WordTokenizer())

    for tokenizer in tokenizers:
        indices = tokenizer.encode(string)
        print(indices)

        string = tokenizer.decode(indices)
        print(string)

        print(tokenizer.get_compression_ratio(string, indices))
