import pandas as pd
from mtgsdk import Card

from sets import recent_sets
from utils.cache import s3_cache

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)


def retrieve_cards(code):
    return [i.__dict__ for i in Card.where(set=code).all()]


def load_set_cards(code):
    return s3_cache(f"cards/{code}_cards.json", retrieve_cards, code)


if __name__ == "__main__":
    for s in recent_sets("2019-01-01"):
        code = s["code"]
        print(code, len(load_set_cards(code)))
