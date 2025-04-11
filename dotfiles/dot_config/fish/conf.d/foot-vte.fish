if status is-interactive
    and [ -z $WAYLAND_DISPLAY ]
    and [ $XDG_VTNR -ge 3 ]

    if [ $(hostnamectl hostname) = "yggdrasil" ]
        set font_size 14
    else if [ $(hostnamectl hostname) = "muspelheim" ]
        set font_size 20
    end

    # --fullscreen to remove black bar at bottom of screen
    # font size 14 to more closely match the default vte
    exec cage -s -- foot --fullscreen --override=mouse.hide-when-typing=yes --font=monospace:size=$font_size 2>/dev/null
end

    
# vim: sts=4 sw=4 et
