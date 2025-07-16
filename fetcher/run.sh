#!/bin/sh
while true; do
    echo "Running stock fetcher at $(date)"
    python main.py
    sleep 14400  # 4 hours
done