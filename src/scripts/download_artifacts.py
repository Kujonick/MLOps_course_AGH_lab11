import boto3
import os
from src.scripts.settings import Settings


def load_artifacts(settings: Settings):
    s3 = boto3.client("s3")

    if settings.bucket is None or settings.prefix is None or settings.resource_dir is None:
        raise ValueError("missing .env or enviromental variables")

    paginator = s3.get_paginator("list_objects_v2")

    for page in paginator.paginate(Bucket=settings.bucket, Prefix=settings.prefix):
        if "Contents" not in page:  # no files in s3
            raise FileNotFoundError("No files in that bucket")

        for obj in page["Contents"]:
            key = obj["Key"][len(settings.prefix):]
            if key.endswith("/") or not key:  # folder
                continue

            local_path = os.path.join(settings.resource_dir, key)
            if os.path.exists(local_path):  # file already exists
                continue

            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            print(f"Downloading {key:<60} -> {local_path:<60}")

            s3.download_file(settings.bucket, obj["Key"], local_path)
