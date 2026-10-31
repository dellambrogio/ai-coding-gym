## Part 1: Publish and subscribe

In `solution.py`, implement `class EventBus`. Topics are dot-separated names like `orders.created`.

- `subscribe(topic: str, handler) -> int`: register `handler` (a function taking one argument, the payload) and return a subscription id. Ids are unique.
- `publish(topic: str, payload) -> int`: call every handler subscribed to exactly this topic, in the order they subscribed, and return how many were called.
- `unsubscribe(sub_id) -> bool`: `False` if the id is unknown.
