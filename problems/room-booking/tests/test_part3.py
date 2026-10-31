import pytest
from solution import Calendar


def test_two_rooms_allow_double_booking():
    c = Calendar(rooms=2)
    assert c.book(0, 10) and c.book(5, 15)
    assert not c.book(6, 7)


def test_triple_overlap_only_matters_at_same_time():
    c = Calendar(rooms=2)
    assert c.book(0, 10)
    assert c.book(0, 5)
    assert c.book(5, 10)
    assert not c.book(4, 6)


def test_free_slots_with_rooms():
    c = Calendar(rooms=2)
    c.book(0, 10)
    c.book(5, 15)
    assert c.free_slots(0, 20) == [(0, 5), (10, 20)]


def test_cancel_with_rooms():
    c = Calendar(rooms=2)
    c.book(0, 10)
    c.book(0, 10)
    assert not c.book(0, 10)
    assert c.cancel(0, 10)
    assert c.book(0, 10)


def test_default_is_one_room():
    c = Calendar()
    c.book(0, 10)
    assert not c.book(5, 6)


def test_invalid_rooms():
    with pytest.raises(ValueError):
        Calendar(rooms=0)
