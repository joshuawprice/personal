# Pass multiple projects with commas between them to separate them
# separate multiple languages with commas or spaces

IFS=,
curl -sL https://www.toptal.com/developers/gitignore/api/"$*"
