"""Data loading and the time-based split used by every notebook."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = (
    ROOT / "data" / "raw" / "apachejit_dataset_replication"
    / "apachejit" / "dataset" / "apachejit_total.csv"
)

FEATURES = ["la", "ld", "nf", "nd", "ns", "ent", "ndev", "age", "nuc", "aexp", "arexp", "asexp"]
LABEL = "buggy"


def load_data():
    """Load the full dataset, ordered by commit time."""
    df = pd.read_csv(DATA_FILE)
    return df.sort_values("author_date").reset_index(drop=True)


def time_split(df):
    """Return train (<=2015), validation (2016), test (2017) and late check (>=2018)."""
    train = df[df["year"] <= 2015]
    validation = df[df["year"] == 2016]
    test = df[df["year"] == 2017]
    late = df[df["year"] >= 2018]
    return train, validation, test, late