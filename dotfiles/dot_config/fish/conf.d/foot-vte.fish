if status is-interactive
    and [ -z $WAYLAND_DISPLAY ]
    and [ $XDG_VTNR -ge 3 ]
    and [ $(hostnamectl hostname) = "yggdrasil" ]

    # --fullscreen to remove black bar at bottom of screen
    # font size 14 to more closely match the default vte
    exec cage -s -- foot --fullscreen --font=monospace:size=14 2>/dev/null
end

    
# vim: sts=4 sw=4 et
