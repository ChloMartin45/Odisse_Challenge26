from dash import dcc, html
from charts import (
    create_social_chart,
    create_fdep_health_chart,
    create_apl_comparison_chart,
)

def create_layout(map_figure, finance, diplome, pcs, analyse_regions, relations_territoriales):
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
        # 1. Inégalités sociales de santé
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

        # =====================================================
        # 2. Territoires et accès aux soins
        # =====================================================
        

        html.H2("2. Territoires et accès aux soins"),

        html.P(
            "Les différences de santé observées entre régions "
            "sont-elles associées à leur niveau de défavorisation ?"
        ),
        # -----------------------------------------------------
        # Défavorisation territoriale et santé
        # -----------------------------------------------------
        
        html.H3(
            "Défavorisation territoriale et santé"
        ),

        html.P(
            "Sélectionnez un indicateur de santé pour observer "
            "sa relation avec l'indice de défavorisation sociale FDep."
        ),

        dcc.RadioItems(
            id="territorial-health-variable",
            options=[
                {
                    "label": "Santé perçue",
                    "value": "sante",
                },
                {
                    "label": "Limitation d'activité",
                    "value": "limitation",
                },
                {
                    "label": "Diabète déclaré",
                    "value": "diabete",
                },
            ],
            value="sante",
            inline=True,
        ),

        dcc.Graph(
            id="fdep-health-chart",
            figure=create_fdep_health_chart(
                analyse_regions,
                relations_territoriales,
                "sante",
            ),
        ),

        html.P(
            "Lecture : chaque point représente une région métropolitaine. "
            "Le coefficient r mesure l'intensité et le sens de la relation "
            "linéaire entre les deux indicateurs."
        ),

        html.P(
            "Ces analyses sont exploratoires et portent sur 13 régions "
            "métropolitaines. Elles décrivent des associations territoriales "
            "et ne permettent pas d'établir une relation causale ou "
            "individuelle."
        ),
        
        # -----------------------------------------------------
        # Accessibilité aux soins
        # -----------------------------------------------------

        html.H3(
            "Accessibilité aux soins : une dimension différente"
        ),

        html.P(
            "L'accessibilité aux médecins généralistes suit-elle "
            "les mêmes relations avec la santé que la défavorisation territoriale ? "
            "Le graphique compare l'association brute avec l'APL à celle "
            "observée après prise en compte du FDep."
        ),

        dcc.Graph(
            id="apl-comparison-chart",
            figure=create_apl_comparison_chart(
                relations_territoriales
            ),
        ),

        html.P(
            "La limitation d'activité se distingue : son association "
            "avec l'APL reste marquée après prise en compte du FDep "
            "(r = 0,55 ; p = 0,063). "
            "Les relations avec la santé perçue et le diabète sont plus faibles."
        ),

        html.P(
            "Lecture : une valeur proche de 0 indique une faible relation "
            "linéaire. Les valeurs négatives et positives indiquent le sens "
            "de l'association. L'APL augmente lorsque l'accessibilité aux "
            "médecins généralistes est meilleure."
        ),

        # =====================================================
        # 3. Profils territoriaux
        # =====================================================

        html.H2("3. Profils territoriaux"),

        html.P(
            "Défavorisation, accessibilité aux soins et état de santé "
            "ne se superposent pas nécessairement. "
            "Explorez les profils territoriaux issus de leur analyse conjointe."
        ),

        # -----------------------------------------------------
        # Carte
        # -----------------------------------------------------

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