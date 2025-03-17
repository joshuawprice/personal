audio_volume=$(amixer -M get Master |\
awk '/Mono.+/ {print $6=="[off]" ?\
$4" 🔇": \
$4" 🔉"}' |\
tr -d [])

date_time="$(date +'%Y-%m-%d %X')"

#battery=$(upower --show-info $(upower --enumerate | grep BAT) | grep -E 'state|percentage' | awk '{print $2}')
battery=/sys/class/power_supply/BAT0/
battery="$(< $battery/status) $(< $battery/capacity)%"

echo $audio_volume $date_time $battery
