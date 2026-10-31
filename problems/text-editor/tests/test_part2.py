from solution import Editor


def test_undo_type():
    e = Editor()
    e.type("ab")
    e.type("cd")
    assert e.undo()
    assert e.text == "ab" and e.cursor == 2


def test_undo_restores_cursor_before_edit():
    e = Editor()
    e.type("hello")
    e.move(1)
    e.backspace()
    assert e.text == "ello"
    e.undo()
    assert e.text == "hello" and e.cursor == 1


def test_undo_nothing():
    assert Editor().undo() is False


def test_redo():
    e = Editor()
    e.type("abc")
    e.move(0)
    e.type("X")
    e.undo()
    assert e.redo()
    assert e.text == "Xabc" and e.cursor == 1
    assert e.redo() is False


def test_new_edit_clears_redo():
    e = Editor()
    e.type("a")
    e.undo()
    e.type("b")
    assert e.redo() is False
    assert e.text == "b"


def test_multiple_undo_redo():
    e = Editor()
    for ch in "abc":
        e.type(ch)
    e.undo()
    e.undo()
    assert e.text == "a"
    e.redo()
    assert e.text == "ab"
    e.undo()
    e.undo()
    assert e.text == "" and e.undo() is False


def test_noop_edits_not_recorded():
    e = Editor()
    e.type("a")
    e.type("")
    e.move(0)
    e.backspace()
    e.undo()
    assert e.text == ""
