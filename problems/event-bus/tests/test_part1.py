from solution import EventBus


def test_publish_calls_handler_with_payload():
    bus, got = EventBus(), []
    bus.subscribe("orders.created", got.append)
    assert bus.publish("orders.created", {"id": 1}) == 1
    assert got == [{"id": 1}]


def test_exact_topic_only():
    bus, got = EventBus(), []
    bus.subscribe("orders.created", got.append)
    assert bus.publish("orders.deleted", 1) == 0
    assert bus.publish("orders", 1) == 0
    assert got == []


def test_subscription_order():
    bus, calls = EventBus(), []
    bus.subscribe("t", lambda p: calls.append("first"))
    bus.subscribe("t", lambda p: calls.append("second"))
    bus.publish("t", None)
    assert calls == ["first", "second"]


def test_unsubscribe():
    bus, got = EventBus(), []
    a = bus.subscribe("t", got.append)
    b = bus.subscribe("t", got.append)
    assert a != b
    assert bus.unsubscribe(a) is True
    assert bus.unsubscribe(a) is False
    assert bus.publish("t", "x") == 1


def test_same_handler_twice_called_twice():
    bus, got = EventBus(), []
    bus.subscribe("t", got.append)
    bus.subscribe("t", got.append)
    bus.publish("t", 1)
    assert got == [1, 1]
