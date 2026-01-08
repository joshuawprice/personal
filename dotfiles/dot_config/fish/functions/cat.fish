# This file is sourced either on first tab completion, or when the command itself is run.
# Warn once if the command is not installed.
if ! command -v bat >/dev/null
    echo -n "`bat' not installed, falling back to cat." >&2

    # If this file is sourced by tab completion, the entire commandline gets
    # broken by the echo above. Therefore go down the amount needed, and
    # reprint it.
    for i in $(seq 1 $(fish_prompt | string split \n | count))
        echo ""
    end
    commandline -f repaint

    return
end

function cat --wraps bat
    command bat $argv
end

# vim: sts=4 sw=4 et
