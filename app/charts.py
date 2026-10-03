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
    Visualise la relation entre la défavorisation territoriale
    et un indicateur de santé dans les 13 régions étudiées.
    """

    configurations = {
        "sante": {
            "colonne": "sante_percue",
            "libelle": "Santé perçue bonne ou très bonne",
            "axe_y": "Population en bonne ou très bonne santé perçue (%)",
            "titre": (
                "Une défavorisation plus élevée est associée "
                "à une moins bonne santé perçue"
            ),
        },

        "limitation": {
            "colonne": "limitation_activite",
            "libelle": "Limitation d'activité",
            "axe_y": "Population déclarant une limitation d'activité (%)",
            "titre": (
                "La relation entre défavorisation et limitation "
                "d'activité est moins nette"
            ),
        },

        "diabete": {
            "colonne": "diabete_declare",
            "libelle": "Diabète déclaré",
            "axe_y": "Population déclarant un diabète (%)",
            "titre": (
                "Le diabète déclaré est plus fréquent "
                "dans les territoires plus défavorisés"
            ),
        },
    }

    config = configurations[indicateur]

    stats = relations.loc[
        relations["indicateur"] == config["libelle"]
    ].iloc[0]

    correlation = stats["correlation_fdep"]
    p_value = stats["p_value_fdep"]

    # --------------------------------------------------------
    # Droite de tendance
    # --------------------------------------------------------

    covariance = regions[
        ["fdep_pondere", config["colonne"]]
    ].cov().iloc[0, 1]

    pente = (
        covariance
        / regions["fdep_pondere"].var()
    )

    intercept = (
        regions[config["colonne"]].mean()
        - pente * regions["fdep_pondere"].mean()
    )

    tendance = regions[
        ["fdep_pondere"]
    ].copy()

    tendance["y"] = (
        pente * tendance["fdep_pondere"]
        + intercept
    )

    tendance = tendance.sort_values(
        "fdep_pondere"
    )

    # --------------------------------------------------------
    # Figure
    # --------------------------------------------------------

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=tendance["fdep_pondere"],
            y=tendance["y"],
            mode="lines",
            name="Tendance",
            hoverinfo="skip",
            line=dict(
                width=2,
                dash="dash",
            ),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=regions["fdep_pondere"],
            y=regions[config["colonne"]],
            mode="markers",
            name="Régions",

            marker=dict(
                size=12,
            ),

            customdata=regions["region"],

            hovertemplate=(
                "<b>%{customdata}</b><br>"
                "FDep : %{x:.2f}<br>"
                + config["axe_y"]
                + " : %{y:.1f}"
                "<extra></extra>"
            ),
        )
    )
    fdep_min = regions["fdep_pondere"].min()
    fdep_max = regions["fdep_pondere"].max()

    # Petite marge pour aérer l'axe
    amplitude = fdep_max - fdep_min

    x_min = min(fdep_min - 0.10 * amplitude, 0)
    x_max = max(fdep_max + 0.10 * amplitude, 0)
    
    # --------------------------------------------------------
    # Mise en forme
    # --------------------------------------------------------

    fig.update_layout(
        title=dict(
            text=config["titre"],
            x=0,
        ),

        xaxis=dict(
            title=dict(
                text="Indice FDep",
                standoff=65,
            ),
            range=[x_min, x_max],
            zeroline=False,
        ),

        yaxis=dict(
            title=config["axe_y"],
        ),

        height=500,

        margin=dict(
            l=80,
            r=40,
            t=110,
            b=145,
        ),

        showlegend=False,

        annotations=[
            # --------------------------------------------------------
            # Informations statistiques
            # --------------------------------------------------------
            dict(
                x=0,
                y=1.10,
                xref="paper",
                yref="paper",
                text=(
                    f"<b>r = {correlation:.2f}</b>"
                    f"   ·   p = {p_value:.3f}"
                    "   ·   13 régions"
                ),
                showarrow=False,
                xanchor="left",
                font=dict(size=13),
            ),
        ],
    )
    
    # --------------------------------------------------------
    # Aide à la lecture de l'indice FDep
    # --------------------------------------------------------

    # Segment vers les valeurs négatives
    fig.add_shape(
        type="line",
        x0=0,
        x1=x_min,
        y0=-0.12,
        y1=-0.12,
        xref="x",
        yref="paper",
        line=dict(width=1.5),
    )

    # Segment vers les valeurs positives
    fig.add_shape(
        type="line",
        x0=0,
        x1=x_max,
        y0=-0.12,
        y1=-0.12,
        xref="x",
        yref="paper",
        line=dict(width=1.5),
    )

    # Petit trait vertical au niveau de 0
    fig.add_shape(
        type="line",
        x0=0,
        x1=0,
        y0=-0.105,
        y1=-0.135,
        xref="x",
        yref="paper",
        line=dict(width=1.5),
    )

    # Pointe gauche
    fig.add_annotation(
        x=x_min,
        y=-0.12,
        xref="x",
        yref="paper",
        text="◀",
        showarrow=False,
        xanchor="center",
        yanchor="middle",
        font=dict(size=10),
    )

    # Pointe droite
    fig.add_annotation(
        x=x_max,
        y=-0.12,
        xref="x",
        yref="paper",
        text="▶",
        showarrow=False,
        xanchor="center",
        yanchor="middle",
        font=dict(size=10),
    )

    # Libellé gauche
    fig.add_annotation(
        x=(x_min + 0) / 2,
        y=-0.18,
        xref="x",
        yref="paper",
        text="Régions moins défavorisées",
        showarrow=False,
        xanchor="center",
        font=dict(size=12),
    )

    # Libellé droite
    fig.add_annotation(
        x=(0 + x_max) / 2,
        y=-0.18,
        xref="x",
        yref="paper",
        text="Régions plus défavorisées",
        showarrow=False,
        xanchor="center",
        font=dict(size=12),
    )
    return fig

def create_apl_comparison_chart(relations):
    """
    Compare la corrélation brute entre l'APL et les indicateurs de santé
    à la corrélation partielle après prise en compte du FDep.
    """

    labels = {
        "Santé perçue bonne ou très bonne": "Santé perçue",
        "Limitation d'activité": "Limitation d'activité",
        "Diabète déclaré": "Diabète déclaré",
    }

    data = relations.copy()
    data["label"] = data["indicateur"].map(labels)

    # Ordre de lecture volontaire
    ordre = [
        "Santé perçue",
        "Limitation d'activité",
        "Diabète déclaré",
    ]

    data["label"] = pd.Categorical(
        data["label"],
        categories=ordre,
        ordered=True,
    )

    data = data.sort_values("label")

    fig = go.Figure()

    # --------------------------------------------------------
    # Traits reliant les deux mesures
    # --------------------------------------------------------

    for _, row in data.iterrows():
        fig.add_trace(
            go.Scatter(
                x=[
                    row["correlation_apl"],
                    row["correlation_partielle_apl_fdep"],
                ],
                y=[
                    row["label"],
                    row["label"],
                ],
                mode="lines",
                line=dict(
                    width=2,
                    color="lightgray",
                ),
                showlegend=False,
                hoverinfo="skip",
            )
        )

    # --------------------------------------------------------
    # Association brute
    # --------------------------------------------------------

    fig.add_trace(
        go.Scatter(
            x=data["correlation_apl"],
            y=data["label"],
            mode="markers+text",
            name="Avant prise en compte du FDep",

            marker=dict(
                size=13,
                symbol="circle",
            ),

            text=[
                f"{value:.2f}"
                for value in data["correlation_apl"]
            ],

            textposition="top center",

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
    # Après prise en compte du FDep
    # --------------------------------------------------------

    fig.add_trace(
        go.Scatter(
            x=data["correlation_partielle_apl_fdep"],
            y=data["label"],
            mode="markers+text",
            name="Après prise en compte du FDep",

            marker=dict(
                size=13,
                symbol="diamond",
            ),

            text=[
                f"{value:.2f}"
                for value in data["correlation_partielle_apl_fdep"]
            ],

            textposition="bottom center",

            customdata=data["p_value_apl_apres_fdep"],

            hovertemplate=(
                "<b>%{y}</b><br>"
                "Après prise en compte du FDep : %{x:.2f}<br>"
                "p-value : %{customdata:.3f}"
                "<extra></extra>"
            ),
        )
    )

    # --------------------------------------------------------
    # Repère : absence de relation linéaire
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
        title=dict(
            text=(
                "APL et santé : la limitation d'activité conserve la relation "
                "la plus marquée après prise en compte du FDep"
            ),
            x=0,
        ),

        xaxis=dict(
            title="Corrélation entre l'APL et l'indicateur de santé",
            range=[-1, 1],
            zeroline=False,
            tickvals=[-1, -0.5, 0, 0.5, 1],
        ),

        yaxis=dict(
            title=None,
            categoryorder="array",
            categoryarray=ordre[::-1],
        ),

        height=430,

        margin=dict(
            l=160,
            r=50,
            t=120,
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