#!/bin/bash

# Usage: ./run.sh "<query>" "<country>"
# Example: ./run.sh "iPhone 16 Pro, 128GB" "US"

if [ "$#" -ne 2 ]; then
  echo "Usage: ./run.sh \"<query>\" \"<country>\""
  exit 1
fi

QUERY="$1"
COUNTRY="$2"

python3 main.py --query "$QUERY" --country "$COUNTRY" 