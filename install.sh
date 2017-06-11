#!/bin/sh
# Installs teabot.service.template into /etc/systemd/system/teabot.service
# and enables it to run at boot-time by default.
#
# Use the --fake argument in testing, to use a secondary server, and avoid the
# need for real USB scales + temperature sensor.

set -e

cd `dirname $0`

sudo pip install -r requirements.txt

if echo $* | grep -q -- --constants
then
    sudo env PYTHONPATH=$PWD python teabot/constants_setup.py
    echo "Please copy these values into teabot.contants.Constants then re-run."
    exit 0
fi

if [ -f teabot.service ]
then
    echo "Please delete teabot.service file before continuing."
    exit 1
fi

if echo $* | grep -q -- --fake
then
    ARGS=" --fake"
fi

cat teabot.service.template \
    | sed "s:{{PWD}}:$PWD:g" \
    | sed "s:{{ARGS}}:$ARGS:g" \
    > teabot.service

CURSOR=`sudo journalctl --lines=0 --show-cursor --unit=teabot.service | tail -n 1 | sed 's/-- cursor: //'`

sudo mv teabot.service /etc/systemd/system/
sudo systemctl enable teabot.service
sudo systemctl restart teabot.service
echo "Tailing logs to make sure everything worked. ^C to exit."
sudo journalctl -u teabot.service --after-cursor=$CURSOR --follow | head -n 100
