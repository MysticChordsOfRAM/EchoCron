#!/bin/bash

if [ -f "/app/.env" ]; then
    set -a
    source /app/.env
    set +a
else
    echo ".env not found!"
    exit 1
fi

SOURCE_FILE="/output/$CALENDAR_FILENAME"
DESTINATION="$PUNT_DESTINATION"

if [ -f "$SOURCE_FILE" ]; then
    echo "[$(date + '%H:%M:%S')] Found $SOURCE_FILE. Starting transfer..."

    rsync -avz "$SOURCE_FILE" "$DESTINATION"

    IF_SUCCESS=$?
    if [$IF_SUCCESS -eq 0 ]; then
        echo "[$(date + '%H:%M:%S')] Transfer to Lomez Successfull."
    else
        echo "[$(date + '%H:%M:%S')] Error: Rsync Fail. Exit code $IF_SUCCESS"
        exit $IF_SUCCESS
    fi
else
    echo "[$(date + '%H:%M:%S')] Error Source File Not Found"
fi
