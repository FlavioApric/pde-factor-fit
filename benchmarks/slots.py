"""Machine-wide CPU slots shared by every corpus run of every session (S-LEARNED parallel build).

A slot is a lock file `slot<i>` in one directory, created exclusively and holding the owner's pid (the
scheduler that spawned the worker). A slot whose owner is dead is reclaimed, so a killed scheduler
never leaks slots. Total slots: env LL_SLOTS (default 10 of 12 threads, the user's choice).

Priority (S-LEARNED PM): a reservation file `reserve.json` = {"tag": "<job>", "n": k} keeps k slots for
the processes whose env LL_SLOT_TAG equals that tag; others may only take slots beyond the unfilled
reservation. `python slots.py reserve <tag> <k>` / `python slots.py release-reserve` / `python slots.py show`.

    with slots.Pool() as pool:
        i = pool.try_acquire()   # None when all slots are taken
        ...
        pool.release(i)
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

DIR = Path(os.environ.get("LL_SLOTS_DIR", Path(tempfile.gettempdir()) / "pdefactor_cpu_slots"))
TOTAL = int(os.environ.get("LL_SLOTS", "10"))


def _alive(pid):
    if pid == os.getpid():
        return True
    if sys.platform == "win32":
        import ctypes

        k = ctypes.windll.kernel32
        h = k.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
        if not h:
            return False
        code = ctypes.c_ulong()
        k.GetExitCodeProcess(h, ctypes.byref(code))
        k.CloseHandle(h)
        return code.value == 259  # STILL_ACTIVE
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def _owners(directory, total):
    out = {}
    for i in range(total):
        try:
            parts = (Path(directory) / f"slot{i}").read_text().split()
        except OSError:
            continue
        if parts:
            out[i] = (int(parts[0]) if parts[0].isdigit() else 0, parts[1] if len(parts) > 1 else "")
    return out


class Pool:
    def __init__(self, total=TOTAL, directory=DIR, tag=None):
        self.total, self.dir, self.held = total, Path(directory), set()
        self.tag = os.environ.get("LL_SLOT_TAG", "") if tag is None else tag
        self.dir.mkdir(parents=True, exist_ok=True)

    def _allowed(self):
        try:
            res = json.loads((self.dir / "reserve.json").read_text())
        except (OSError, ValueError):
            return True
        if not res.get("n") or res.get("tag") == self.tag:
            return True
        own = _owners(self.dir, self.total)
        busy = sum(1 for pid, _ in own.values() if pid and _alive(pid))
        mine = sum(1 for pid, t in own.values() if t == res["tag"] and pid and _alive(pid))
        return self.total - busy - max(0, int(res["n"]) - mine) > 0

    def try_acquire(self):
        if not self._allowed():
            return None
        for i in range(self.total):
            f = self.dir / f"slot{i}"
            try:
                fd = os.open(f, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError:
                try:
                    pid = int((f.read_text().split() or ["0"])[0])
                except (OSError, ValueError):
                    continue  # being written right now
                if pid and not _alive(pid):
                    try:
                        f.unlink()
                    except OSError:
                        pass
                continue
            os.write(fd, f"{os.getpid()} {self.tag}".strip().encode())
            os.close(fd)
            self.held.add(i)
            return i
        return None

    def release(self, i):
        if i in self.held:
            self.held.discard(i)
            try:
                (self.dir / f"slot{i}").unlink()
            except OSError:
                pass

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        for i in list(self.held):
            self.release(i)


if __name__ == "__main__":
    cmd = sys.argv[1:] or ["show"]
    DIR.mkdir(parents=True, exist_ok=True)
    if cmd[0] == "reserve":
        (DIR / "reserve.json").write_text(json.dumps(dict(tag=cmd[1], n=int(cmd[2]))))
    elif cmd[0] == "release-reserve":
        (DIR / "reserve.json").unlink(missing_ok=True)
    for i, (pid, t) in sorted(_owners(DIR, TOTAL).items()):
        print(f"slot{i}: pid {pid} {t} {'alive' if _alive(pid) else 'dead'}")
    r = DIR / "reserve.json"
    print("reserve:", r.read_text() if r.exists() else "none")
