"""Config."""
# pylint: disable=too-few-public-methods

import sys
from pathlib import Path
from pydantic import BaseSettings
import dotenv


class Settings(BaseSettings):
    """Settings."""

    remote_host: str = ""
    remote_user: str = ""
    remote_pubkey: str = ""
    cl_key: str = ""
    cl_key_pub: str = ""
    gh_key: str = ""

    class Config:
        """Setting config."""

        # in colab  and drive mounted
        env_file = ""
        _ = "/content/drive/MyDrive"
        if "google.colab" in sys.modules and Path(_).is_dir():
            _ = "/content/drive/MyDrive/dotenv"
            if Path(_).is_file():
                env_file = _
            elif Path("/content/drive/MyDrive/.env").is_file():
                env_file = "/content/drive/MyDrive/.env"

        # neither exists, try .env in cwd and upper dirs
        if not env_file:
            # env_file = ".env"
            env_file = dotenv.find_dotenv()
