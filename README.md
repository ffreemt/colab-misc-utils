# colab miscellaneous utils [![Codacy Badge](https://app.codacy.com/project/badge/Grade/83b7b2cb3ade4589812917f187a8abab)](https://www.codacy.com/gh/ffreemt/colab-misc-utils/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ffreemt/colab-misc-utils&amp;utm_campaign=Badge_Grade)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/clmutils.svg)](https://badge.fury.io/py/clmutils)
Miscellaneous utils mainly intended for use in colab

## Installation
```bash
pip install clmutils  # clm: colab-misc
# pip install clmutils -U to update
```
Or clone the repo `https://github.com/ffreemt/colab-misc-utils.git` in Colab/jupyter:
```
!git clone https://github.com/ffreemt/colab-misc-utils.git
%cd colab-misc-utils
!pip install -r requirements.txt
```

## Usage:  with a setting file dotenv/`.env`

1. `setup_git`
    ```python
    from clmutils import setup_git, Settings
    config = Settings()
    setup_git(
      user_name=config.user_name,
      user_email=config.user_email,
      priv_key=config.gh_key
    )
    ```
    Do the usual `git pull`, amend codes and `git push` stuff.

    For more on `Connecting to GitHub with SSH`, refer to  https://docs.github.com/cn/free-pro-team@latest/github/authenticating-to-github/connecting-to-github-with-ssh

2. `setup_ssh_tunnel`
    * Run these lines in Colab
    ```python
    from clmutils import setup_ssh_tunnel, Settings
    config = Settings()
    setup_ssh_tunnel(
      remote_host=config.remote_host,
      remote_user=config.remote_user,
      priv_key=config.cl_key,
      remote_pubkey=config.remote_pubkey
    )
    ```

    * Append the value of `cl_key_pub` in `dotenv/.env` (below) in remote computer's `~/.ssh/authorized_keys`.

    * In the remote computer:
    ```bash
    ssh colab
    ```

`clmutils.Setting` will look for `dotenv` or `.env` in `/content/drive/MyDrive` if google drive is momunted; otherwise it looks for `.env` in the current dir and parents dir.

`dotenv/.env` basically contains the necessary information to setup git for github or ssh tunnel:
  * For git:
      * gh_key: private key
      * user_name/user_email;
  * For reverse ssh tunnel:
      * cl_key/cl_key_pub: private key/public key of Colab
      * remote_pubkey: public_key of the remote computer
      * remote_user: login name

`dotenv/.env` is read by `clmutils.Settin` as follows
```bash
from clmutils import Settings
config = Settings()
# config = Setting(_env_file=file_path)
```
`config` will then have attributes: `config.gh_key, user_name, user_email,
    cl_key, cl_key_pub, remote_pubkey, remote_user`.
If a particular attribute is not assigned a value in `dotenv/.env`, it defaults to empty string (`""`).

`dotenv` or `.env` has the following info and format (lines starting with a `#` are comments):
```bash
# for git
user_email = "...@......"
user_name = "......"
gh_key = "-----BEGIN EC PRIVATE KEY-----
...............................................................9
...............................................................J
K9ztlJBRRAOHh5sPhQ4QpdZH1v1rWeDWIQ==
-----END EC PRIVATE KEY-----
"

# for ssh tunnel
remote_host = "168.138.222.163"
remote_user = "ubuntu"

# colab's private key, to be put in ~/.ssh/id_ed25519
# or as specified in ~/.ssh/config
cl_key = "-----BEGIN OPENSSH PRIVATE KEY-----
.....................................................................W
QyNTUxOQAAACCClZGt/9ibAd9oxuWcfuSjnw0ERuY68/1QiirdrrtngQAAAJDlRQSF5UUE
hQAAAAtzc2gtZWQyNTUxOQAAACCClZGt/9ibAd9oxuWcfuSjnw0ERuY68/1QiirdrrtngQ
.....................................................................f
DQRG5jrz/VCKKt2uu2eBAAAACWZvci1jb2xhYgECAwQ=
-----END OPENSSH PRIVATE KEY-----
"

# to be put in remote computer's ~/.ssh/autorized_keys
cl_key_pub = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIKVka3/2JsB32jG5Zx+5KOfDQRG5jrz/VCKKt2uu2eB colab-key"

# to be put in colab's ~/.ssh/authorized_keys
remote_pubkey = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIE60sowZ4M0MA5nTGIH1RN54zERTuWSddFKqyeWZzaKv for-colab"
```

## Usage: withtout dotenv/`.env`
### Set up `github` with ssh using `clmutils.setup_git`

