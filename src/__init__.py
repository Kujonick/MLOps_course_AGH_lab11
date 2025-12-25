import boto3
import os
from dotenv import load_dotenv

s3 = boto3.client("s3")

load_dotenv()

BUCKET = os.getenv("BUCKET")
PREFIX = os.getenv("PREFIX")
LOCAL_DIR = os.getenv("LOCAL_DIR")

if BUCKET is None or PREFIX is None or LOCAL_DIR is None:
    raise ValueError("missing .env")

paginator = s3.get_paginator("list_objects_v2")

for page in paginator.paginate(Bucket=BUCKET, Prefix=PREFIX):
    if "Contents" not in page:  # no files in s3
        continue

    for obj in page["Contents"]:
        key = obj["Key"][len(PREFIX) :]
        if key.endswith("/") or not key:  # folder
            continue

        local_path = os.path.join(LOCAL_DIR, key)
        if os.path.exists(local_path):  # file already exists
            continue

        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        print(f"Downloading {key:<60} -> {local_path:<60}")

        s3.download_file(BUCKET, obj["Key"], local_path)
