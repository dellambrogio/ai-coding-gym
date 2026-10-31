import fnmatch


class FileSystem:
    def __init__(self):
        self.root = {}  # dirs are dicts, files are str

    @staticmethod
    def _parts(path):
        if not path.startswith("/"):
            raise ValueError(f"path must be absolute: {path}")
        return [p for p in path.split("/") if p]

    def _node(self, parts):
        node = self.root
        for p in parts:
            if not isinstance(node, dict) or p not in node:
                raise FileNotFoundError("/" + "/".join(parts))
            node = node[p]
        return node

    def _parent(self, parts):
        if not parts:
            raise IsADirectoryError("/")
        parent = self._node(parts[:-1])
        if not isinstance(parent, dict):
            raise FileNotFoundError("/" + "/".join(parts[:-1]))
        return parent

    def mkdir(self, path):
        node = self.root
        for p in self._parts(path):
            node = node.setdefault(p, {})
            if not isinstance(node, dict):
                raise FileExistsError(path)

    def write(self, path, content, append=False):
        parts = self._parts(path)
        parent = self._parent(parts)
        if isinstance(parent.get(parts[-1]), dict):
            raise IsADirectoryError(path)
        parent[parts[-1]] = (parent.get(parts[-1], "") if append else "") + content

    def append(self, path, content):
        self.write(path, content, append=True)

    def read(self, path):
        node = self._node(self._parts(path))
        if isinstance(node, dict):
            raise IsADirectoryError(path)
        return node

    def ls(self, path):
        parts = self._parts(path)
        node = self._node(parts)
        return sorted(node) if isinstance(node, dict) else [parts[-1]]

    def size(self, path):
        def total(n):
            return sum(total(c) for c in n.values()) if isinstance(n, dict) else len(n)
        return total(self._node(self._parts(path)))

    def rm(self, path, recursive=False):
        parts = self._parts(path)
        if not parts:
            raise ValueError("cannot remove /")
        parent = self._node(parts[:-1])
        if not isinstance(parent, dict) or parts[-1] not in parent:
            raise FileNotFoundError(path)
        node = parent[parts[-1]]
        if isinstance(node, dict) and node and not recursive:
            raise OSError(f"directory not empty: {path}")
        del parent[parts[-1]]

    def mv(self, src, dst):
        sp, dp = self._parts(src), self._parts(dst)
        if not sp:
            raise ValueError("cannot move /")
        node = self._node(sp)
        try:
            if isinstance(self._node(dp), dict):
                dp = dp + [sp[-1]]
        except FileNotFoundError:
            pass
        if isinstance(node, dict) and dp[:len(sp)] == sp:
            raise ValueError("cannot move a directory into itself")
        parent = self._parent(dp)
        if dp[-1] in parent:
            raise FileExistsError("/" + "/".join(dp))
        del self._node(sp[:-1])[sp[-1]]
        parent[dp[-1]] = node

    def find(self, path, pattern):
        out = []

        def walk(node, prefix):
            for name, child in node.items():
                full = f"{prefix}/{name}"
                if isinstance(child, dict):
                    walk(child, full)
                elif fnmatch.fnmatchcase(name, pattern):
                    out.append(full)

        parts = self._parts(path)
        node = self._node(parts)
        if isinstance(node, dict):
            walk(node, "/" + "/".join(parts) if parts else "")
        elif fnmatch.fnmatchcase(parts[-1], pattern):
            out.append("/" + "/".join(parts))
        return sorted(out)
