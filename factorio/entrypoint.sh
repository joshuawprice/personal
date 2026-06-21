#!/bin/sh

readonly FACTORIO_BIN=/opt/factorio/bin/x64/factorio

if ! [ -f "/data/world.zip" ]; then
    $FACTORIO_BIN --create /data/world.zip
fi

if [ $# -ge 1 ]; then
    exec $FACTORIO_BIN "$@"
fi

# Optionally enable whitelist if file exists.
if [ -f "/config/server-whitelist.json" ]; then
    echo "Whitelist file found. Enabling whitelist."
    FLAGS="$FLAGS --use-server-whitelist --server-whitelist /config/server-whitelist.json"
fi

exec $FACTORIO_BIN --start-server /data/world.zip $FLAGS

# vim: sts=4 sw=4 et
