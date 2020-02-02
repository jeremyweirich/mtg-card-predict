import json
import os
import time
from functools import lru_cache


@lru_cache(maxsize=50)
def json_cache(p, retrieve, *args, **kwargs):
    if not os.path.exists(p):
        print(f"{p} not found locally, fetching...")
        s = time.time()
        content = retrieve(*args, **kwargs)
        with open(p, "w") as f:
            f.write(json.dumps(content))
        print(f"{p} loaded in {time.time() - s}s")
    else:
        with open(p, "r") as f:
            content = json.loads(f.read())
    return content
