from pathlib import Path
import json

import plotly.graph_objects as go

from geojson_rewind import rewind

REGIONS_GEOJSON_PATH = (
    Path(__file__).parent.parent
    / "data"
    / "processed"
    / "regions_hcpc.geojson"
)

DEPARTEMENTS_GEOJSON_PATH = (
    Path(__file__).parent.parent
    / "data"
    / "processed"
    / "departements.geojson"
)


def load_geojson(path):
    """Charge un fichier GeoJSON."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def create_map(regions):
    """Crée la carte interactive des profils territoriaux."""

    regions_geojson = rewind(load_geojson(REGIONS_GEOJSON_PATH), rfc7946=False)
    departements_geojson = load_geojson(DEPARTEMENTS_GEOJSON_PATH)

    # Correspondance entre les groupes HCPC et les couleurs
    couleurs = {
        1: "#4C78A8",
        2: "#59A14F",
        3: "#F28E2B",
        4: "#E15759",
    }

    noms_profils = {
        1: "Profil francilien atypique",
        2: "Profil territorial globalement favorable",
        3: "Profil de santé contrasté",
        4: "Profil de défavorisation et de santé défavorable",
    }

    # ---------------------------------------------------------
    # 1. Couche principale : régions
    # ---------------------------------------------------------

    fig = go.Figure()

    fig.add_trace(
        go.Choropleth(
            geojson=regions_geojson,
            locations=regions["region"],
            featureidkey="properties.region",
            z=regions["clust"],
            zmin=1,
            zmax=4,

            # Chaque intervalle correspond à un cluster
            colorscale=[
                [0.00, couleurs[1]],
                [0.249, couleurs[1]],

                [0.25, couleurs[2]],
                [0.499, couleurs[2]],

                [0.50, couleurs[3]],
                [0.749, couleurs[3]],

                [0.75, couleurs[4]],
                [1.00, couleurs[4]],
            ],

            marker_line_color="white",
            marker_line_width=1.5,

            customdata=regions[
                ["profil", "clust"]
            ].values,

            hovertemplate=(
                "<b>%{location}</b><br>"
                "Profil : %{customdata[0]}<br>"
                "Groupe : %{customdata[1]}"
                "<extra></extra>"
            ),

            showscale=False,
        )
    )

    # ---------------------------------------------------------
    # 2. Contours des départements
    # ---------------------------------------------------------

    for feature in departements_geojson["features"]:

        geometry = feature["geometry"]

        if geometry["type"] == "Polygon":
            polygons = [geometry["coordinates"]]

        elif geometry["type"] == "MultiPolygon":
            polygons = geometry["coordinates"]

        else:
            continue

        for polygon in polygons:

            for ring in polygon:

                lons = [point[0] for point in ring]
                lats = [point[1] for point in ring]

                fig.add_trace(
                    go.Scattergeo(
                        lon=lons,
                        lat=lats,
                        mode="lines",
                        line=dict(
                            color="rgba(80, 80, 80, 0.55)",
                            width=0.6,
                        ),
                        hoverinfo="skip",
                        showlegend=False,
                    )
                )

    # ---------------------------------------------------------
    # 3. Légende des profils
    # ---------------------------------------------------------

    for cluster, nom in noms_profils.items():

        fig.add_trace(
            go.Scattergeo(
                lon=[None],
                lat=[None],
                mode="markers",
                marker=dict(
                    size=10,
                    color=couleurs[cluster],
                ),
                name=nom,
                hoverinfo="skip",
                showlegend=True,
            )
        )

    # ---------------------------------------------------------
    # 4. Réglages géographiques
    # ---------------------------------------------------------

    fig.update_geos(
        visible=False,
        projection_type="mercator",
        lonaxis_range=[-5.5, 10],
        lataxis_range=[41, 51.5],
        bgcolor="rgba(0,0,0,0)",
    )    
    
    # ---------------------------------------------------------
    # 5. Mise en forme
    # ---------------------------------------------------------

    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        height=650,
        legend_title_text="Profil territorial",
    )

    return fig