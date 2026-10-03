import pandas as pd
import plotly.graph_objects as go


INDICATEURS_STANDARDISES = {
    "z_fdep": "Défavorisation (FDep)",
    "z_fedi": "Défavorisation (F-EDI)",
    "z_apl": "Faible accessibilité aux soins",
    "z_sante": "Santé perçue défavorable",
    "z_limitation": "Limitation d'activité",
    "z_diabete": "Diabète déclaré",
}


def create_region_profile(regions, region_name):
    """Crée le profil standardisé d'une région."""

    region = regions.loc[
        regions["region"] == region_name
    ].iloc[0]

    indicateurs = list(INDICATEURS_STANDARDISES.values())

    valeurs = [
        region[colonne]
        for colonne in INDICATEURS_STANDARDISES
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=valeurs,
            y=indicateurs,
            orientation="h",
            name=region_name,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Score standardisé : %{x:.2f}"
                "<extra></extra>"
            ),
        )
    )

    # Ligne représentant la moyenne des 13 régions
    fig.add_vline(
        x=0,
        line_width=2,
        line_dash="dash",
        annotation_text="Moyenne",
        annotation_position="top",
    )

    fig.update_layout(
        title=f"Profil territorial — {region_name}",
        xaxis_title="Score standardisé",
        yaxis_title=None,
        showlegend=False,
        height=450,
        margin=dict(l=170, r=30, t=70, b=60),
    )

    return fig

def create_social_chart(data, variable):
    """Crée le graphique des indicateurs de santé selon une dimension sociale."""

    configurations = {
        "finance": {
            "colonne": "situation_financiere",
            "ordre": [
                "À l'aise",
                "Ça va",
                "C'est juste",
                "Difficultés financières",
            ],
            "titre": "La santé se dégrade à mesure que les difficultés financières augmentent",
            "axe": "Situation financière perçue",
        },

        "diplome": {
            "colonne": "Diplôme",
            "ordre": [
                "Aucun diplôme ou inférieur au Bac",
                "Bac",
                "Supérieur au Bac",
            ],
            "titre": "Les indicateurs de santé diffèrent selon le niveau de diplôme",
            "axe": "Niveau de diplôme",
        },

        "pcs": {
            "colonne": "PCS",
            "ordre": [
                "Cadres et professions intellectuelles supérieures",
                "Professions intermédiaires",
                "Agriculteurs, artisans, commerçants, chefs d’entreprise",
                "Employés",
                "Ouvriers",
            ],
            "titre": "Les indicateurs de santé diffèrent selon la catégorie socioprofessionnelle",
            "axe": "Catégorie socioprofessionnelle",
        },
    }

    config = configurations[variable]

    fig = go.Figure()

    for indicateur in data["Indicateur"].unique():

        subset = data[
            data["Indicateur"] == indicateur
        ].copy()

        subset[config["colonne"]] = pd.Categorical(
            subset[config["colonne"]],
            categories=config["ordre"],
            ordered=True,
        )

        subset = subset.sort_values(config["colonne"])
        mode = "markers" if variable == "pcs" else "lines+markers"
        
        fig.add_trace(
            go.Scatter(
                x=subset[config["colonne"]],
                y=subset["Estimation"],
                mode=mode,
                name=indicateur,

                error_y=dict(
                    type="data",
                    symmetric=False,
                    array=subset["ic_sup"] - subset["Estimation"],
                    arrayminus=subset["Estimation"] - subset["ic_inf"],
                ),

                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "%{y:.1f} %"
                    "<extra>%{fullData.name}</extra>"
                ),
            )
        )

    fig.update_layout(
        title=config["titre"],
        xaxis_title=config["axe"],
        yaxis_title="Part de la population (%)",
        hovermode="x unified",
        height=500,
        margin=dict(l=60, r=30, t=70, b=100),
    )

    return fig