For manually setting up github with ssh, refer to
[https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/connecting-to-github-with-ssh](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/connecting-to-github-with-ssh)

Assume you configure git as follows:
```bash
git config --global user.email your-email-address
git config --global user.name your-github-username
```

With `clmutils`, you'd do:
```python
from clmutils import setup_git`

user_email = "your-email-address"
user_name = "your-github-username"
gh_key = \
"""
-----BEGIN EC PRIVATE KEY-----
MH.............................................................9
AwEHoUQDQgAEoLlGQRzIVHYw3gvC/QFw3Ru45zGawaBaCq6jTqdyH2Kp8zIB3TdJ
K9ztlJBRRAOHh5sPhQ4QpdZH1v1rWeDWIQ==
-----END EC PRIVATE KEY-----
""".strip() + "\n"

setup_git(user_email=user_email, user_name=user_name, priv_key=gh_key)
```
You then upload the `public key` for `gh_key` to [https://github.com/settings/keys](https://github.com/settings/keys).

Refer to Step 2 [https://support.cloudways.com/using-git-command-line-ssh/](https://support.cloudways.com/using-git-command-line-ssh/) for how to generate a private/public key pair. You can also use clmutils.gen_keypair to do that in Python.

### Alternatively, set up `github` with ssh in 4 steps

1. Write a private key to `~/.ssh/gh-key`
```python
from clmutils import create_file
gh_key = \
"""
-----BEGIN EC PRIVATE KEY-----
MH.............................................................9
AwEHoUQDQgAEoLlGQRzIVHYw3gvC/QFw3Ru45zGawaBaCq6jTqdyH2Kp8zIB3TdJ
K9ztlJBRRAOHh5sPhQ4QpdZH1v1rWeDWIQ==
-----END EC PRIVATE KEY-----
""".strip() + "\n"
# Do not remove .strip() + "\n"
# the private key is very picky about format

create_file(gh_key, dest="~/.ssh/gh-key")
```
2. Set up `github.com` config for `git push`
```python
from clmutils import append_content
config_github_entry = \
"""
Host github.com
   HostName github.com
   User git
   IdentityFile ~/.ssh/gh-key
"""
append_content(config_github_entry, dest="~/.ssh/config")
```
3. Verify that everything is OK, from a cell
```ipynb
!ssh -o StrictHostKeyChecking=no -T git@github.com
```
If you see something similar to
```bash
Hi your-name! You've successfully authenticated, but GitHub does not provide shell access.
```
you are good to go.

4. `git config --global`
You can now set up `git config global` from a cell, e.g.
```ipynb
!git config --global user.email your-email-address
!git config --global user.name your-github-username
# !ssh-keyscan github.com >> ~/.ssh/known_hosts
```
You are ready to clone your own repo, run your app and generate new data, update the repo and push to `github`.

## Utils planned

* :white_check_mark: `setup_git` sets up `git` for `github.com`

* :white_check_mark:  `reverse_ssh_tunnel`
 sets up a reverse ssh tunnel to a remote host with via autossh

* Auxiliary utils
  * :white_check_mark: `create_file`
    creates a file with given mode, e.g. for `.ssh/id_rsa` or `IdentityFile` in `.ssh/config`

  * :white_check_mark: `apppend_content`
   appends some content to a file, e.g., for appended a public key to `.ssh/authorized_keys`

  * :white_check_mark: `chmod600`
     `chmod` of a file

  * :white_check_mark: `gen_keypair` generates private/public key pair.

  * :white_check_mark: `run_cmd` wraps
      `subprocess.check_output`

  * :white_check_mark: `run_cmd1` wraps
      `subprocess.Popen`

  * :white_check_mark: `check_running`  shows running processes with names containings a certain patter; based on `psutil.Proceess()'s `cmdline` and `status`

## Demo: notebooks in Colab

### git push from Colab: one line (`setup_git()`)
```
!pip install clmutils
from clmutils import setup_git
gh_key = """..."""
user_name = "..."
user_email = "..."
setup_git(setup_git(user_email=user_email, user_name=user_name, priv_key=gh_key)
```
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1u-eNhJpG64ajP-fPO3jtSQzdlAMSxtwE?usp=sharing#scrollTo=svB7ci6VzLnl)

### `git push` from Colab in several steps
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1n0agOGg8rBoR0Ld3WAvh20QzXeZZ7xCk?usp=sharing) (in Chinese, shouldn't be too difficult to follow without knowing any Chinese though, just click through :smiley:)
### Reverse ssh tunnel for ssh to Colab VM
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1CIstRNIZjKhMqCch-FRyoIoiFjGAOGii?usp=sharing?usp=sharing)
in English (I may provide a Chinese version later)
