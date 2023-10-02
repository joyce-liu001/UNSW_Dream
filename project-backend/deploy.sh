#!/usr/bin/env bash

WORKING_DIRECTORY="~/www/cs1531deploy"

USERNAME="thur11amaero"
SSH_HOST="ssh-thur11amaero.alwaysdata.net"

rm -rf ./**/__pycache__ ./**/.pytest_cache > /dev/null
scp -r ./requirements.txt ./src "$USERNAME@$SSH_HOST:$WORKING_DIRECTORY"
ssh "$USERNAME@$SSH_HOST" "cd $WORKING_DIRECTORY && source env/bin/activate && pip3 install -r requirements.txt"
