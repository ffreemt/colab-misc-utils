"""Set up ssh tunnel.

remote_user
remote_ip
local_user
priv_key
"""
# pylint: disable=too-many-arguments

from typing import (
    Optional,
    Union,
)

from pathlib import Path
from logzero import logger

from clmutils.create_file import create_file
from clmutils.chmod600 import chmod600
from clmutils.append_content import append_content
from clmutils.run_cmd import run_cmd
from clmutils.run_cmd1 import run_cmd1


# fmt: off
def setup_ssh_tunnel(
        remote_user: str,
        remote_host: str,  # ip or domainname
        remote_pubkey: str,
        priv_key: Optional[str] = None,  # use existing priv_key_file
        local_user: str = "root",
        priv_key_file: Union[str, Path] = "~/.ssh/id_ed25519",
        overwrite: bool = False,
) -> None:
    # fmt: on
    """Set up ssh tunnel."""
    remote_ip = remote_host
    # authorized_keys
    try:
        remote_pubkey = remote_pubkey.strip() + "\n"
    except Exception as exc:
        logger.error("Something weird happened with remote_pubkey, exc: %s", exc)
        logger.info("It probably makes no sense to continue, exiting.")
        raise SystemExit(1)
    try:
        append_content(remote_pubkey, "~/.ssh/authorized_keys")
    except Exception as exc:
        logger.warning(" append_content(remote_pubkey) exc: %s", exc)
        logger.info("We ll continue tho. You can manually append the public key to ~/.ssh/authorized_keys")

    try:
        priv_key = priv_key.strip() + "\n"
    except Exception as exc:
        logger.error("Something weird happened with priv_key, exc: %s", exc)
        logger.info("It probably makes no sense to continue, exiting.")
        raise SystemExit(1)

    if not priv_key:
        if Path(priv_key_file).expanduser().is_file():
            chmod600(priv_key_file)
        else:
            logger.error(" priv_key not provided AND %s is not a file or does not exist, cant continue", priv_key_file)
            raise SystemExit(1)
    else:
        if Path(priv_key_file).expanduser().is_file() and overwrite:
            logger.warinng(" priv_key provided yet %s also exists", priv_key_file)
            logger.info(" How should it be done?, existing")
            raise SystemExit(1)

        create_file(priv_key, priv_key_file, setmode=True)

    # testing setup
    # !ssh -T ubuntu@{remote_ip} -o StrictHostKeyChecking=no hostname

    # try once, update ~/.ssh/known_hosts
    out, err = run_cmd1(f"ssh -nT ubuntu@{remote_ip} -o StrictHostKeyChecking=no -o BatchMode=yes echo Tested OK")

    out, err = run_cmd1(f"ssh -nT ubuntu@{remote_ip} echo Tested OK 2x")
    # ('Tested OK 2x\n', ''): success
    # ('', 'Permission denied (publickey).\n') failed

    if err:
        logger.warning("Colab->remote ssh Not properly setup: %s", err)
        raise SystemExit(1)

    logger.info("Looks good, able to connect: %s", out)

    # Install sshd/autossh and start sshd services
    run_cmd("apt install openssh-server")
    run_cmd("apt install autossh")
    run_cmd("/etc/init.d/ssh start")

    # start reverse tunnerl using autossh
    cmd = f"autossh -f -M 0 {remote_user}@{remote_ip} -CN -R 2222:127.0.0.1:22 -o StrictHostKeyChecking=no "
    cmd += "-o ExitOnForwardFailure=yes -o ServerAliveInterval=10 -o ServerAliveCountMax=50 "
    run_cmd1(cmd)

    # assembly an entry in ~/.ssh/config for remote
    config_entry = f"""
Host colab
  HostName 127.0.0.1
  User {local_user}
  Port 2222
  StrictHostKeyChecking no
  IdentityFile ~/.ssh/id_rsa
  # or  IdentityFile ~/.ssh/for-colab-key
"""
    logger.info("Paste this to remote computer's ~/.ssh/config\n%s", config_entry)

    logger.info("In the remote computer, issue this command:\nssh colab")

    logger.info(" Enjoy! ")
