from pathlib import Path
import json

import plotly.graph_objects as go

from geojson_rewind import rewind


# ============================================================
# Chemins vers les données géographiques
# ============================================================

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

# ============================================================
# Chargement GeoJSON
# ============================================================


def load_geojson(path):
    """Charge un fichier GeoJSON."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)

# ============================================================
# Carte des profils territoriaux
# ============================================================

def create_map(regions):
    """
    Crée la carte interactive des profils territoriaux.
    """

    regions_geojson = rewind(
        load_geojson(REGIONS_GEOJSON_PATH),
        rfc7946=False,
    )

    departements_geojson = load_geojson(
        DEPARTEMENTS_GEOJSON_PATH
    )


    # ========================================================
    # Couleurs des quatre profils
    # ========================================================
    #
    # Palette catégorielle :
    # aucune logique vert = favorable / rouge = défavorable.
    # Les quatre couleurs servent uniquement à distinguer
    # les profils.
    # ========================================================

    couleurs = {
        1: "#3A75C4",   # bleu
        2: "#8B6FC0",   # violet
        3: "#E58A2B",   # orange
        4: "#C94F7C",   # framboise
    }


    # ========================================================
    # Noms des profils
    # ========================================================
    #
    # On récupère directement les noms présents dans la base
    # afin d'éviter de les dupliquer dans le code.
    # ========================================================

    noms_profils = (
        regions[
            ["clust", "profil"]
        ]
        .drop_duplicates()
        .sort_values("clust")
        .set_index("clust")["profil"]
        .to_dict()
    )


    # ========================================================
    # Figure
    # ========================================================

    fig = go.Figure()


    # ========================================================
    # 1. Régions
    # ========================================================

    fig.add_trace(
        go.Choropleth(

            geojson=regions_geojson,

            locations=regions["region"],

            featureidkey="properties.region",

            z=regions["clust"],

            zmin=1,
            zmax=4,


            # ------------------------------------------------
            # Échelle catégorielle discrète
            # ------------------------------------------------

            colorscale=[

                [0.000, couleurs[1]],
                [0.249, couleurs[1]],

                [0.250, couleurs[2]],
                [0.499, couleurs[2]],

                [0.500, couleurs[3]],
                [0.749, couleurs[3]],

                [0.750, couleurs[4]],
                [1.000, couleurs[4]],

            ],


            marker_line_color="white",

            marker_line_width=1.4,


            customdata=regions[
                [
                    "clust",
                    "profil",
                ]
            ].values,

            hovertemplate=(
                "<b>%{location}</b><br>"
                "Profil %{customdata[0]}<br>"
                "%{customdata[1]}<br><br>"
                "<i>Cliquez pour explorer cette région</i>"
                "<extra></extra>"
            ),

            showscale=False,
        )
    )


    # ========================================================
    # 2. Contours départementaux
    # ========================================================

    for feature in departements_geojson["features"]:

        geometry = feature["geometry"]

        if geometry["type"] == "Polygon":

            polygons = [
                geometry["coordinates"]
            ]

        elif geometry["type"] == "MultiPolygon":

            polygons = geometry["coordinates"]

        else:

            continue


        for polygon in polygons:

            for ring in polygon:

                lons = [
                    point[0]
                    for point in ring
                ]

                lats = [
                    point[1]
                    for point in ring
                ]

                fig.add_trace(
                    go.Scattergeo(

                        lon=lons,

                        lat=lats,

                        mode="lines",

                        line=dict(
                            color="rgba(45, 67, 86, 0.18)",
                            width=0.4,
                        ),

                        hoverinfo="skip",

                        showlegend=False,
                    )
                )


    # ========================================================
    # 3. Légende
    # ========================================================

    for cluster in sorted(
        noms_profils.keys()
    ):

        fig.add_trace(
            go.Scattergeo(

                lon=[None],

                lat=[None],

                mode="markers",

                marker=dict(
                    size=9,
                    color=couleurs[cluster],
                ),

                name=noms_profils[cluster],

                hoverinfo="skip",

                showlegend=True,
            )
        )


    # ========================================================
    # 4. Cadrage géographique
    # ========================================================
    #
    # On resserre volontairement le cadrage autour de la
    # France métropolitaine + Corse.
    #
    # La carte occupera ainsi réellement son panneau au lieu
    # de rester petite au centre d'un grand espace blanc.
    # ========================================================

    fig.update_geos(

        visible=False,

        projection_type="mercator",

        lonaxis_range=[
            -5.3,
            9.8,
        ],

        lataxis_range=[
            41.2,
            51.2,
        ],

        bgcolor="rgba(0,0,0,0)",
    )


    # ========================================================
    # 5. Mise en forme générale
    # ========================================================

    fig.update_layout(

        autosize=True,
        height=620,
        dragmode=False,
        hovermode="closest",

        margin=dict(
            l=8,
            r=8,
            t=12,
            b=8,
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            family="Outfit, Arial, sans-serif",
            color="#17324A",
            size=12,
        ),

        legend=dict(

            title=dict(
                text="Profils territoriaux",
                font=dict(
                    size=11,
                    color="#17324A",
                ),
            ),

            orientation="h",

            x=0.5,
            xanchor="center",

            y=-0.02,
            yanchor="top",

            bgcolor="rgba(0,0,0,0)",

            borderwidth=0,

            font=dict(
                size=10,
                color="#17324A",
            ),

            itemsizing="constant",
        ),


        hoverlabel=dict(

            bgcolor="white",

            bordercolor="#D5DEE8",

            font=dict(
                family="Outfit, Arial, sans-serif",
                color="#17324A",
                size=11,
            ),
            
            align="left",
        ),
    )
    
    return fig



# ========================================================
# 5. Carte diabète
# ========================================================

def create_diabetes_residuals_map(data):
    """
    Crée une carte analytique simple des écarts entre le diabète
    observé et la valeur associée au FDep.
    """

    regions_geojson = rewind(
        load_geojson(REGIONS_GEOJSON_PATH),
        rfc7946=False,
    )

    data_plot = data.copy()

    max_abs = max(
        abs(data_plot["residu_diabete"]).max(),
        0.5,
    )

    fig = go.Figure()

    fig.add_trace(
        go.Choropleth(
            geojson=regions_geojson,
            locations=data_plot["region"],
            featureidkey="properties.region",
            z=data_plot["residu_diabete"],
            zmin=-max_abs,
            zmax=max_abs,
            zmid=0,

            # Palette divergente douce
            colorscale=[
                [0.00, "#8B6FC0"],   # violet FDep
                [0.40, "#CBBCE7"],
                [0.50, "#F6F8FB"],   # neutre
                [0.60, "#F8D6B7"],
                [1.00, "#EC9955"],   # orange diabète
            ],

            marker_line_color="white",
            marker_line_width=1.4,

            customdata=data_plot[
                [
                    "diabete_declare",
                    "diabete_attendu",
                    "residu_diabete",
                ]
            ].values,

            hovertemplate=(
                "<b>%{location}</b><br><br>"
                "Diabète déclaré : <b>%{customdata[0]:.1f} %</b><br>"
                "Valeur associée au FDep : <b>%{customdata[1]:.1f} %</b><br>"
                "Écart à la tendance : <b>%{customdata[2]:+.1f} point(s)</b>"
                "<extra></extra>"
            ),

            colorbar=dict(
                title=dict(
                    text="Écart à la<br>tendance (pt)",
                    side="top",
                    font=dict(
                        size=11,
                        color="#17324A",
                    ),
                ),
                thickness=12,
                len=0.62,
                x=0.98,
                y=0.5,
                outlinewidth=0,
                tickfont=dict(
                    size=10,
                    color="#627487",
                ),
            ),
        )
    )

    fig.update_geos(
        visible=False,
        projection_type="mercator",
        lonaxis_range=[
            -5.3,
            9.8,
        ],
        lataxis_range=[
            41.2,
            51.2,
        ],
        bgcolor="rgba(0,0,0,0)",
    )

    fig.update_layout(
        autosize=True,
        height=470,
        dragmode=False,
        hovermode="closest",

        margin=dict(
            l=8,
            r=24,
            t=10,
            b=8,
        ),

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            family="Outfit, Arial, sans-serif",
            color="#17324A",
            size=12,
        ),

        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#D5DEE8",
            font=dict(
                family="Outfit, Arial, sans-serif",
                color="#17324A",
                size=11,
            ),
            align="left",
        ),
    )

    return fig