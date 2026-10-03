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

FINANCE_PATH = (
    Path(__file__).parent.parent
    / "data"
    / "processed"
    / "indicateurs_finance.csv"
)


def load_finance():
    """Charge les indicateurs de santé selon la situation financière perçue."""
    return pd.read_csv(FINANCE_PATH)

DIPLOME_PATH = (
    Path(__file__).parent.parent
    / "data"
    / "processed"
    / "indicateurs_diplome.csv"
)

def load_diplome():
    """Charge les indicateurs de santé selon le niveau de diplôme."""
    return pd.read_csv(DIPLOME_PATH)

PCS_PATH = (
    Path(__file__).parent.parent
    / "data"
    / "processed"
    / "indicateurs_pcs.csv"
)

def load_pcs():
    """Charge les indicateurs de santé selon la PCS."""
    return pd.read_csv(PCS_PATH)