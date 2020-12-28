"""Set up ssh tunnel.

remote_user
remote_ip
local_user
priv_key
"""
# pylint

from pathlib import Path


# fmt: off
def setup_ssh_tunnel(
        remote_ip: str,
        priv_key: str,
        remote_user: str,
        local_user: str = "root",
):
    # fmt: on
    """Set up ssh tunnel."""
