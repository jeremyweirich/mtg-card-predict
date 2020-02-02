import os
from datetime import datetime

from mtgsdk import Set

from settings import DATA_ROOT
from utils import json_cache


RELEASE_CUTOFF = datetime(2019, 1, 1)


def retrieve_sets():
    return [i.__dict__ for i in Set.all()]


def load_sets():
    cache_path = os.path.join(DATA_ROOT, "sets.json")
    return json_cache(cache_path, retrieve_sets)


def recent_sets(cutoff):
    if isinstance(cutoff, str):
        cutoff = datetime.strptime(cutoff, "%Y-%m-%d")
    for s in load_sets():
        release_date = datetime.strptime(s["release_date"], "%Y-%m-%d")
        if release_date >= cutoff:
            if s["type"] == "expansion":
                yield s


if __name__ == "__main__":
    for s in recent_sets("2019-01-01"):
        print(f"{s['code']}: {s['name']}")
