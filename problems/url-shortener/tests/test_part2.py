import pytest
from solution import Shortener


def test_alias():
    s = Shortener()
    assert s.shorten("https://a.com", alias="my-link") == "my-link"
    assert s.resolve("my-link") == "https://a.com"


def test_alias_taken_by_other_url():
    s = Shortener()
    s.shorten("https://a.com", alias="promo")
    with pytest.raises(ValueError):
        s.shorten("https://b.com", alias="promo")
    assert s.shorten("https://a.com", alias="promo") == "promo"


@pytest.mark.parametrize("alias", ["ab", "x" * 31, "has space", "émoji"])
def test_invalid_alias(alias):
    with pytest.raises(ValueError):
        Shortener().shorten("https://a.com", alias=alias)


def test_url_keeps_automatic_code_alongside_alias():
    s = Shortener()
    auto = s.shorten("https://a.com")
    s.shorten("https://a.com", alias="alias1")
    assert s.shorten("https://a.com") == auto


def test_automatic_code_created_after_alias():
    s = Shortener()
    s.shorten("https://a.com", alias="alias1")
    auto = s.shorten("https://a.com")
    assert auto != "alias1" and len(auto) == 6


def test_clicks():
    s = Shortener()
    code = s.shorten("https://a.com")
    for _ in range(3):
        s.resolve(code)
    assert s.clicks(code) == 3
    assert s.clicks("nothing") == 0
