from __future__ import annotations

from delivery_models import calculate_delivery_cost_cents


class DeliveryCostSystem:
    def __init__(self) -> None:
        self._driver_rates: dict[int, float] = {}

    def add_driver(self, driver_id: int, usd_hourly_rate: float) -> None:
        raise NotImplementedError("add_driver() not implemented yet.")

    def record_delivery(self, driver_id: int, start_time: int, end_time: int) -> None:
        _ = calculate_delivery_cost_cents(
            self._driver_rates[driver_id],
            start_time,
            end_time,
        )
        raise NotImplementedError("record_delivery() not implemented yet.")

    def get_total_cost(self) -> float:
        raise NotImplementedError("get_total_cost() not implemented yet.")

    def pay_up_to(self, pay_time: int) -> None:
        raise NotImplementedError("pay_up_to() not implemented yet.")

    def get_total_cost_unpaid(self) -> float:
        raise NotImplementedError(
            "get_total_cost_unpaid() not implemented yet.")

    def max_simultaneous_drivers_in_past_24_hours(self, now: int) -> int:
        raise NotImplementedError(
            "max_simultaneous_drivers_in_past_24_hours() not implemented yet.")
