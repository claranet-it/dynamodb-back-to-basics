#!/bin/bash

ENDPOINT_URL="http://dynamodb-local:8000"
DATA_DIR="./data"

# Create tables
for f in $DATA_DIR/*.table.json; do 
    aws dynamodb create-table --endpoint-url $ENDPOINT_URL --cli-input-json file://"${f#./}"; 
done

# Load fixtures
for f in $DATA_DIR/*.fixtures.json; do 
    aws dynamodb batch-write-item --endpoint-url $ENDPOINT_URL --request-items file://"${f#./}"; 
done