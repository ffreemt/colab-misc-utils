"""Execute cmd via subprocess.Popen."""
from typing import Optional, Tuple, Union

import shlex
import subprocess as sp
from logzero import logger


# fmt: off
def run_cmd1(
        cmd: Union[str, list],
        inp: Optional[str] = None,
        shell: bool = False,
) -> Tuple[Optional[str], Optional[str]]:
    # fmt: on
    """Execute cmd via subprocess.Popen.

    inp: interactive input to cmd.
    """
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)

    # fmt: off
    proc = sp.Popen(
        cmd,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
        encoding="utf8",
        shell=shell,
    )
    # fmt: on
    out, err = proc.communicate(inp)
    logger.info("%s...\n%s", " ".join(cmd), out)
    if err:
        logger.error("%s,", err)
    return out, err
