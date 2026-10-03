from dash import dcc, html


def create_layout(map_figure):
    return html.Div([

        # -----------------------------------------------------
        # En-tête
        # -----------------------------------------------------

        html.H1("Inégalités sociales et territoriales de santé"),

        html.P(
            "Une exploration des profils territoriaux de santé "
            "et de leur accessibilité aux soins en France."
        ),

        # -----------------------------------------------------
        # Carte
        # -----------------------------------------------------

        html.H2("Profils territoriaux"),

        html.P(
            "Cliquez sur une région pour explorer ses indicateurs."
        ),

        dcc.Graph(
            id="map-profiles",
            figure=map_figure
        ),

        # -----------------------------------------------------
        # Fiche régionale
        # -----------------------------------------------------

        html.Div(
            id="region-details",
            children=[
                html.H2("Explorer une région"),
                html.P(
                    "Sélectionnez une région sur la carte "
                    "pour afficher son profil territorial."
                )
            ]
        )

    ])