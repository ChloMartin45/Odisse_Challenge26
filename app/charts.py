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