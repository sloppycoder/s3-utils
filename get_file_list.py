import argparse
import json
import re
import sys

import boto3
from dotenv import load_dotenv
from tqdm import tqdm

# regex for parsing restore header
# 'ongoing-request="false", expiry-date="Wed, 17 Jan 2024 00:00:00 GMT"'
restore_p = re.compile(r'([\w|\-]+)\s*=\s*"([^"]*)"')


def list_objects(s3, bucket_name, prefix):
    result = {}

    continuation_token = None
    while True:
        # List objects in the bucket
        if continuation_token:
            response = s3.list_objects_v2(Bucket=bucket_name, ContinuationToken=continuation_token, Prefix=prefix)
        else:
            response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        for obj in tqdm(response.get("Contents", [])):
            key = obj["Key"]
            etag = obj["ETag"].strip('"')  # Remove quotes around ETag
            storage_class = obj.get("StorageClass", "STANDARD")
            size = obj["Size"]

            obj_stats = {"etag": etag, "storage_class": storage_class, "size": size}
            metadata = s3.head_object(Bucket=bucket_name, Key=key)
            if "Restore" in metadata:
                restore = dict(restore_p.findall(metadata["Restore"]))
                obj_stats["restore"] = restore
            if "Etag" in metadata:
                obj_stats["etag2"] = metadata["ETag"].strip('"')

            result[key] = obj_stats

        if response["IsTruncated"]:
            continuation_token = response["NextContinuationToken"]
        else:
            break

    return result


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix", help="file prefix")
    parser.add_argument("--bucket", help="S3 bucket name", default="brick.vino9.net")
    parser.add_argument("--output", help="output file", default="obj_stats.json")
    options = parser.parse_args(argv)
    return options


def main(argv):
    options = parse_args(argv)

    session = boto3.Session()
    s3 = session.client("s3")
    stats = list_objects(s3, options.bucket, prefix=options.prefix)
    with open(options.output, "w") as f:
        json.dump(stats, f, indent=4)


if __name__ == "__main__":
    load_dotenv()
    main(sys.argv[1:])
