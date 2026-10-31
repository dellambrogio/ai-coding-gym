## Part 3: Trip rules

Add trip-level rules (`scope == "trip"`, `matches_trip(trip_id, expenses)`), such as a maximum total per trip or per category per trip. Report them under `"trip_violations"`: `{trip_id: [rule_id, ...]}`, again only trips with violations, in rule order.

Tests: `tests/test_part3_trip_rules.py`
