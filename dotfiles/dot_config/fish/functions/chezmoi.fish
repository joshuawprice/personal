function chezmoi --wraps chezmoi
    if [ $argv[1] = cd ]
        cd $(command chezmoi source-path)
    else
        command chezmoi $argv
    end
end


# vim: sts=4 sw=4 et
