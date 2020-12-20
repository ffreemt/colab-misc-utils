"""Chmod 600/666."""
from typing import Union

from pathlib import Path
from logzero import logger


# fmt: off
def chmod600(
        fpath: Union[str, Path] = Path("~/.ssh/id_rsa").expanduser(),
        mode: int = 0o600,
) -> bool:
    # fmt: on
    """Chmod 600.

    Can set to other mode, e.g. chmod600(mode=0o666)
    """
    fpath = Path(fpath)
    if fpath.exists():
        _ = fpath.stat().st_mode
        try:
            fpath.chmod(mode)
            _ = fpath.stat().st_mode
            logger.info("%s mode set to %s", fpath.as_posix(), oct(_))
            return True
        except Exception as exc:
            logger.error(" chmod exc: %s", exc)
            return False
    else:
        return False
