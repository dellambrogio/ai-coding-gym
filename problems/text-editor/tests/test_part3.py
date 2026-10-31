from solution import Editor


def make(text):
    e = Editor()
    e.type(text)
    return e


def test_type_replaces_selection():
    e = make("hello world")
    e.select(0, 5)
    e.type("howdy")
    assert e.text == "howdy world" and e.cursor == 5


def test_backspace_deletes_selection_ignoring_n():
    e = make("hello world")
    e.select(11, 5)
    e.backspace(100)
    assert e.text == "hello" and e.cursor == 5


def test_copy_paste():
    e = make("abc")
    e.select(0, 2)
    assert e.copy() == "ab"
    e.move(3)
    e.paste()
    assert e.text == "abcab"


def test_cut_and_undo():
    e = make("abcdef")
    e.select(2, 4)
    assert e.cut() == "cd"
    assert e.text == "abef" and e.cursor == 2
    e.undo()
    assert e.text == "abcdef"
    e.paste()
    assert e.text == "abcdcdef"


def test_replace_selection_is_one_undo():
    e = make("hello")
    e.select(0, 5)
    e.type("bye")
    e.undo()
    assert e.text == "hello"


def test_copy_without_selection():
    e = make("abc")
    e.select(0, 1)
    e.copy()
    e.move(3)
    assert e.copy() == ""
    e.paste()
    assert e.text == "abca"


def test_move_clears_selection():
    e = make("abc")
    e.select(0, 3)
    e.move(3)
    e.type("!")
    assert e.text == "abc!"


def test_empty_selection_and_clamping():
    e = make("abc")
    e.select(2, 2)
    e.type("X")
    assert e.text == "abXc"
    e.select(-10, 100)
    assert e.copy() == "abXc"
