#!/usr/bin/env bash

echo ********************
echo Starting Replication
echo ********************

sleep 10 | echo Sleeping...
mongo mongodb://db-manager:27017 replica.js