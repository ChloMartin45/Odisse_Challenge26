from dash import Input, Output, html, dcc, ctx, no_update

from charts import (
    create_region_profile,
    create_social_chart,
    create_fdep_health_chart,
)


SOCIAL_MESSAGES = {
    "finance": {
        "titre": (
            "Les écarts se creusent sur les trois dimensions de santé"
        ),
        "texte": (
            "À mesure que la situation financière déclarée devient plus "
            "difficile, la santé perçue diminue tandis que les limitations "
            "dans les activités habituelles et le diabète déclaré augmentent. Le gradient est "
            "particulièrement marqué pour la santé perçue et les limitations "
            "dans les activités habituelles."
        ),
    },

    "diplome": {
        "titre": (
            "Le diplôme s’accompagne d’écarts de santé nets"
        ),
        "texte": (
            "Les personnes les plus diplômées déclarent plus souvent une "
            "bonne santé, et moins souvent des limitations dans les activités habituelles ou un "
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

FDEP_INDICATOR_LABELS = {
    "sante": "Santé perçue bonne ou très bonne",
    "limitation": "Limitation d'activité",
    "diabete": "Diabète déclaré",
}

FDEP_MESSAGES = {
    "sante": {
        "titre": (
            "La santé perçue diminue nettement avec la défavorisation territoriale"
        ),
        "texte": (
            "Les régions les plus défavorisées tendent à présenter une part "
            "plus faible de personnes déclarant une bonne ou très bonne santé. "
            "C'est la relation la plus marquée observée avec le FDep."
        ),
    },

    "limitation": {
        "titre": (
            "Les limitations augmentent aussi, mais la relation est moins nette"
        ),
        "texte": (
            "Les limitations dans les activités habituelles tendent à être "
            "plus fréquentes dans les régions les plus défavorisées. "
            "L'association est toutefois plus modérée et plus incertaine."
        ),
    },

    "diabete": {
        "titre": (
            "Le diabète déclaré est plus fréquent dans les régions défavorisées"
        ),
        "texte": (
            "Les régions présentant un FDep plus élevé tendent à afficher "
            "une fréquence plus importante de diabète déclaré. "
            "La relation est nette, même si elle est moins forte que pour la santé perçue."
        ),
    },
}

def create_region_metric(label, value):
    return html.Div(
        [
            html.Span(
                label,
                className="region-metric-label",
            ),

            html.Strong(
                value,
                className="region-metric-value",
            ),
        ],
        className="region-metric",
    )

def register_callbacks(app, regions, finance, diplome, pcs, analyse_regions, relations_territoriales):
    """Enregistre les interactions de l'application."""

    social_datasets = {
        "finance": finance,
        "diplome": diplome,
        "pcs": pcs,
    }
    
    app.clientside_callback(
        """
        function(tab) {
            window.scrollTo(0, 0);
            return tab;
        }
        """,
        Output("scroll-trigger", "data"),
        Input("main-tabs", "value"),
    )
    
    # ========================================================
    # Navigation entre les onglets
    # ========================================================

    @app.callback(
        Output("main-tabs", "value"),
        Input("go-to-social", "n_clicks"),
        Input("go-to-territoires", "n_clicks"),
        Input("go-to-profils", "n_clicks"),
        prevent_initial_call=True,
    )
    def navigate_tabs(go_social, go_territoires, go_profils):

        triggered = ctx.triggered_id
        
        if triggered == "go-to-social":
            return "social"

        if triggered == "go-to-territoires":
            return "territoires"

        if triggered == "go-to-profils":
            return "profils"

        return no_update

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
        # Graphique
        # ----------------------------------------------------

        figure = create_social_chart(
            social_datasets[variable],
            variable,
        )

        # ----------------------------------------------------
        # Interprétation
        # ----------------------------------------------------

        message = SOCIAL_MESSAGES[variable]

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

        nom_indicateur = FDEP_INDICATOR_LABELS[indicateur]

        relation = relations_territoriales.loc[
            relations_territoriales["indicateur"] == nom_indicateur
        ].iloc[0]

        r = relation["correlation_fdep"]
        p = relation["p_value_fdep"]

        # ----------------------------------------------------
        # Interprétation
        # ----------------------------------------------------

        message = FDEP_MESSAGES[indicateur]

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

                            create_region_metric(
                                "Bonne santé perçue",
                                f"{region['sante_percue']:.1f} %",
                            ),

                            create_region_metric(
                                "Limitations dans les activités habituelles",
                                f"{region['limitation_activite']:.1f} %",
                            ),

                            create_region_metric(
                                "Diabète déclaré",
                                f"{region['diabete_declare']:.1f} %",
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

                            create_region_metric(
                                "FDep pondéré",
                                f"{region['fdep_pondere']:.2f}",
                            ),

                            create_region_metric(
                                "F-EDI pondéré",
                                f"{region['fedi_pondere']:.2f}",
                            ),
                            create_region_metric(
                                "APL pondérée",
                                f"{region['apl_pondere']:.2f}",
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
                            "Écart à la moyenne des 13 régions"
                        ),
                    ],
                    className="region-profile-heading",
                ),

                html.P(
                    "0 correspond à la moyenne des 13 régions. "
                    "Les scores standardisés sont orientés dans le même sens : "
                    "plus le point est à droite, plus la situation est relativement défavorable. "
                    "Plus il est éloigné de 0, plus la région se distingue de la moyenne.",

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