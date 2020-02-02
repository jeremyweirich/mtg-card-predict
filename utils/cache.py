import json
import os
import time

from utils.aws import S3Client


S3 = S3Client()


def json_cache(p, retrieve, *args, **kwargs):
    if not os.path.exists(p):
        print(f"{p} not found in cache, fetching...")
        s = time.time()
        content = retrieve(*args, **kwargs)
        with open(p, "w") as f:
            f.write(json.dumps(content))
        print(f"{p} loaded in {time.time() - s}s")
    else:
        with open(p, "r") as f:
            content = json.loads(f.read())
    return content


def s3_cache(p, retrieve, *args, **kwargs):
    if not S3.exists(p):
        print(f"{p} not found in cache, fetching...")
        s = time.time()
        content = retrieve(*args, **kwargs)
        S3.upload(json.dumps(content), p)
        print(f"{p} loaded in {time.time() - s}s")
    else:
        content = json.loads(S3.read(p).read())
    return content
