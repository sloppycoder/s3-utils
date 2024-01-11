import argparse
import json
import os
import sys

from dotenv import load_dotenv


def check_files(stats, base_dir):
    diff_size = 0
    for key, obj in stats.items():
        try:
            stats = os.stat(f"{base_dir}/{key}")
            if stats.st_size != obj["size"]:
                print(f"x{key}")
                diff_size += obj["size"]
        except FileNotFoundError:
            print(f"-{key}")
            diff_size += obj["size"]
    if diff_size > 0:
        print(f"diff size: {round(diff_size/1024/1024/1024)}TB")


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True, help="base directory")
    parser.add_argument("--input", help="input fiie list in json format", default="obj_stats.json")
    options = parser.parse_args(argv)
    return options


def main(argv):
    options = parse_args(argv)

    with open(options.input, "r") as f:
        stats = json.load(f)
        check_files(stats, options.base)


if __name__ == "__main__":
    load_dotenv()
    main(sys.argv[1:])
