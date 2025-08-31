if command -v bat >/dev/null
    function cat --wraps bat
        command bat $argv
    end
end

# vim: sts=4 sw=4 et
