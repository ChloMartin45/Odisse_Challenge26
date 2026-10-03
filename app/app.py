from dash import Dash

from data import load_regions
from layout import create_layout
from maps import create_map
from callbacks import register_callbacks


app = Dash(__name__)


regions = load_regions()
map_figure = create_map(regions)

app.layout = create_layout(map_figure)

register_callbacks(app)


if __name__ == "__main__":
    app.run(debug=True)