import pytest
from solution import FileSystem


def test_mkdir_and_ls():
    fs = FileSystem()
    fs.mkdir("/a/b/c")
    assert fs.ls("/") == ["a"]
    assert fs.ls("/a/b") == ["c"]
    assert fs.ls("/a/b/c") == []


def test_mkdir_existing_is_ok():
    fs = FileSystem()
    fs.mkdir("/a")
    fs.write("/a/f", "x")
    fs.mkdir("/a")
    assert fs.read("/a/f") == "x"


def test_write_read_overwrite():
    fs = FileSystem()
    fs.write("/f.txt", "hello")
    assert fs.read("/f.txt") == "hello"
    fs.write("/f.txt", "bye")
    assert fs.read("/f.txt") == "bye"


def test_ls_sorted_and_on_file():
    fs = FileSystem()
    fs.mkdir("/d")
    fs.write("/d/b", "")
    fs.write("/d/a", "")
    fs.mkdir("/d/c")
    assert fs.ls("/d") == ["a", "b", "c"]
    assert fs.ls("/d/a") == ["a"]


def test_write_needs_parent():
    with pytest.raises(FileNotFoundError):
        FileSystem().write("/missing/f", "x")


def test_write_onto_directory():
    fs = FileSystem()
    fs.mkdir("/d")
    with pytest.raises(IsADirectoryError):
        fs.write("/d", "x")


def test_read_errors():
    fs = FileSystem()
    fs.mkdir("/d")
    with pytest.raises(FileNotFoundError):
        fs.read("/nope")
    with pytest.raises(IsADirectoryError):
        fs.read("/d")


def test_mkdir_through_file():
    fs = FileSystem()
    fs.write("/f", "x")
    with pytest.raises(FileExistsError):
        fs.mkdir("/f/sub")


def test_ls_missing():
    with pytest.raises(FileNotFoundError):
        FileSystem().ls("/nope")
