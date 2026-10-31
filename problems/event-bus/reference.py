class EventBus:
    def __init__(self):
        self.subs = {}  # id -> (segments, handler, once)
        self.next_id = 1
        self.errors = []

    def subscribe(self, topic, handler, once=False):
        parts = topic.split(".")
        if any(not p for p in parts) or "#" in parts[:-1]:
            raise ValueError(f"invalid topic {topic!r}")
        sid = self.next_id
        self.next_id += 1
        self.subs[sid] = (parts, handler, once)
        return sid

    def unsubscribe(self, sub_id):
        return self.subs.pop(sub_id, None) is not None

    @staticmethod
    def _match(pattern, topic):
        if pattern[-1] == "#":
            pattern = pattern[:-1]
            if len(topic) < len(pattern):
                return False
            topic = topic[:len(pattern)]
        return len(pattern) == len(topic) and all(p in ("*", t) for p, t in zip(pattern, topic))

    def publish(self, topic, payload=None):
        parts = topic.split(".")
        if any(not p or p in ("*", "#") for p in parts):
            raise ValueError(f"invalid topic {topic!r}")
        matched = [(sid, s) for sid, s in list(self.subs.items()) if self._match(s[0], parts)]
        for sid, (_, handler, once) in matched:
            if once:
                self.subs.pop(sid, None)
            try:
                handler(payload)
            except Exception as e:
                self.errors.append((sid, e))
        return len(matched)
