from solution import Calendar


def test_cancel_frees_slot():
    c = Calendar()
    c.book(10, 20)
    assert c.cancel(10, 20)
    assert c.book(15, 25)


def test_cancel_needs_exact_bounds():
    c = Calendar()
    c.book(10, 20)
    assert not c.cancel(10, 19)
    assert not c.cancel(0, 5)


def test_free_slots_basic():
    c = Calendar()
    c.book(9, 10)
    c.book(12, 13)
    assert c.free_slots(8, 18) == [(8, 9), (10, 12), (13, 18)]


def test_free_slots_adjacent_bookings_merge_busy_time():
    c = Calendar()
    c.book(9, 10)
    c.book(10, 11)
    assert c.free_slots(8, 12) == [(8, 9), (11, 12)]


def test_free_slots_min_length():
    c = Calendar()
    c.book(9, 10)
    c.book(12, 13)
    assert c.free_slots(8, 18, min_length=2) == [(10, 12), (13, 18)]


def test_free_slots_clips_bookings():
    c = Calendar()
    c.book(5, 9)
    c.book(17, 20)
    assert c.free_slots(8, 18) == [(9, 17)]


def test_free_slots_empty_calendar_and_fully_booked():
    assert Calendar().free_slots(0, 10) == [(0, 10)]
    c = Calendar()
    c.book(0, 10)
    assert c.free_slots(2, 8) == []
