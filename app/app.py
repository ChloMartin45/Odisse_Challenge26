from dash import Dash

from data import (
    load_regions,
    load_finance,
    load_diplome,
    load_pcs,
    load_synthese_sociale,
    load_analyse_regions,
    load_relations_territoriales,
    load_profils_clusters,
    load_diabete_age_sexe,
    load_diabete_ecart_sexe_age,
)

from layout import create_layout
from maps import create_map
from callbacks import register_callbacks


# ============================================================
# Application
# ============================================================

app = Dash(__name__)
server = app.server

# ============================================================
# Chargement des données
# ============================================================

regions = load_regions()

finance = load_finance()
diplome = load_diplome()
pcs = load_pcs()
synthese_sociale = load_synthese_sociale()

analyse_regions = load_analyse_regions()
relations_territoriales = load_relations_territoriales()

profils_clusters = load_profils_clusters()

# Focus diabète

diabete_age_sexe = load_diabete_age_sexe()
diabete_ecart_sexe_age = load_diabete_ecart_sexe_age()

# ============================================================
# Carte
# ============================================================

map_figure = create_map(regions)


# ============================================================
# Layout
# ============================================================

app.layout = create_layout(
    finance,
    synthese_sociale,
    analyse_regions,
    relations_territoriales,
    regions,
    profils_clusters,
    map_figure,
    diabete_age_sexe,
    diabete_ecart_sexe_age,
)


# ============================================================
# Callbacks
# ============================================================

register_callbacks(
    app,
    regions,
    finance,
    diplome,
    pcs,
    analyse_regions,
    relations_territoriales,)


# ============================================================
# Lancement
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)