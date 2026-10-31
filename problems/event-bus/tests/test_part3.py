from solution import EventBus


def test_failing_handler_does_not_stop_others():
    bus, got = EventBus(), []

    def boom(p):
        raise RuntimeError("boom")

    bad = bus.subscribe("t", boom)
    bus.subscribe("t", got.append)
    assert bus.publish("t", 1) == 2
    assert got == [1]
    assert len(bus.errors) == 1
    sid, exc = bus.errors[0]
    assert sid == bad and isinstance(exc, RuntimeError)


def test_once():
    bus, got = EventBus(), []
    bus.subscribe("t", got.append, once=True)
    bus.subscribe("t", got.append)
    assert bus.publish("t", 1) == 2
    assert bus.publish("t", 2) == 1
    assert got == [1, 1, 2]


def test_once_removed_even_if_it_fails():
    bus = EventBus()

    def boom(p):
        raise ValueError

    bus.subscribe("t", boom, once=True)
    bus.publish("t", None)
    assert bus.publish("t", None) == 0


def test_subscribe_during_publish_takes_effect_next_time():
    bus, got = EventBus(), []

    def adder(p):
        bus.subscribe("t", got.append)

    bus.subscribe("t", adder, once=True)
    assert bus.publish("t", "first") == 1
    assert got == []
    assert bus.publish("t", "second") == 1
    assert got == ["second"]


def test_unsubscribe_during_publish_takes_effect_next_time():
    bus, got = EventBus(), []
    ids = {}

    def remover(p):
        bus.unsubscribe(ids["victim"])

    bus.subscribe("t", remover)
    ids["victim"] = bus.subscribe("t", got.append)
    assert bus.publish("t", 1) == 2
    assert got == [1]
    assert bus.publish("t", 2) == 1
    assert got == [1]
