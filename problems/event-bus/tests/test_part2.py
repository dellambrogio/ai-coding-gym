import pytest
from solution import EventBus


def matches(pattern, topic):
    bus = EventBus()
    bus.subscribe(pattern, lambda p: None)
    return bus.publish(topic, None) == 1


@pytest.mark.parametrize("pattern,topic,expected", [
    ("orders.*", "orders.created", True),
    ("orders.*", "orders", False),
    ("orders.*", "orders.eu.created", False),
    ("*.created", "users.created", True),
    ("orders.#", "orders", True),
    ("orders.#", "orders.created", True),
    ("orders.#", "orders.eu.created", True),
    ("orders.#", "users.created", False),
    ("#", "anything.at.all", True),
    ("a.*.c.#", "a.b.c", True),
    ("a.*.c.#", "a.b.d.c", False),
])
def test_wildcards(pattern, topic, expected):
    assert matches(pattern, topic) is expected


def test_order_across_patterns():
    bus, calls = EventBus(), []
    bus.subscribe("a.#", lambda p: calls.append(1))
    bus.subscribe("a.b", lambda p: calls.append(2))
    bus.subscribe("a.*", lambda p: calls.append(3))
    assert bus.publish("a.b", None) == 3
    assert calls == [1, 2, 3]


@pytest.mark.parametrize("pattern", ["a..b", "", "a.#.b", "#.a"])
def test_invalid_subscribe(pattern):
    with pytest.raises(ValueError):
        EventBus().subscribe(pattern, print)


@pytest.mark.parametrize("topic", ["a.*", "#", "a..b"])
def test_invalid_publish(topic):
    with pytest.raises(ValueError):
        EventBus().publish(topic, None)
