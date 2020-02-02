import os

import boto3
from botocore.config import Config

import settings  # noqa: F401


REGION = os.getenv("AWS_REGION")
BUCKET = os.getenv("S3_BUCKET")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


class S3Client:
    def __init__(
        self,
        aws_access_key_id=None,
        aws_secret_access_key=None,
        region_name=None,
        bucket=None,
    ):
        config = Config(connect_timeout=5, retries={"max_attempts": 5})
        self.bucket = bucket or BUCKET
        self.client = boto3.client(
            "s3",
            region_name=region_name or REGION,
            aws_access_key_id=aws_access_key_id or AWS_ACCESS_KEY_ID,
            aws_secret_access_key=aws_secret_access_key or AWS_SECRET_ACCESS_KEY,
            verify=True,
            config=config,
        )

    def ls(self, prefix="", bucket=None, full=False):
        """List all objects in a bucket under a specific prefix."""
        bucket = bucket or self.bucket

        # grab initial data
        s3_response = self.client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        contents = s3_response.get("Contents", [])
        if not contents:
            return contents

        # if truncated, keep fetching data
        while s3_response["IsTruncated"]:
            s3_response = self.client.list_objects_v2(
                Bucket=bucket,
                Prefix=prefix,
                ContinuationToken=s3_response["NextContinuationToken"],
            )
            contents += s3_response["Contents"]

        contents.sort(key=lambda x: x["LastModified"], reverse=True)
        if full:
            return contents
        else:
            return [file["Key"] for file in contents if not file["Key"].endswith("/")]

    def cp(self, src, dest, bucket=None):
        bucket = bucket or self.bucket
        self.client.copy_object(Bucket=bucket, CopySource=f"{bucket}/{src}", Key=dest)

    def rm(self, key, bucket=None):
        bucket = bucket or self.bucket
        self.client.delete_object(Bucket=bucket, Key=key)

    def mv(self, src, dest, bucket=None):
        bucket = bucket or self.bucket
        if src == dest:
            return
        self.cp(src, dest, bucket=bucket)
        self.rm(src, bucket=bucket)

    def upload(self, content, key, bucket=None):
        bucket = bucket or self.bucket
        self.client.put_object(Body=content, Bucket=bucket, Key=key)

    def read(self, key, bucket=None, full=False):
        bucket = bucket or self.bucket
        f = self.client.get_object(Bucket=bucket, Key=key)
        if full:
            return f
        return f["Body"]

    def exists(self, key, bucket=None):
        bucket = bucket or self.bucket
        try:
            keys = self.ls(prefix=key, bucket=bucket)
            return len(keys) and keys[0] == key
        except Exception:
            return False


if __name__ == "__main__":
    s3 = S3Client()
    print(s3.exists("test.txt"))
    s3.upload("test", "test.txt")
    print(s3.exists("test.txt"))
    s3.mv("test.txt", "test2.txt")
    print(s3.exists("test.txt"))
    print(s3.exists("test2.txt"))
    s3.rm("test2.txt")
    print(s3.exists("test2.txt"))
