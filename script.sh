#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <N>"
    exit 1
fi

N=$1

if ! [[ "$N" =~ ^[0-9]+$ ]]; then
    echo "Error: Please provide a valid positive integer."
    exit 1
fi

echo "Even numbers from 0 to $N:"
for ((i=0; i<=$N; i+=2)); do
    echo $i
done
