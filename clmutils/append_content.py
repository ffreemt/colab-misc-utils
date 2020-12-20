"""Create a file."""
from typing import Optional, Union

from pathlib import Path
import re

# import subprocess as sp  # noqa: F401
import chardet
from logzero import logger

from clmutils import create_file


# fmt: off
def append_content(
        content: str = "",
        dest: Union[Path, str] = Path("~/.ssh/authorized_keys").expanduser(),
) -> Optional[Path]:
    # fmt: on
    """
    Append content to a file.

    Create the file if it does not exist.
    """
    # unticipate people from another world
    patt = re.compile(r"\$home|%userprofile%?", re.IGNORECASE)
    if isinstance(dest, str):
        dest = patt.sub("~", dest)
    else:
        _ = dest.__str__()
        dest = patt.sub("~", _)
    dest = Path(dest).expanduser().resolve()

    if not dest.exists():
        try:
            create_file("", dest)
        except Exception as exc:
            logger.error("create_file exc: %s", exc)

    # detect encoding and read
    _ = dest.read_bytes()
    encoding = chardet.detect(_).get("encoding")
    c_content = Path(dest).read_text(encoding)

    # attach content and write back in utf8
    _ = f"{c_content}\n{content}"
    try:
        Path(dest).write_text(_, "utf8")
    except Exception as exc:
        logger.error("write_text exc: %s", exc)
        return None

    return dest
