"""Create a file."""
from typing import Optional, Union

from pathlib import Path
import re

# import subprocess as sp  # noqa: F401
from logzero import logger

from .chmod600 import chmod600


# fmt: off
def create_file(
        content: str = "",
        dest: Union[Path, str] = Path("~/.ssh/gh-key").expanduser(),
        overwrite: bool = False,
        setmode: bool = False,  # if True, chmode600
) -> Optional[Path]:
    # fmt: on
    """
    Create a file if it does not exist.

    Overwrite existing file only if set to True.
    Set mode to 600 if setmode is True (default false)
    """
    # unticipate people from another world
    pattern = re.compile(r"\$home|%userprofile%?", re.IGNORECASE)
    if isinstance(dest, str):
        dest = pattern.sub("~", dest)
    else:
        _ = dest.__str__()
        dest = pattern.sub("~", _)
    dest = Path(dest).expanduser().resolve()

    if dest.exists() and overwrite is False:
        logger.warning(" %s exists and overwrite set to %s", dest, overwrite)
        logger.warning("Will not proceed")
        return dest
    p_dir = dest.parent

    try:
        p_dir.mkdir(parents=True, exist_ok=True)
    except Exception as exc:
        logger.error("p_dir.mkdir exc: %s", exc)
        logger.warning("Will not proceed")
        return None

    try:
        dest.write_text(content, encoding="utf8")
    except Exception as exc:
        logger.error("dest.write_text exc: %s", exc)
        return None

    if setmode:
        chmod600(dest)

    return dest
