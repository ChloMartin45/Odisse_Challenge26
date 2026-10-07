from pathlib import Path

import pandas as pd


# ============================================================
# Chemin vers les données préparées
# ============================================================

DATA_DIR = (
    Path(__file__).parent.parent
    / "data"
    / "processed"
)


# ============================================================
# 1. Inégalités sociales de santé
# ============================================================

def load_finance():
    """Charge les indicateurs de santé selon la situation financière perçue."""
    return pd.read_csv(
        DATA_DIR / "indicateurs_finance.csv"
    )


def load_diplome():
    """Charge les indicateurs de santé selon le niveau de diplôme."""
    return pd.read_csv(
        DATA_DIR / "indicateurs_diplome.csv"
    )


def load_pcs():
    """Charge les indicateurs de santé selon la catégorie socioprofessionnelle."""
    return pd.read_csv(
        DATA_DIR / "indicateurs_pcs.csv"
    )

def load_synthese_sociale():
    """Charge la synthèse des écarts sociaux de santé."""
    return pd.read_csv(
        DATA_DIR / "synthese_sociale.csv"
    )


# ============================================================
# 2. Relations territoriales
# ============================================================

def load_analyse_regions():
    """Charge les indicateurs territoriaux et de santé des 13 régions."""
    return pd.read_csv(
        DATA_DIR / "analyse_regions.csv"
    )


def load_relations_territoriales():
    """Charge les corrélations territoriales et leurs p-values."""
    return pd.read_csv(
        DATA_DIR / "relations_territoriales.csv"
    )


# ============================================================
# 3. Profils territoriaux HCPC
# ============================================================

def load_regions():
    """Charge les profils HCPC des 13 régions."""
    return pd.read_csv(
        DATA_DIR / "carte_regions_hcpc.csv"
    )

def load_profils_clusters():
    """Charge les caractéristiques moyennes des quatre profils territoriaux."""

    return pd.read_csv(
        DATA_DIR / "profils_clusters.csv"
    )

# ============================================================
# 4. Focus diabète
# ============================================================

def load_diabete_age_sexe():
    """Charge les estimations du diabète déclaré selon l'âge et le sexe."""

    return pd.read_csv(
        DATA_DIR / "focus_diabete_age_sexe.csv"
    )
    
def load_diabete_ecart_sexe_age():
    """Charge l'écart hommes-femmes du diabète déclaré selon l'âge."""

    return pd.read_csv(
        DATA_DIR / "focus_diabete_ecart_sexe_age.csv"
    )

def load_diabete_residus_regions():
    """Charge les écarts régionaux au modèle FDep -> diabète."""
    return pd.read_csv(
        DATA_DIR / "focus_diabete_residus_regions.csv"
    )
