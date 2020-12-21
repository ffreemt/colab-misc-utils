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
    try:
        keytype = str(keytype).lower().strip()
    except Exception as exc:
        logger.error("str*keytype) exc: %s", exc)
        keytype = "rsa"

    if keytype not in ["dsa", "ecdsa", "ed25519", "rsa"]:
        keytype = "rsa"

    if dest is None:
        dest = f"~/.ssh/id_{keytype}"
    try:
        dest = Path(dest).expanduser().resolve()
    except Exception as exc:
        logger.error("Path(dest).expanduser().resolve() exc: %s", exc)
        dest = f"~/.ssh/id_{keytype}"
        dest = Path(dest).expanduser().resolve()

    dest_pub = Path(f"{dest}.pub")

    dest_str = dest.as_posix().__str__()

    if Path(dest).exists():
        logger.warning(" %s already exists", dest)
        logger.info("We try to retrieve the corresponding public key")
        if dest_pub.exists():
            try:
                pub_key = dest_pub.read_text("utf8").strip()
            except Exception as exc:
                logger.error(" dest_pub.read_text exc: %s", exc)
                return ""
            return pub_key

        cmd = f"ssh-keygen -f {dest_str} -y"
        try:
            logger.info("cmd: %s", cmd)
            pub_key = run_cmd(cmd)
        except Exception as exc:
            logger.error("run_cmd(%s) exc: %s", cmd, exc)
            return ""

        if isinstance(pub_key, str):
            pub_key = pub_key.strip()
        return "" if pub_key is None else pub_key

        # return pub_key or ""

    cmd = f"ssh-keygen -t {keytype} -f {dest_str} -N '' -C 'colab-key' "
    try:
        logger.info("cmd: %s", cmd)
        run_cmd(cmd)
    except Exception as exc:
        logger.error("%s exc: %s ", cmd, exc)
        return ""

    try:
        pub_key = dest_pub.read_text("utf8")
    except Exception as exc:
        logger.error("dest_pub.read_text exc: %s", exc)
        pub_key = ""

    if isinstance(pub_key, str):
        pub_key = pub_key.strip()
    return pub_key
