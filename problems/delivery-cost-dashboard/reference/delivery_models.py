from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal


SECONDS_PER_HOUR = 3600
CENTS_PER_DOLLAR = Decimal("100")


def calculate_delivery_cost_cents(hourly_rate_usd: float, start_time: int, end_time: int) -> int:
    duration_seconds = end_time - start_time
    if duration_seconds < 0:
        raise ValueError("end_time must be >= start_time")

    hourly_rate_cents = Decimal(str(hourly_rate_usd)) * CENTS_PER_DOLLAR
    cost = hourly_rate_cents * duration_seconds / SECONDS_PER_HOUR
    return int(cost.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def cents_to_usd(amount_cents: int) -> float:
    return amount_cents / 100.0


@dataclass
class DeliveryRecord:
    driver_id: int
    start_time: int
    end_time: int
    payout_cents: int
    paid: bool = False
