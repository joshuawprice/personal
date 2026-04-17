#!/bin/sh

# For an explanation of why this exists, see the makefile.

set -eu

uv sync --locked

ln -sf /usr/bin/python3.14 .venv/bin/python
ln -sf python .venv/bin/python3
ln -sf python .venv/bin/python3.14

sed -i 's:home = /usr/local/bin:/usr/bin:' .venv/pyvenv.cfg
