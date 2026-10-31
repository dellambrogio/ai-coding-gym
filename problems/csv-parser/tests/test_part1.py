import pytest
from solution import parse_csv


def test_simple():
    assert parse_csv("a,b,c\n1,2,3") == [["a", "b", "c"], ["1", "2", "3"]]


def test_trailing_newline_and_crlf():
    assert parse_csv("a,b\r\n1,2\r\n") == [["a", "b"], ["1", "2"]]


def test_empty_fields():
    assert parse_csv("a,,c\n,,") == [["a", "", "c"], ["", "", ""]]


def test_quoted_comma_and_newline():
    assert parse_csv('name,note\n"Smith, J","line1\nline2"') == [["name", "note"], ["Smith, J", "line1\nline2"]]


def test_escaped_quotes():
    assert parse_csv('"say ""hi""",x') == [['say "hi"', "x"]]


def test_quoted_empty_field():
    assert parse_csv('""') == [[""]]
    assert parse_csv('a,""') == [["a", ""]]


def test_empty_lines_skipped():
    assert parse_csv("a\n\nb\n") == [["a"], ["b"]]
    assert parse_csv("") == []


def test_unterminated_quote():
    with pytest.raises(ValueError):
        parse_csv('a,"oops\nmore')
