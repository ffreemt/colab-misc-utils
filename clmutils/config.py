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

    class Config:
        """Setting config."""

        _ = "/content/drive/MyDrive/dotenv"
        # in colab, if google drive mounted
        if "google.colab" in sys.modules and Path(_).is_file():
            env_file = _
        else:
            # env_file = ".env"
            env_file = dotenv.find_dotenv()
