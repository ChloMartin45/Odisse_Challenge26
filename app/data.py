from pathlib import Path

import pandas as pd


DATA_DIR = (
    Path(__file__).parent.parent
    / "data"
    / "processed"
)


def load_regions():
    """Charge les profils HCPC des 13 régions."""
    return pd.read_csv(
        DATA_DIR / "carte_regions_hcpc.csv"
    )