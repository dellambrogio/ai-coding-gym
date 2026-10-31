from __future__ import annotations


def sample_expenses() -> list[dict[str, str]]:
    return [
        {
            "expense_id": "001",
            "trip_id": "001",
            "amount_usd": "49.99",
            "expense_type": "supplies",
            "vendor_type": "restaurant",
            "vendor_name": "Outback Roadhouse",
        },
        {
            "expense_id": "002",
            "trip_id": "001",
            "amount_usd": "125.00",
            "expense_type": "supplies",
            "vendor_type": "retailer",
            "vendor_name": "Staples",
        },
        {
            "expense_id": "003",
            "trip_id": "002",
            "amount_usd": "153.00",
            "expense_type": "meals",
            "vendor_type": "restaurant",
            "vendor_name": "Olive Yurt",
        },
        {
            "expense_id": "004",
            "trip_id": "002",
            "amount_usd": "1996.00",
            "expense_type": "airfare",
            "vendor_type": "transportation",
            "vendor_name": "Southeast Airlines",
        },
        {
            "expense_id": "005",
            "trip_id": "002",
            "amount_usd": "34.68",
            "expense_type": "meals",
            "vendor_type": "restaurant",
            "vendor_name": "The Great Grill",
        },
        {
            "expense_id": "006",
            "trip_id": "002",
            "amount_usd": "22.40",
            "expense_type": "meals",
            "vendor_type": "restaurant",
            "vendor_name": "The Great Grill",
        },
        {
            "expense_id": "007",
            "trip_id": "003",
            "amount_usd": "59.50",
            "expense_type": "entertainment",
            "vendor_type": "theater",
            "vendor_name": "Silver Screen",
        },
    ]
