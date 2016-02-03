#!/usr/bin/env bash
# ONLY USE THIS IN DEVELOPMENT ENVIRONMENTS!!!

function block_for_change () {
  inotifywait -r \
    -e modify,move,create,delete \
    --exclude '.*(\.pyc|~)' .
}
function build () {
  sudo /usr/local/sbin/update-intelmq $1
}

build 2
build 3
echo '######################################################################'
echo '######################################################################'
while block_for_change; do
  build 2
  build 3
  echo '######################################################################'
  echo '######################################################################'
done
