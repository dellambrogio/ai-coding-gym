from solution import Editor


def test_type_appends():
    e = Editor()
    e.type("hello")
    e.type(" world")
    assert e.text == "hello world" and e.cursor == 11


def test_type_in_middle():
    e = Editor()
    e.type("held")
    e.move(3)
    e.type("lo worl")
    assert e.text == "hello world" and e.cursor == 10


def test_move_clamps():
    e = Editor()
    e.type("abc")
    e.move(-5)
    assert e.cursor == 0
    e.move(99)
    assert e.cursor == 3


def test_backspace():
    e = Editor()
    e.type("abcdef")
    e.move(4)
    e.backspace(2)
    assert e.text == "abef" and e.cursor == 2


def test_backspace_more_than_available():
    e = Editor()
    e.type("abc")
    e.move(2)
    e.backspace(10)
    assert e.text == "c" and e.cursor == 0


def test_backspace_default_one():
    e = Editor()
    e.type("abc")
    e.backspace()
    assert e.text == "ab"
