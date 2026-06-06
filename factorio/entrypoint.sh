#!/bin/sh

readonly FACTORIO_BIN=/opt/factorio/bin/x64/factorio

if ! [ -f "/data/world.zip" ]; then
    $FACTORIO_BIN --create /data/world.zip
fi

if [ $# -ge 1 ]; then
    exec $FACTORIO_BIN "$@"
fi

exec $FACTORIO_BIN --start-server /data/world.zip

# vim: sts=4 sw=4 et
