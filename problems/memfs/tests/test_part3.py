import pytest
from solution import FileSystem


def make_fs():
    fs = FileSystem()
    fs.mkdir("/src/lib")
    fs.mkdir("/dst")
    fs.write("/src/main.py", "m")
    fs.write("/src/lib/util.py", "u")
    fs.write("/src/lib/notes.txt", "n")
    return fs


def test_rename_file():
    fs = make_fs()
    fs.mv("/src/main.py", "/src/app.py")
    assert fs.read("/src/app.py") == "m"
    assert "main.py" not in fs.ls("/src")


def test_move_into_existing_dir():
    fs = make_fs()
    fs.mv("/src/lib", "/dst")
    assert fs.ls("/dst") == ["lib"]
    assert fs.read("/dst/lib/util.py") == "u"
    assert fs.ls("/src") == ["main.py"]


def test_move_onto_existing_file_fails():
    fs = make_fs()
    fs.write("/dst/main.py", "other")
    with pytest.raises(FileExistsError):
        fs.mv("/src/main.py", "/dst")
    assert fs.read("/src/main.py") == "m"


def test_move_into_own_subtree():
    fs = make_fs()
    with pytest.raises(ValueError):
        fs.mv("/src", "/src/lib")


def test_mv_errors():
    fs = make_fs()
    with pytest.raises(FileNotFoundError):
        fs.mv("/nope", "/dst")
    with pytest.raises(FileNotFoundError):
        fs.mv("/src/main.py", "/missing/dir/x.py")


def test_find():
    fs = make_fs()
    assert fs.find("/", "*.py") == ["/src/lib/util.py", "/src/main.py"]
    assert fs.find("/src/lib", "*") == ["/src/lib/notes.txt", "/src/lib/util.py"]
    assert fs.find("/", "?ain.py") == ["/src/main.py"]
    assert fs.find("/", "*.PY") == []
