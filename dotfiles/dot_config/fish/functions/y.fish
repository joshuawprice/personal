# Yazi support for changing cwd on exit.
# Changes when q is used to quit. Q can be used to return to original position.
function y --wraps yazi
	if ! command -v yazi >/dev/null
		echo "`yazi' not installed."
		return
	end
	set tmp (mktemp -t "yazi-cwd.XXXXXX")
	yazi $argv --cwd-file="$tmp"
	if read -z cwd < "$tmp"; and [ -n "$cwd" ]; and [ "$cwd" != "$PWD" ]
		builtin cd -- "$cwd"
	end
	rm -f -- "$tmp"
end
