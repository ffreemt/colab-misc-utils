# colab miscellaneous utils [![Codacy Badge](https://app.codacy.com/project/badge/Grade/83b7b2cb3ade4589812917f187a8abab)](https://www.codacy.com/gh/ffreemt/colab-misc-utils/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ffreemt/colab-misc-utils&amp;utm_campaign=Badge_Grade)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/clmutils.svg)](https://badge.fury.io/py/clmutils)
Miscellaneous utils mainly intended for use in colab

## Demo: notebooks in Colab
### `git push` from Colab
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1n0agOGg8rBoR0Ld3WAvh20QzXeZZ7xCk?usp=sharing)
### Set up a reverse ssh tunnel for ssh to Colab VM
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1CIstRNIZjKhMqCch-FRyoIoiFjGAOGii?usp=sharing)
in English (I may provide a Chinese version later)


## Installation
```bash
pip install clmutils  # clm: colab-misc
```

## Usage
### Write a private key to `~/.ssh/gh-key`
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
### Set up `github.com` config for `git push`
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
Verify that everything is OK, from a cell
```ipynb
!ssh -o StrictHostKeyChecking=no -T git@github.com
```
If you see something similar to
```bash
Hi your-name! You've successfully authenticated, but GitHub does not provide shell access.
```
you are good to go.

You can now set up `git config global` from a cell, e.g.
```ipynb
!git config --global user.email your-email-address
!git config --global user.name your-github-username
# !ssh-keyscan github.com >> ~/.ssh/known_hosts
```
You are ready to clone your own repo, run your app and generate new data, update the repo and push to `github`.

## Utils planned
* :white_check_mark: `create_file`
  creates a file with given mode, e.g. for `.ssh/id_rsa` or `IdentityFile` in `.ssh/config`

* :white_check_mark: `apppend_content`
 appends some content to a file, e.g., for appended a public key to `.ssh/authorized_keys`

* :white_check_mark: `chmod600`
   `chmod` of a file

*  `reverse_ssh_tunnel`
 sets up a reverse ssh tunnel to a remote host with via autossh

*  More