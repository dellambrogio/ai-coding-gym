import pytest
from solution import Calendar


def test_non_overlapping_bookings():
    c = Calendar()
    assert c.book(1, 3) and c.book(5, 8)


def test_touching_intervals_allowed():
    c = Calendar()
    assert c.book(1, 3) and c.book(3, 5) and c.book(0, 1)


def test_overlap_rejected():
    c = Calendar()
    c.book(10, 20)
    assert not c.book(15, 25)
    assert not c.book(5, 11)


def test_contained_and_containing_rejected():
    c = Calendar()
    c.book(10, 20)
    assert not c.book(12, 13)
    assert not c.book(0, 30)


def test_rejected_booking_not_stored():
    c = Calendar()
    c.book(10, 20)
    assert not c.book(15, 30)
    assert c.book(20, 30)


@pytest.mark.parametrize("s,e", [(5, 5), (6, 5)])
def test_invalid_interval(s, e):
    with pytest.raises(ValueError):
        Calendar().book(s, e)
