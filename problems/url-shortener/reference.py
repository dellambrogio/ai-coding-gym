import random
import re
import string
import time

ALPHABET = string.ascii_letters + string.digits
ALIAS = re.compile(r"[A-Za-z0-9_-]{3,30}")


class Shortener:
    def __init__(self, clock=time.monotonic):
        self.clock = clock
        self.codes = {}  # code -> [url, expires_at or None, clicks]
        self.auto = {}  # url -> automatic code

    def _live(self, code):
        entry = self.codes.get(code)
        if entry and entry[1] is not None and self.clock() >= entry[1]:
            del self.codes[code]
            return None
        return entry

    def shorten(self, url, alias=None, ttl=None):
        if not url.startswith(("http://", "https://")):
            raise ValueError("invalid url")
        if ttl is not None and ttl <= 0:
            raise ValueError("ttl must be > 0")
        expires = None if ttl is None else self.clock() + ttl
        if alias is not None:
            if not ALIAS.fullmatch(alias):
                raise ValueError("invalid alias")
            entry = self._live(alias)
            if entry:
                if entry[0] != url:
                    raise ValueError("alias taken")
                return alias
            self.codes[alias] = [url, expires, 0]
            return alias
        code = self.auto.get(url)
        if code and self._live(code) and self.codes[code][0] == url:
            return code
        while True:
            code = "".join(random.choices(ALPHABET, k=6))
            if not self._live(code):
                break
        self.codes[code] = [url, expires, 0]
        self.auto[url] = code
        return code

    def resolve(self, code):
        entry = self._live(code)
        if not entry:
            return None
        entry[2] += 1
        return entry[0]

    def clicks(self, code):
        entry = self._live(code)
        return entry[2] if entry else 0

    def delete(self, code):
        if not self._live(code):
            return False
        del self.codes[code]
        return True
