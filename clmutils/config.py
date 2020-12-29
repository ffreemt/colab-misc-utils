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
    cl_key: str = ""
    cl_key_pub: str = ""
    gh_key: str = ""

    class Config:
        """Setting config."""

        # in colab  and drive mounted
        _ = "/content/drive/MyDrive"
        if "google.colab" in sys.modules and Path(_).is_dir():
            envfile = ""
            _ = "/content/drive/MyDrive/dotenv"
            if Path(_).is_file():
                envfile = _
            elif Path("/content/drive/MyDrive/.env").is_file():
                envfile = "/content/drive/MyDrive/.env"
        
        # neither exists, try cwd and upper
        if not envfile:
            # env_file = ".env"
            env_file = dotenv.find_dotenv()
