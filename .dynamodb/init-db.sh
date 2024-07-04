#!/bin/bash

DATA_DIR="./data"

# Create tables
for f in $DATA_DIR/*.table.json; do 
    aws dynamodb create-table --endpoint-url $1 --cli-input-json file://"${f#./}"; 
done

# Load fixtures
for f in $DATA_DIR/*.fixtures.json; do 
    aws dynamodb batch-write-item --endpoint-url $1 --request-items file://"${f#./}"; 
done