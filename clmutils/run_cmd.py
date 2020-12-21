"""Run cmd in subprocess.check_output.

With some error checking.
"""
from typing import List, Union

import subprocess as sp
from shlex import split

from logzero import logger


def run_cmd(cmd: Union[str, List[str]]) -> Union[str, bool]:
    """Run cmd in subprocess.check_output.

    With some error checking.
    """
    if isinstance(cmd, str):
        cmd = split(cmd)
    try:
        _ = sp.check_output(cmd, encoding="utf8", stderr=sp.STDOUT)
        if _ is None:
            _ = ""
        return _
    except Exception as exc:
        # logger.exception(exc)
        logger.info("%s", " ".join(cmd))
        logger.error("\n%s", exc)
        return False
