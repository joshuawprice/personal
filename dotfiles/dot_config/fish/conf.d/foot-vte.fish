if status is-interactive
    and [ -z $WAYLAND_DISPLAY ]
    and set -q XDG_VTNR
    and [ $XDG_VTNR -ge 3 ]

    if ! command -v cage >/dev/null
        echo "`cage' not installed, falling back to tty." >&2
        return
    end

    if ! command -v foot >/dev/null
        echo "`foot' not installed, falling back to tty." >&2
        return
    end

    # -s            allow VT switching
    # --fullscreen  enables padding, removing black bar at bottom of display
    exec cage -s -- foot --fullscreen --override=dpi-aware=yes --override=mouse.hide-when-typing=yes 2>/dev/null
end

    
# vim: sts=4 sw=4 et
