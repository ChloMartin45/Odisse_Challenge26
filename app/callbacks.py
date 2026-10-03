from dash import Input, Output, html

from data import load_regions


regions = load_regions()


def register_callbacks(app):
    """Enregistre les interactions de l'application."""

    @app.callback(
        Output("region-details", "children"),
        Input("map-profiles", "clickData"),
    )
    def update_region_details(click_data):

        # Aucun clic : message par défaut
        if click_data is None:
            return [
                html.H2("Explorer une région"),
                html.P(
                    "Sélectionnez une région sur la carte "
                    "pour afficher son profil territorial."
                ),
            ]

        # Région récupérée depuis la carte
        region_name = click_data["points"][0]["location"]

        # Recherche de la région dans les données
        region = regions.loc[
            regions["region"] == region_name
        ].iloc[0]

        return [
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