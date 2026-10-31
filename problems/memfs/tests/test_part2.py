import pytest
from solution import FileSystem


def test_append_creates_and_extends():
    fs = FileSystem()
    fs.append("/log", "a")
    fs.append("/log", "bc")
    assert fs.read("/log") == "abc"


def test_size_file_and_dir():
    fs = FileSystem()
    fs.mkdir("/d/sub")
    fs.write("/d/x", "12345")
    fs.write("/d/sub/y", "123")
    assert fs.size("/d/x") == 5
    assert fs.size("/d") == 8
    assert fs.size("/") == 8
    assert fs.size("/d/sub") == 3


def test_rm_file():
    fs = FileSystem()
    fs.write("/f", "x")
    fs.rm("/f")
    assert fs.ls("/") == []


def test_rm_empty_dir_without_recursive():
    fs = FileSystem()
    fs.mkdir("/d")
    fs.rm("/d")
    assert fs.ls("/") == []


def test_rm_non_empty_dir():
    fs = FileSystem()
    fs.mkdir("/d/e")
    with pytest.raises(OSError):
        fs.rm("/d")
    fs.rm("/d", recursive=True)
    assert fs.ls("/") == []


def test_rm_errors():
    fs = FileSystem()
    with pytest.raises(ValueError):
        fs.rm("/")
    with pytest.raises(FileNotFoundError):
        fs.rm("/nope")
