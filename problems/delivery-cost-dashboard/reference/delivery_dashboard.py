from __future__ import annotations

from delivery_models import DeliveryRecord, calculate_delivery_cost_cents, cents_to_usd

SECONDS_PER_DAY = 24 * 3600


class DeliveryCostSystem:
    def __init__(self) -> None:
        self._driver_rates: dict[int, float] = {}
        self._deliveries: list[DeliveryRecord] = []
        self._total_cents = 0
        self._unpaid_cents = 0

    def add_driver(self, driver_id: int, usd_hourly_rate: float) -> None:
        if driver_id in self._driver_rates:
            raise ValueError(f"driver {driver_id} already exists")
        self._driver_rates[driver_id] = usd_hourly_rate

    def record_delivery(self, driver_id: int, start_time: int, end_time: int) -> None:
        if driver_id not in self._driver_rates:
            raise KeyError(f"unknown driver {driver_id}")
        cents = calculate_delivery_cost_cents(
            self._driver_rates[driver_id],
            start_time,
            end_time,
        )
        self._deliveries.append(DeliveryRecord(driver_id, start_time, end_time, cents))
        self._total_cents += cents
        self._unpaid_cents += cents

    def get_total_cost(self) -> float:
        return cents_to_usd(self._total_cents)

    def pay_up_to(self, pay_time: int) -> None:
        for record in self._deliveries:
            if not record.paid and record.end_time <= pay_time:
                record.paid = True
                self._unpaid_cents -= record.payout_cents

    def get_total_cost_unpaid(self) -> float:
        return cents_to_usd(self._unpaid_cents)

    def max_simultaneous_drivers_in_past_24_hours(self, now: int) -> int:
        window_start = now - SECONDS_PER_DAY
        by_driver: dict[int, list[tuple[int, int]]] = {}
        for r in self._deliveries:
            start, end = max(r.start_time, window_start), min(r.end_time, now)
            if start < end:
                by_driver.setdefault(r.driver_id, []).append((start, end))
        # Merge each driver's overlapping deliveries so a driver counts once.
        events: list[tuple[int, int]] = []
        for intervals in by_driver.values():
            intervals.sort()
            cur_start, cur_end = intervals[0]
            for start, end in intervals[1:]:
                if start <= cur_end:
                    cur_end = max(cur_end, end)
                else:
                    events += [(cur_start, 1), (cur_end, -1)]
                    cur_start, cur_end = start, end
            events += [(cur_start, 1), (cur_end, -1)]
        best = active = 0
        for _, delta in sorted(events):  # ends sort before starts at the same time
            active += delta
            best = max(best, active)
        return best
