"""Check a string in running process's name."""
# pylint

import psutil


def check_running(name: str) -> bool:
    """Check a string in running process's name."""
    for elm in psutil.process_iter():
        try:
            cmdline = " ".join(elm.cmdline())
        except Exception:
            cmdline = ""
        if name in cmdline and elm.status() in ["running"]:
            return True
    return False
