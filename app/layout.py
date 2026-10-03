from dash import dcc, html
from charts import create_social_chart

def create_layout(map_figure, finance, diplome, pcs):
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
        # 1ère section : indicateurs sociaux
        # -----------------------------------------------------
        html.H2("1. Les inégalités sociales de santé"),

        html.P(
            "La santé varie-t-elle selon la position sociale ? "
            "Explorez trois dimensions : la situation financière perçue, "
            "le niveau de diplôme et la catégorie socioprofessionnelle."
        ),

        dcc.RadioItems(
            id="social-variable",
            options=[
                {
                    "label": "Situation financière",
                    "value": "finance",
                },
                {
                    "label": "Diplôme",
                    "value": "diplome",
                },
                {
                    "label": "Catégorie socioprofessionnelle",
                    "value": "pcs",
                },
            ],
            value="finance",
            inline=True,
        ),

        dcc.Graph(
            id="social-chart",
            figure=create_social_chart(
                finance,
                "finance",
            ),
        ),

        html.P(
            "Lecture : les estimations sont accompagnées de leur "
            "intervalle de confiance à 95 %. "
            "Les résultats décrivent des différences observées entre groupes "
            "et ne permettent pas, à eux seuls, d'établir une relation causale."
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
        ),

        # -----------------------------------------------------
        # Profil standardisé
        # -----------------------------------------------------

        dcc.Graph(
            id="region-profile"
        )

    ])