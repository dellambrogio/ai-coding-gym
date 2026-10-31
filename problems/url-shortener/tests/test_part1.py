import re

import pytest
from solution import Shortener


def test_code_format():
    code = Shortener().shorten("https://example.com/a")
    assert re.fullmatch(r"[A-Za-z0-9]{6}", code)


def test_resolve_roundtrip():
    s = Shortener()
    code = s.shorten("https://example.com/a")
    assert s.resolve(code) == "https://example.com/a"


def test_same_url_same_code():
    s = Shortener()
    assert s.shorten("http://x.io") == s.shorten("http://x.io")


def test_many_urls_unique_codes():
    s = Shortener()
    codes = {s.shorten(f"https://example.com/{i}") for i in range(2000)}
    assert len(codes) == 2000
    assert s.resolve(s.shorten("https://example.com/1234")) == "https://example.com/1234"


def test_unknown_code():
    assert Shortener().resolve("zzzzzz") is None


@pytest.mark.parametrize("url", ["example.com", "ftp://x.io", ""])
def test_invalid_url(url):
    with pytest.raises(ValueError):
        Shortener().shorten(url)
