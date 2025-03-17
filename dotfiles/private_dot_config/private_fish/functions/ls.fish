if command -v eza >/dev/null
    function ls --wraps eza
        command eza --icons $argv
    end
else
    function ls --wraps ls
        command ls --color=auto
    end
end

# vim: sts=4 sw=4 et
