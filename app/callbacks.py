from dash import Input, Output, html, dcc

from data import (
    load_regions,
    load_finance,
    load_diplome,
    load_pcs,
    load_analyse_regions,
    load_relations_territoriales,
)

from charts import (
    create_region_profile,
    create_social_chart,
    create_fdep_health_chart,
)


# ============================================================
# Chargement des données
# ============================================================

regions = load_regions()

finance = load_finance()
diplome = load_diplome()
pcs = load_pcs()

analyse_regions = load_analyse_regions()
relations_territoriales = load_relations_territoriales()


def register_callbacks(app):
    """Enregistre les interactions de l'application."""

    # ========================================================
    # 1. Inégalités sociales de santé
    # ========================================================

    @app.callback(
        Output("social-chart", "figure"),
        Output("social-interpretation", "children"),
        Input("social-variable", "value"),
    )
    def update_social_chart(variable):

        # ----------------------------------------------------
        # Données
        # ----------------------------------------------------

        datasets = {
            "finance": finance,
            "diplome": diplome,
            "pcs": pcs,
        }


        # ----------------------------------------------------
        # Graphique
        # ----------------------------------------------------

        figure = create_social_chart(
            datasets[variable],
            variable,
        )


        # ----------------------------------------------------
        # Messages de lecture
        # ----------------------------------------------------

        social_messages = {

            "finance": {
                "titre": (
                    "Les écarts se creusent sur les trois dimensions de santé"
                ),
                "texte": (
                    "À mesure que la situation financière déclarée devient plus "
                    "difficile, la santé perçue diminue tandis que les limitations "
                    "d’activité et le diabète déclaré augmentent. Le gradient est "
                    "particulièrement marqué pour la santé perçue et les limitations "
                    "d’activité."
                ),
            },

            "diplome": {
                "titre": (
                    "Le diplôme s’accompagne d’écarts de santé nets"
                ),
                "texte": (
                    "Les personnes les plus diplômées déclarent plus souvent une "
                    "bonne santé, et moins souvent une limitation d’activité ou un "
                    "diabète. Les trois indicateurs évoluent ici dans une direction "
                    "cohérente."
                ),
            },

            "pcs": {
                "titre": (
                    "Des écarts existent sans former un gradient unique"
                ),
                "texte": (
                    "Les cadres présentent globalement les indicateurs les plus "
                    "favorables et les ouvriers des niveaux moins favorables. "
                    "Les catégories socioprofessionnelles ne constituent toutefois "
                    "pas une échelle sociale continue : leur comparaison reste "
                    "descriptive."
                ),
            },
        }


        # ----------------------------------------------------
        # Interprétation
        # ----------------------------------------------------

        message = social_messages[variable]

        interpretation = html.Div(
            [
                html.H3(
                    message["titre"],
                    className="dashboard-reading-title",
                ),

                html.P(
                    message["texte"],
                    className="dashboard-reading-text",
                ),
            ]
        )


        return figure, interpretation

    # ========================================================
    # 2. Défavorisation territoriale et santé
    # ========================================================

    @app.callback(
        Output("fdep-health-chart", "figure"),
        Output("fdep-interpretation", "children"),
        Input("territorial-health-variable", "value"),
    )
    def update_fdep_health_chart(indicateur):

        # ----------------------------------------------------
        # Graphique
        # ----------------------------------------------------

        figure = create_fdep_health_chart(
            analyse_regions,
            relations_territoriales,
            indicateur,
        )

        # ----------------------------------------------------
        # Correspondance avec relations_territoriales.csv
        # ----------------------------------------------------

        indicateurs = {
            "sante": "Santé perçue bonne ou très bonne",
            "limitation": "Limitation d'activité",
            "diabete": "Diabète déclaré",
        }

        nom_indicateur = indicateurs[indicateur]

        relation = relations_territoriales.loc[
            relations_territoriales["indicateur"] == nom_indicateur
        ].iloc[0]

        r = relation["correlation_fdep"]
        p = relation["p_value_fdep"]

        # ----------------------------------------------------
        # Interprétation
        # ----------------------------------------------------

        interpretations = {

            "sante": {
                "titre": (
                    "La santé perçue diminue avec la défavorisation territoriale"
                ),
                "texte": (
                    "Les régions présentant "
                    "un FDep plus élevé tendent à compter une part plus faible "
                    "de personnes déclarant une bonne ou très bonne santé."
                ),
            },

            "limitation": {
                "titre": (
                    "La relation avec la limitation d'activité est plus modérée"
                ),
                "texte": (
                    "Les limitations d'activité tendent à être plus fréquentes "
                    "dans les régions plus défavorisées, mais la relation observée "
                    "est moins marquée à cette échelle."
                ),
            },

            "diabete": {
                "titre": (
                    "Le diabète déclaré augmente avec la défavorisation territoriale"
                ),
                "texte": (
                    "Les régions présentant un FDep plus élevé tendent également "
                    "à présenter une fréquence plus importante de diabète déclaré."
                ),
            },
        }

        message = interpretations[indicateur]

        interpretation = html.Div(
            [
                html.H3(
                    message["titre"],
                    className="dashboard-reading-title",
                ),

                html.P(
                    message["texte"],
                    className="dashboard-reading-text",
                ),

                html.P(
                    f"r = {r:.2f} · p = {p:.3f} · 13 régions",
                    className="dashboard-stat",
                ),
            ]
        )
        return figure, interpretation
    
    # ========================================================
    # 3. Fiche régionale et profil standardisé
    # ========================================================

    @app.callback(
        Output("region-details", "children"),
        Output("region-profile-container", "children"),
        Input("map-profiles", "clickData"),
    )
    def update_region_details(click_data):

        # ----------------------------------------------------
        # Aucun clic
        # ----------------------------------------------------

        if click_data is None:

            placeholder = html.Div(
                [
                    html.P(
                        "EXPLORATION",
                        className="region-eyebrow",
                    ),

                    html.H3(
                        "Explorer une région",
                        className="region-title",
                    ),

                    html.P(
                        "Sélectionnez une région sur la carte pour afficher "
                        "ses indicateurs et situer son profil par rapport aux "
                        "13 régions étudiées.",
                        className="region-text",
                    ),
                ],
                className="region-placeholder",
            )

            return placeholder, None

        # ----------------------------------------------------
        # Région sélectionnée
        # ----------------------------------------------------

        region_name = click_data["points"][0]["location"]

        region = regions.loc[
            regions["region"] == region_name
        ].iloc[0]

        # ----------------------------------------------------
        # Fiche régionale
        # ----------------------------------------------------

        population = (
            f"{region['population']:,.0f}"
            .replace(",", " ")
        )

        details = [

            html.Div(
                [

                    html.Div(
                        [
                            html.P(
                                "RÉGION SÉLECTIONNÉE",
                                className="region-eyebrow",
                            ),

                            html.H2(
                                region["region"],
                                className="region-title",
                            ),

                            html.P(
                                region["profil"],
                                className="region-profile-name",
                            ),
                        ]
                    ),

                    html.Div(
                        [
                            html.Span(
                                "Population",
                                className="region-population-label",
                            ),

                            html.Strong(
                                population,
                                className="region-population-value",
                            ),

                            html.Span(
                                "habitants",
                                className="region-population-unit",
                            ),
                        ],
                        className="region-population",
                    ),

                ],
                className="region-header",
            ),


            # ========================================================
            # Indicateurs
            # ========================================================

            html.Div(
                [

                    # ------------------------------------------------
                    # Santé
                    # ------------------------------------------------

                    html.Div(
                        [

                            html.P(
                                "SANTÉ",
                                className="region-section-label",
                            ),

                            html.Div(
                                [
                                    html.Span(
                                        "Santé perçue",
                                        className="region-metric-label",
                                    ),

                                    html.Strong(
                                        f"{region['sante_percue']:.1f} %",
                                        className="region-metric-value",
                                    ),
                                ],
                                className="region-metric",
                            ),

                            html.Div(
                                [
                                    html.Span(
                                        "Limitation d'activité",
                                        className="region-metric-label",
                                    ),

                                    html.Strong(
                                        f"{region['limitation_activite']:.1f} %",
                                        className="region-metric-value",
                                    ),
                                ],
                                className="region-metric",
                            ),

                            html.Div(
                                [
                                    html.Span(
                                        "Diabète déclaré",
                                        className="region-metric-label",
                                    ),

                                    html.Strong(
                                        f"{region['diabete_declare']:.1f} %",
                                        className="region-metric-value",
                                    ),
                                ],
                                className="region-metric",
                            ),

                        ],
                        className="region-metrics-group",
                    ),


                    # ------------------------------------------------
                    # Contexte territorial
                    # ------------------------------------------------

                    html.Div(
                        [

                            html.P(
                                "CONTEXTE TERRITORIAL",
                                className="region-section-label",
                            ),

                            html.Div(
                                [
                                    html.Span(
                                        "FDep",
                                        className="region-metric-label",
                                    ),

                                    html.Strong(
                                        f"{region['fdep_pondere']:.2f}",
                                        className="region-metric-value",
                                    ),
                                ],
                                className="region-metric",
                            ),

                            html.Div(
                                [
                                    html.Span(
                                        "F-EDI",
                                        className="region-metric-label",
                                    ),

                                    html.Strong(
                                        f"{region['fedi_pondere']:.2f}",
                                        className="region-metric-value",
                                    ),
                                ],
                                className="region-metric",
                            ),

                            html.Div(
                                [
                                    html.Span(
                                        "APL",
                                        className="region-metric-label",
                                    ),

                                    html.Strong(
                                        f"{region['apl_pondere']:.2f}",
                                        className="region-metric-value",
                                    ),
                                ],
                                className="region-metric",
                            ),

                        ],
                        className="region-metrics-group",
                    ),

                ],
                className="region-metrics-grid",
            ),

        ]

        # ----------------------------------------------------
        # Profil standardisé
        # ----------------------------------------------------

        profile_figure = create_region_profile(
            regions,
            region_name,
        )

        profile_card = html.Div(
            [

                html.Div(
                    [

                        html.P(
                            "POSITION RELATIVE",
                            className="region-section-label",
                        ),

                        html.H3(
                            "Par rapport aux 13 régions"
                        ),

                    ],
                    className="region-profile-heading",
                ),

                html.P(
                    "0 correspond à la moyenne. Une valeur positive indique "
                    "une situation relativement plus défavorable et une valeur "
                    "négative une situation relativement plus favorable. "
                    "La longueur du segment indique l’écart à la moyenne des 13 régions : "
                    "plus le point est éloigné de 0, plus la région se distingue sur l’indicateur considéré.",
                    className="region-profile-note",
                ),

                dcc.Graph(
                    figure=profile_figure,

                    config={
                        "responsive": True,
                        "displayModeBar": False,
                    },

                    className="region-profile-chart",
                ),

            ],
            className="region-profile-card",
        )

        return details, profile_card