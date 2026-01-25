if ! status is-interactive
    return
end

if ! command -v starship >/dev/null
    echo "`starship' not installed, falling back to default prompt." >&2
    return
end

starship init fish | source

# vim: sts=4 sw=4 et
