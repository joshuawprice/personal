#!/bin/sh

palette="/tmp/palette.png"
filters="fps=30,scale=720:-1:flags=lanczos"

ffmpeg -v warning -i "$1" -vf "$filters,palettegen" -y $palette
ffmpeg -v warning -i "$1" -i $palette -lavfi "$filters [x]; [x][1:v] paletteuse=dither=floyd_steinberg" -y "$2"
