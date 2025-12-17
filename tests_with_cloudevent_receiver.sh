#!/usr/bin/env sh

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
return $TEST_RES
