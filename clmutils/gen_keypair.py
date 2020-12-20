"""Generaete keypairs of type keytype using ssh-keygen.

Write to dest if provided, otherwise write to
~/.ssh/id_{keytype} and ~/.ssh/id_{keytype}.pub
"""
from typing import Optional, Union
from pathlib import Path
from logzero import logger

from .run_cmd import run_cmd


# fmt: off
def gen_keypair(
        dest: Optional[Union[str, Path]] = None,
        keytype: str = "rsa",
) -> Union[str, bool]:
    # fmt: on
    """Generae a keypair of keytype using ssh-keygen.

    Write to dest if provided, otherwise write to
    ~/.ssh/id_{keytype} and ~/.ssh/id_{keytype}.pub

    keytype: dsa | ecdsa | ed25519 | rsa

    return pub
    """
    if dest is None:
        dest = Path(f"~/.ssh/id_{keytype}").expanduser().resolve()
    if keytype not in ["dsa", "ecdsa", "ed25519", "rsa"]:
        keytype = "rsa"

    dest = Path(dest).expanduser().resolve()
    dest_pub = Path(f"{dest}.pub")

    if Path(dest).exists():
        logger.warning(" %s already exists", dest)
        logger.info("We try to retrieve the corresponding public key")
        if dest_pub.exists():
            try:
                pub_key = dest_pub.read_text("utf8")
            except Exception as exc:
                logger.error(" dest_pub.read_text exc: %s", exc)
                return ""
            return pub_key

        cmd = f"ssh-keygen -f {dest.as_posix()} -y"
        try:
            pub_key = run_cmd(cmd)
        except Exception as exc:
            logger.error(f"run_cmd(%s) exc: %s", cmd, exc)
            return ""
        return "" if pub_key is None else pub_key
        # return pub_key or ""

    cmd = f"""ssh-keygen -t {keytype} -f {dest}" -N"" -C"colab-key" """
    try:
        run_cmd(cmd)
    except Exception as exc:
        logger.error("%s exc: %s ", cmd, exc)
        return ""

    try:
        pub_key = dest_pub.read_text("utf8")
    except Exception as exc:
        logger.error("dest_pub.read_text exc: %s", exc)
        pub_key = ""
    return pub_key
