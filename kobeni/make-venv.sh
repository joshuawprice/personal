#!/bin/sh

# For an explanation of why this exists, see the makefile.

set -eu

uv sync --locked

uv run slice2py --output-dir kobeni/mumble kobeni/mumble/MumbleServer.ice

ln -sf /usr/bin/python3.13 .venv/bin/python
ln -sf python .venv/bin/python3
ln -sf python .venv/bin/python3.13

sed -i 's:home = /usr/local/bin:/usr/bin:' .venv/pyvenv.cfg
