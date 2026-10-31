"""Find a string in a list that contains another member as a substring.

Every strategy in this module shares one contract: given a list of
strings, return one string from the list that contains at least one
other member (at a different position) as a contiguous substring, or
None when no such pair exists.

Rules shared by all strategies:
- every input string is non-empty,
- matching is case-sensitive,
- identical strings at different positions contain each other,
- any qualifying answer is acceptable.
"""

from __future__ import annotations


def find_contained_string(strings: list[str]) -> str | None:
    """Check every pair of strings with a native substring test."""
    raise NotImplementedError("find_contained_string() not implemented yet.")


def find_shortest_contained_string(strings: list[str]) -> str | None:
    """Return the shortest string that contains another list member, or the empty result."""
    raise NotImplementedError("find_shortest_contained_string() not implemented yet.")


class _TrieNode:
    __slots__ = ("children", "count", "word")

    def __init__(self) -> None:
        self.children: dict[str, _TrieNode] = {}
        self.count = 0
        self.word: str | None = None


class SubstringTrie:
    """Trie over whole strings with end-of-word occurrence counts."""

    def __init__(self) -> None:
        self._root = _TrieNode()

    def insert(self, word: str) -> None:
        """Add one word; identical words share an end node and bump its count."""
        raise NotImplementedError("SubstringTrie.insert() not implemented yet.")

    def find_contained_word(self, text: str) -> str | None:
        """Return some trie word occurring in text, or None.

        The trivial self-match (the whole text from position 0) is
        ignored unless the end node holds a duplicate of text.
        """
        raise NotImplementedError(
            "SubstringTrie.find_contained_word() not implemented yet."
        )

    def all_contained_words(self, text: str) -> list[str]:
        """Return every trie word occurring in text, sorted.

        No self-match discounting: callers decide what is in the trie.
        """
        raise NotImplementedError(
            "SubstringTrie.all_contained_words() not implemented yet."
        )


def find_contained_string_trie(strings: list[str]) -> str | None:
    """Insert everything into one trie, then scan each string."""
    raise NotImplementedError("find_contained_string_trie() not implemented yet.")


def find_all_contained_pairs(strings: list[str]) -> list[tuple[str, str]]:
    """Return all distinct (container, contained) pairs, sorted."""
    raise NotImplementedError("find_all_contained_pairs() not implemented yet.")
