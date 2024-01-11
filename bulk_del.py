import argparse
import sys

import boto3
from dotenv import load_dotenv


def bulk_del_objects(s3, bucket_name, prefix):
    total = 0

    continuation_token = None
    while True:
        # List objects in the bucket
        if continuation_token:
            response = s3.list_objects_v2(Bucket=bucket_name, ContinuationToken=continuation_token, Prefix=prefix)
        else:
            response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        obj_list = [{"Key": obj["Key"]} for obj in response.get("Contents", [])]
        if len(obj_list) > 0:
            # print(obj_list)
            s3.delete_objects(Bucket=bucket_name, Delete={"Objects": obj_list, "Quiet": True})
            total += len(obj_list)
            print(f"Deleted {total} objects")

        if response["IsTruncated"]:
            continuation_token = response["NextContinuationToken"]
        else:
            break


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix", help="file prefix")
    parser.add_argument("--bucket", help="S3 bucket name", default="brick.vino9.net")
    options = parser.parse_args(argv)
    return options


def main(argv):
    options = parse_args(argv)

    session = boto3.Session()
    s3 = session.client("s3")
    bulk_del_objects(s3, options.bucket, prefix=options.prefix)


if __name__ == "__main__":
    load_dotenv()
    main(sys.argv[1:])
