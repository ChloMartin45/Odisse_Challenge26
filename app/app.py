from dash import Dash

from data import (
    load_regions,
    load_finance,
    load_diplome,
    load_pcs,
    load_analyse_regions,
    load_relations_territoriales,
)

from layout import create_layout
from maps import create_map
from callbacks import register_callbacks


# ============================================================
# Application
# ============================================================

app = Dash(__name__)


# ============================================================
# Chargement des données
# ============================================================

regions = load_regions()

finance = load_finance()
diplome = load_diplome()
pcs = load_pcs()

analyse_regions = load_analyse_regions()
relations_territoriales = load_relations_territoriales()


# ============================================================
# Carte
# ============================================================

map_figure = create_map(regions)


# ============================================================
# Layout
# ============================================================

app.layout = create_layout(
    map_figure,
    finance,
    diplome,
    pcs,
    analyse_regions,
    relations_territoriales,
)


# ============================================================
# Callbacks
# ============================================================

register_callbacks(app)


# ============================================================
# Lancement
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)