def create_fdep_health_chart(regions, relations, indicateur):
    """
    Crée le nuage de points entre le FDep régional
    et un indicateur de santé.
    """

    configurations = {
        "sante": {
            "colonne": "sante_percue",
            "libelle": "Santé perçue bonne ou très bonne",
            "axe_y": "Bonne ou très bonne santé perçue (%)",
            "titre": (
                "La santé perçue est moins favorable "
                "dans les territoires plus défavorisés"
            ),
        },

        "limitation": {
            "colonne": "limitation_activite",
            "libelle": "Limitation d'activité",
            "axe_y": "Limitation d'activité (%)",
            "titre": (
                "La limitation d'activité tend à augmenter "
                "avec la défavorisation territoriale"
            ),
        },

        "diabete": {
            "colonne": "diabete_declare",
            "libelle": "Diabète déclaré",
            "axe_y": "Diabète déclaré (%)",
            "titre": (
                "Le diabète déclaré est plus fréquent "
                "dans les territoires plus défavorisés"
            ),
        },
    }

    config = configurations[indicateur]

    # Résultats statistiques correspondant à l'indicateur sélectionné
    stats = relations.loc[
        relations["indicateur"] == config["libelle"]
    ].iloc[0]

    correlation = stats["correlation_fdep"]
    p_value = stats["p_value_fdep"]

    fig = go.Figure()

    # --------------------------------------------------------
    # Régions
    # --------------------------------------------------------

    fig.add_trace(
        go.Scatter(
            x=regions["fdep_pondere"],
            y=regions[config["colonne"]],
            mode="markers",
            text=regions["region"],
            customdata=regions["region"],

            marker=dict(
                size=11,
            ),

            hovertemplate=(
                "<b>%{customdata}</b><br>"
                "FDep : %{x:.2f}<br>"
                + config["axe_y"]
                + " : %{y:.1f} %"
                "<extra></extra>"
            ),
        )
    )

    # --------------------------------------------------------
    # Droite de tendance
    # --------------------------------------------------------

    fig.add_trace(
        go.Scatter(
            x=regions["fdep_pondere"],
            y=(
                regions["fdep_pondere"]
                * regions[
                    ["fdep_pondere", config["colonne"]]
                ].cov().iloc[0, 1]
                / regions["fdep_pondere"].var()
                + (
                    regions[config["colonne"]].mean()
                    - regions["fdep_pondere"].mean()
                    * regions[
                        ["fdep_pondere", config["colonne"]]
                    ].cov().iloc[0, 1]
                    / regions["fdep_pondere"].var()
                )
            ),
            mode="lines",
            name="Tendance linéaire",
            hoverinfo="skip",
        )
    )

    # --------------------------------------------------------
    # Mise en forme
    # --------------------------------------------------------

    fig.update_layout(
        title=config["titre"],
        xaxis_title="Défavorisation territoriale — FDep",
        yaxis_title=config["axe_y"],
        height=500,
        margin=dict(l=70, r=30, t=90, b=70),
        showlegend=False,

        annotations=[
            dict(
                x=0.02,
                y=0.98,
                xref="paper",
                yref="paper",
                text=(
                    f"r = {correlation:.2f}"
                    f" · p = {p_value:.3f}"
                    " · n = 13"
                ),
                showarrow=False,
                xanchor="left",
                yanchor="top",
            )
        ],
    )

    return fig

def create_apl_comparison_chart(relations):
    """
    Compare la corrélation brute entre l'APL et la santé
    à la corrélation partielle après prise en compte du FDep.
    """

    labels = {
        "Santé perçue bonne ou très bonne": "Santé perçue",
        "Limitation d'activité": "Limitation d'activité",
        "Diabète déclaré": "Diabète déclaré",
    }

    data = relations.copy()

    data["label"] = data["indicateur"].map(labels)

    fig = go.Figure()

    # --------------------------------------------------------
    # Corrélation brute avec l'APL
    # --------------------------------------------------------

    fig.add_trace(
        go.Scatter(
            x=data["correlation_apl"],
            y=data["label"],
            mode="markers",
            name="Association brute",

            marker=dict(
                size=12,
                symbol="circle",
            ),

            customdata=data["p_value_apl"],

            hovertemplate=(
                "<b>%{y}</b><br>"
                "Corrélation avec l'APL : %{x:.2f}<br>"
                "p-value : %{customdata:.3f}"
                "<extra></extra>"
            ),
        )
    )

    # --------------------------------------------------------
    # Corrélation après prise en compte du FDep
    # --------------------------------------------------------

    fig.add_trace(
        go.Scatter(
            x=data["correlation_partielle_apl_fdep"],
            y=data["label"],
            mode="markers",
            name="Après prise en compte du FDep",

            marker=dict(
                size=12,
                symbol="diamond",
            ),

            customdata=data["p_value_apl_apres_fdep"],

            hovertemplate=(
                "<b>%{y}</b><br>"
                "Corrélation partielle : %{x:.2f}<br>"
                "p-value : %{customdata:.3f}"
                "<extra></extra>"
            ),
        )
    )

    # --------------------------------------------------------
    # Ligne correspondant à l'absence de corrélation
    # --------------------------------------------------------

    fig.add_vline(
        x=0,
        line_dash="dash",
        line_width=1,
    )

    # --------------------------------------------------------
    # Mise en forme
    # --------------------------------------------------------

    fig.update_layout(
        title=(
            "L'accessibilité aux soins ne présente pas "
            "la même relation avec toutes les dimensions de santé"
        ),

        xaxis=dict(
            title="Coefficient de corrélation",
            range=[-1, 1],
            zeroline=False,
        ),

        yaxis_title=None,

        height=400,

        margin=dict(
            l=150,
            r=40,
            t=90,
            b=70,
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
    )

    return fig