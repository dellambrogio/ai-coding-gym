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
    for i, container in enumerate(strings):
        for j, other in enumerate(strings):
            if i != j and other in container:
                return container
    return None


def find_shortest_contained_string(strings: list[str]) -> str | None:
    """Return the shortest string that contains another list member, or the empty result."""
    order = sorted(range(len(strings)), key=lambda i: len(strings[i]))
    for i in order:
        container = strings[i]
        # Only strings no longer than the container can occur in it.
        for j in order:
            if len(strings[j]) > len(container):
                break
            if i != j and strings[j] in container:
                return container
    return None


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
        node = self._root
        for ch in word:
            node = node.children.setdefault(ch, _TrieNode())
        node.count += 1
        node.word = word

    def find_contained_word(self, text: str) -> str | None:
        """Return some trie word occurring in text, or None.

        The trivial self-match (the whole text from position 0) is
        ignored unless the end node holds a duplicate of text.
        """
        for start in range(len(text)):
            node = self._root
            for end in range(start, len(text)):
                node = node.children.get(text[end])
                if node is None:
                    break
                if node.count == 0:
                    continue
                is_self = start == 0 and end == len(text) - 1
                if not is_self or node.count > 1:
                    return node.word
        return None

    def all_contained_words(self, text: str) -> list[str]:
        """Return every trie word occurring in text, sorted.

        No self-match discounting: callers decide what is in the trie.
        """
        found: set[str] = set()
        for start in range(len(text)):
            node = self._root
            for end in range(start, len(text)):
                node = node.children.get(text[end])
                if node is None:
                    break
                if node.count:
                    found.add(node.word)
        return sorted(found)

    def count(self, word: str) -> int:
        """How many times word was inserted."""
        node = self._root
        for ch in word:
            node = node.children.get(ch)
            if node is None:
                return 0
        return node.count


def find_contained_string_trie(strings: list[str]) -> str | None:
    """Insert everything into one trie, then scan each string."""
    trie = SubstringTrie()
    for s in strings:
        trie.insert(s)
    for s in strings:
        if trie.find_contained_word(s) is not None:
            return s
    return None


def find_all_contained_pairs(strings: list[str]) -> list[tuple[str, str]]:
    """Return all distinct (container, contained) pairs, sorted."""
    trie = SubstringTrie()
    for s in strings:
        trie.insert(s)
    pairs: set[tuple[str, str]] = set()
    for container in set(strings):
        for word in trie.all_contained_words(container):
            if word != container or trie.count(container) > 1:
                pairs.add((container, word))
    return sorted(pairs)
