#!/usr/bin/env sh

# start cloud event receiver server
python3 tests/cloudevent_receiver_server.py &
sleep 1

if [ "$1" = "dev" ]
then
  echo "Executing only 'dev' tests ..."
  pytest -m "dev"
elif [ "$1" = "integrationtest" ]
then
  pytest -m "integrationtest"
elif [ "$1" = "unittest" ]
then
  pytest -m "unittest"
else
  pytest
fi

TEST_RES=$?

# TODO: stop cloud event receiver server

return $TEST_RES
