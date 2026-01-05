

if status is-interactive
    # Disable the default fish greeting
    set fish_greeting

    if command -v starship >/dev/null
        starship init fish | source
    else
        echo "`starship' not installed, falling back to default prompt." >&2
    end
end

# vim: sts=4 sw=4 et
