from dash import Dash

from data import (
    load_regions,
    load_finance,
    load_diplome,
    load_pcs,
)
from layout import create_layout
from maps import create_map
from callbacks import register_callbacks

app = Dash(__name__)


regions = load_regions()

finance = load_finance()
diplome = load_diplome()
pcs = load_pcs()

map_figure = create_map(regions)

app.layout = create_layout(
    map_figure,
    finance,
    diplome,
    pcs,
)

register_callbacks(app)


if __name__ == "__main__":
    app.run(debug=True)