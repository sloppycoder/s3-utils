#!/bin/bash

# Check if a filename has been provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 filename"
    exit 1
fi

filename="$1"

# Check if the file exists
if [ ! -f "$filename" ]; then
    echo "Error: File not found."
    exit 1
fi

BUCKET=brick.vino9.net

while IFS= read -r line
do
    status=$(aws s3api head-object --bucket $BUCKET --key "$line" | jq -r ".Restore")

    if [ "$status" = "null" ]; then
        echo calling restore-object for $line
        aws s3api restore-object --bucket $BUCKET --key "$line" --restore-request 'Days=7,GlacierJobParameters={Tier=Standard}'
    else
        echo $line, $status
    fi

done < "$filename"

# the file can be created with the following AWS CLI command
# aws s3api list-objects --bucket bucket_name_ --query 'Contents[].Key' --prefix="prefix/" | jq -r '.[]'
