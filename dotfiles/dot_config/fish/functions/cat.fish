function cat --wraps bat
    # When fish is autoloading the completion for cat, it actually runs the
    # cat command, inadvertently running this very function.
    # To avoid this counting as the first invocation, test for it and just
    # return normal cat.
    #
    # This appears to return "fish" when in the completions/ file, but cat
    # otherwise when invoking the cat command.
    if [ $(status current-command) = "fish" ]
        command cat $argv
        return
    end

    if command -q bat
        command bat $argv
        return
    end

    if not set -q __cat_bat_not_found
        set -g __cat_bat_not_found 0
        echo "`bat' not found, falling back to cat." >&2
    end

    command cat $argv
end


# vim: sts=4 sw=4 et
