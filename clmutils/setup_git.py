"""Set up ssh config and git global email/name.

pip install clmutils
colan notebooks https://github.com/ffreemt/colab-misc-utils

pubkey
git config --global user.email colab.misc.utils@gmail.com
git config --global user.name clmutils
git config --global --list

# colab-misc.utils
Host github-clmutils  # default github.com
   HostName github.com
   User git
   # IdentityFile ~/.ssh/id_rsa_work_user1
   # IdentityFile ~/.ssh/id_aliyun
   IdentityFile ~/.ssh/clmutils_id_ed25519
"""
# pylint: disable=too-many-arguments, too-many-locals, too-many-branches, too-many-statements
from typing import Optional, Union

from pathlib import Path
import re
import chardet

from logzero import logger

from .create_file import create_file
from .append_content import append_content
from .run_cmd import run_cmd
from .run_cmd1 import run_cmd1

CLMUTISL_EMAIL = "colab.misc.utils@gmail.com"
CLMUTISL_USER_NAME = "clmutils"
CLMUTISL_PRIV_KEY = """-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACCZC8DOrHpisdDq66KFCniUxdUG0e3VO/x+LDW3u3BBPQAAAJBmk3z1ZpN8
9QAAAAtzc2gtZWQyNTUxOQAAACCZC8DOrHpisdDq66KFCniUxdUG0e3VO/x+LDW3u3BBPQ
AAAEAKaAKiJSYphKjds5DFaKPdxaIVV6kTs4icy2F+VTxpkZkLwM6semKx0OrrooUKeJTF
1QbR7dU7/H4sNbe7cEE9AAAAC2NsbXV0aWxzLWdoAQI=
-----END OPENSSH PRIVATE KEY-----
"""


# fmt: off
def setup_git(
        user_email: str = CLMUTISL_EMAIL,
        user_name: str = CLMUTISL_USER_NAME,
        priv_key: Union[str, Path] = CLMUTISL_PRIV_KEY,
        identity_file: Union[str, Path] = "",  # default f"~/.ssh/gh_{user_name}"
        set_global: bool = True,
        host: str = "github.com",
        overwrite: bool = False,  # do not overwrite identity_file
) -> Optional[str]:
    # fmt: on
    """
    Set up ssh config and git global email/name for git.

    Setting up multiple git accounts is possible by setting host (if you know what you are doing), e.g.
        setup_git(..., set_global=False, host="git4work")
    you can then set up
        git config --local user.email
        git config --local user.name
    in a git directory to use a different git account
    """
    if isinstance(identity_file, str) and not identity_file.strip():  # default to f"gh_{user_name}"
        identity_file = f"~/.ssh/gh_{user_name}"

    def check(arg: str) -> str:
        try:
            arg = arg.strip()
        except Exception as exc:
            logger.error("%s: %s", arg, exc)
            raise SystemExit(exc)
        if not user_email:
            raise SystemExit(f"Empty {arg}, cant continue")
        return arg

    if isinstance(priv_key, Path):
        priv_key_path = priv_key.expanduser()
        if not priv_key_path.exists():
            logger.error(" %s does not exist, cant continue")
            raise SystemExit(1)

        try:
            _ = priv_key_path.read_bytes()
            encoding = chardet.detect(_).get("encoding")
            priv_key = priv_key_path.read_text(encoding)
        except Exception as exc:
            logger.error(" priv_key_path.read_text exc: %s", exc)
            raise SystemExit(1)

    for arg in [user_email, user_name, priv_key]:
        arg = check(arg)

    # attach a needed "\n"
    priv_key = priv_key.strip() + "\n"

    if isinstance(identity_file, str):
        identity_file = identity_file.strip()

    # convert to str for IdentityFile entry in ~/.ssh/config
    try:
        identity_file_str = Path(identity_file).expanduser().as_posix()
    except Exception as exc:
        logger.error(" identity_file %s cant be converted to str, exc: %s", identity_file, exc)
        raise

    # create identity_file
    create_file(
        priv_key,
        identity_file,
        overwrite=overwrite,
        setmode=True  # chmod 600
    )

    # set up an entry in ~/.ssh/config
    config_entry = f"""
Host {host}
   HostName github.com
   User git
   IdentityFile {identity_file_str}
    """

    # check for duplicate
    entry_exits = False
    if Path("~/.ssh/config").expanduser().exists():
        fpath = Path("~/.ssh/config").expanduser()
        try:
            _ = fpath.read_bytes()
            encoding = chardet.detect(_).get("encoding")
            _ = fpath.read_text(encoding=encoding)
        except Exception as exc:
            logger.error("Reading %s exc: %s", fpath, exc)
            raise
        if re.findall(rf"{identity_file_str}", _):
            entry_exits = True
        # write to ~/.ssh/config if the entry does not already exist
        if not entry_exits:
            append_content(config_entry, "~/.ssh/config")
    else:
        append_content(config_entry, "~/.ssh/config")

    # set up git config --global if set_global is True
    if set_global:
        run_cmd(f"git config --global user.email {user_email}")
        run_cmd(f"git config --global user.name {user_name}")

        # validate setup
        out_err = run_cmd1("ssh -T git@github.com -o StrictHostKeyChecking=no")

        if "successfully authenticated" in str(out_err):
            logger.debug(str(out_err))
            logger.info("\n\t Congrats! You are good to go. ")
        else:
            # out_err = run_cmd1("ssh -T git@github.com -o StrictHostKeyChecking=no -v")
            # out = out_err[0] if isinstance(out_err[0], str) else ""
            # err = out_err[1] if isinstance(out_err[1], str) else ""
            # logger.debug(out + "\n" + err)
            logger.warning(
                "\n There appears to be some problem."
                "\nYou may wish to exam the debug messages above, "
                "\nfix it and give it another try."
            )
