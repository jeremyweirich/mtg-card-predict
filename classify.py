import pandas as pd
from sklearn import metrics
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

from cards import load_set_cards

cards = load_set_cards("RNA")


# handle array features
filtered_cards = []
for card in cards:
    if card["watermark"] is None:
        continue
    card["primary_type"] = card["types"][0]
    card["color_identity"] = "".join([i for i in sorted(card["color_identity"])])
    filtered_cards.append(card)

# filter to just creatures
df = pd.DataFrame(filtered_cards)
# df = df[df["primary_type"] == "Creature"]

features = [
    "cmc",
    "rarity",
    "power",
    "toughness",
    # "watermark",
]
labels = ["color_identity"]
df = df[features + labels]
df.fillna("NULL", inplace=True)

# label encode all relevant fields
le = preprocessing.LabelEncoder()
for column in features + labels:
    df[column] = le.fit_transform(df[column])

X_train, X_test, y_train, y_test = train_test_split(
    df[features], df[labels], test_size=0.3
)

gnb = GaussianNB()
gnb.fit(X_train, y_train)

y_pred = gnb.predict(X_test)
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
