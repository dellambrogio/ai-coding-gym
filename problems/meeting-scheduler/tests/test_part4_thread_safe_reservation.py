from __future__ import annotations

import threading
import time
import unittest

from scheduler import Booking, ThreadSafeMeetingScheduler


class TestPart4ThreadSafeReservation(unittest.TestCase):
    def test_reserves_distinct_slots_under_concurrency(self):
        scheduler = ThreadSafeMeetingScheduler()
        scheduler._reservation_hook = lambda: time.sleep(0.01)

        results: list[int] = []
        exceptions: list[BaseException] = []

        def worker() -> None:
            try:
                results.append(scheduler.reserve_earliest_slot(0, 30))
            except BaseException as exc:  # pragma: no cover
                exceptions.append(exc)

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual(exceptions, [])
        self.assertEqual(sorted(results), [0, 30, 60, 90])
        self.assertEqual(
            scheduler.bookings,
            [Booking(0, 30), Booking(30, 60),
             Booking(60, 90), Booking(90, 120)],
        )


if __name__ == "__main__":
    unittest.main()
