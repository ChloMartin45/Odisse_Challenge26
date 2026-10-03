from dash import Input, Output, html

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
        Input("social-variable", "value"),
    )
    def update_social_chart(variable):

        datasets = {
            "finance": finance,
            "diplome": diplome,
            "pcs": pcs,
        }

        return create_social_chart(
            datasets[variable],
            variable,
        )

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
            "sante": (
                "Une défavorisation territoriale plus élevée est associée "
                "à une moins bonne santé perçue dans les régions étudiées."
            ),
            "limitation": (
                "La relation observée entre défavorisation territoriale "
                "et limitation d'activité est plus modérée et plus incertaine."
            ),
            "diabete": (
                "Les régions présentant une défavorisation territoriale "
                "plus élevée tendent également à présenter davantage "
                "de diabète déclaré."
            ),
        }

        interpretation = html.P([
            interpretations[indicateur],
            html.Br(),
            html.Strong(
                f"r = {r:.2f} · p = {p:.3f}"
            ),
        ])

        return figure, interpretation

    # ========================================================
    # 3. Fiche régionale et profil standardisé
    # ========================================================

    @app.callback(
        Output("region-details", "children"),
        Output("region-profile", "figure"),
        Output("region-profile-container", "style"),
        Input("map-profiles", "clickData"),
    )
    def update_region_details(click_data):

        # ----------------------------------------------------
        # Aucun clic
        # ----------------------------------------------------

        if click_data is None:

            return [
                html.H2("Explorer une région"),
                html.P(
                    "Sélectionnez une région sur la carte "
                    "pour afficher ses indicateurs et situer son profil "
                    "par rapport aux 13 régions étudiées."
                ),
            ], {}, {"display": "none"}

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

        details = [
            html.H2(region["region"]),

            html.H3(region["profil"]),

            html.P(
                f"Population : {region['population']:,.0f}"
                .replace(",", " ")
            ),

            html.H4("Indicateurs de santé"),

            html.P(
                f"Santé perçue bonne ou très bonne : "
                f"{region['sante_percue']:.1f} %"
            ),

            html.P(
                f"Limitation d'activité : "
                f"{region['limitation_activite']:.1f} %"
            ),

            html.P(
                f"Diabète déclaré : "
                f"{region['diabete_declare']:.1f} %"
            ),

            html.H4("Contexte territorial"),

            html.P(
                f"FDep : {region['fdep_pondere']:.2f}"
            ),

            html.P(
                f"F-EDI : {region['fedi_pondere']:.2f}"
            ),

            html.P(
                f"APL : {region['apl_pondere']:.2f}"
            ),
        ]

        # ----------------------------------------------------
        # Profil standardisé
        # ----------------------------------------------------

        profile_figure = create_region_profile(
            regions,
            region_name,
        )

        return details, profile_figure, {"display": "block"}