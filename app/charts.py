import pandas as pd
import plotly.graph_objects as go
import math

# ============================================================
# Identité graphique
# ============================================================

COLOR_NAVY = "#0B3C5D"        # Structure / titres
COLOR_HEALTH = "#3A75C4"      # Santé perçue
COLOR_RASPBERRY = "#C2185B"   # Limitation d'activité
COLOR_ORANGE = "#F28E2B"      # Diabète déclaré

COLOR_DEPRIVATION = "#8B6FC0"

COLOR_GRID = "#E8EDF3"
COLOR_TEXT = "#17324A"
COLOR_MUTED = "#627487"

PLOT_BACKGROUND = "rgba(0,0,0,0)"

SOCIAL_STYLES = {
    "Santé perçue bonne ou très bonne": {
        "color": COLOR_HEALTH,
        "symbol": "circle",
    },

    "Limitation d'activité": {
        "color": COLOR_RASPBERRY,
        "symbol": "diamond",
    },

    "Diabète déclaré": {
        "color": COLOR_ORANGE,
        "symbol": "square",
    },
}

# ============================================================
# Indicateurs standardisés
# ============================================================

INDICATEURS_STANDARDISES = {
    "z_fdep": "Défavorisation (FDep)",
    "z_fedi": "Défavorisation (F-EDI)",
    "z_apl": "Faible accessibilité aux soins",
    "z_sante": "Santé perçue défavorable",
    "z_limitation": "Limitation d'activité",
    "z_diabete": "Diabète déclaré",
}


def create_region_profile(regions, region_name):
    """
    Crée une signature territoriale standardisée compacte.

    Convention :
    valeur positive = situation relativement plus défavorable
    valeur négative = situation relativement plus favorable.
    """

    region = regions.loc[
        regions["region"] == region_name
    ].iloc[0]

    # ========================================================
    # Indicateurs
    # ========================================================

    configuration = [
        {
            "colonne": "z_fdep",
            "label": "FDep",
            "label_complet": "Défavorisation — FDep",
            "color": COLOR_DEPRIVATION,
        },
        {
            "colonne": "z_fedi",
            "label": "F-EDI",
            "label_complet": "Défavorisation — F-EDI",
            "color": COLOR_DEPRIVATION,
        },
        {
            "colonne": "z_apl",
            "label": "Accessibilité",
            "label_complet": "Faible accessibilité aux soins",
            "color": COLOR_NAVY,
        },
        {
            "colonne": "z_sante",
            "label": "Santé perçue",
            "label_complet": "Santé perçue défavorable",
            "color": COLOR_HEALTH,
        },
        {
            "colonne": "z_limitation",
            "label": "Limitation",
            "label_complet": "Limitation d'activité",
            "color": COLOR_RASPBERRY,
        },
        {
            "colonne": "z_diabete",
            "label": "Diabète",
            "label_complet": "Diabète déclaré",
            "color": COLOR_ORANGE,
        },
    ]

    labels = [
        item["label"]
        for item in configuration
    ]

    valeurs = [
        region[item["colonne"]]
        for item in configuration
    ]


    # ========================================================
    # Axe X commun à toutes les régions
    # ========================================================
    #
    # Important : il ne change pas lorsqu'on clique sur une
    # autre région. La comparaison visuelle reste donc stable.
    # ========================================================

    colonnes_z = [
        item["colonne"]
        for item in configuration
    ]

    max_abs = max(
        regions[colonne].abs().max()
        for colonne in colonnes_z
    )

    limite = (
        math.ceil(
            (max_abs * 1.12) * 2
        )
        / 2
    )


    # ========================================================
    # Figure
    # ========================================================

    fig = go.Figure()


    # ========================================================
    # Lignes depuis la moyenne jusqu'à chaque région
    # ========================================================

    for item, valeur in zip(
        configuration,
        valeurs,
    ):

        fig.add_trace(
            go.Scatter(
                x=[
                    0,
                    valeur,
                ],

                y=[
                    item["label"],
                    item["label"],
                ],

                mode="lines",

                line=dict(
                    color="#D5DEE8",
                    width=3,
                ),

                showlegend=False,

                hoverinfo="skip",
            )
        )


    # ========================================================
    # Points
    # ========================================================

    fig.add_trace(
        go.Scatter(

            x=valeurs,

            y=labels,

            mode="markers",

            marker=dict(
                size=11,

                color=[
                    item["color"]
                    for item in configuration
                ],

                line=dict(
                    color="white",
                    width=1.5,
                ),
            ),

            customdata=[
                [
                    item["label_complet"],
                    valeur,
                ]
                for item, valeur in zip(
                    configuration,
                    valeurs,
                )
            ],

            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Score standardisé : "
                "<b>%{customdata[1]:+.2f}</b>"
                "<extra></extra>"
            ),

            showlegend=False,
        )
    )


    # ========================================================
    # Moyenne des 13 régions
    # ========================================================

    fig.add_vline(
        x=0,

        line_width=1.5,

        line_dash="dash",

        line_color="#98A8B8",
    )


    # ========================================================
    # Mise en forme
    # ========================================================

    fig.update_layout(

        font=dict(
            family="Outfit, Arial, sans-serif",
            color=COLOR_TEXT,
            size=12,
        ),

        plot_bgcolor=PLOT_BACKGROUND,
        paper_bgcolor=PLOT_BACKGROUND,

        height=300,

        margin=dict(
            l=125,
            r=18,
            t=18,
            b=42,
        ),

        showlegend=False,

        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#D5DEE8",

            font=dict(
                family="Outfit, Arial, sans-serif",
                color=COLOR_TEXT,
            ),
        ),
    )


    # ========================================================
    # Axe X
    # ========================================================

    fig.update_xaxes(

        range=[
            -limite,
            limite,
        ],

        zeroline=False,

        showgrid=True,
        gridcolor=COLOR_GRID,
        gridwidth=1,

        showline=False,

        title=None,

        tickfont=dict(
            size=10,
            color=COLOR_MUTED,
        ),

        tickformat=".1f",
    )


    # ========================================================
    # Axe Y
    # ========================================================

    fig.update_yaxes(

        categoryorder="array",

        categoryarray=labels[::-1],

        showgrid=False,

        showline=False,

        ticks="",

        tickfont=dict(
            size=11,
            color=COLOR_TEXT,
        ),
    )


    return fig

def create_social_chart(data, variable):
    """
    Crée le graphique des indicateurs de santé
    selon une dimension sociale.
    """

    configurations = {

        "finance": {
            "colonne": "situation_financiere",

            "ordre": [
                "À l'aise",
                "Ça va",
                "C'est juste",
                "Difficultés financières",
            ],

            "titre": (
                "La santé se dégrade à mesure que "
                "les difficultés financières augmentent"
            ),

            "axe": "Situation financière perçue",
        },


        "diplome": {
            "colonne": "Diplôme",

            "ordre": [
                "Aucun diplôme ou inférieur au Bac",
                "Bac",
                "Supérieur au Bac",
            ],

            "titre": (
                "Les indicateurs de santé diffèrent "
                "selon le niveau de diplôme"
            ),

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

            "titre": (
                "Les indicateurs de santé diffèrent "
                "selon la catégorie socioprofessionnelle"
            ),

            "axe": "Catégorie socioprofessionnelle",
        },
    }


    config = configurations[variable]

    pcs_labels = {
        "Cadres et professions intellectuelles supérieures": "Cadres",
        "Professions intermédiaires": "Professions<br>intermédiaires",
        "Agriculteurs, artisans, commerçants, chefs d’entreprise":
            "Agriculteurs, artisans,<br>commerçants, chefs d’entreprise",
        "Employés": "Employés",
        "Ouvriers": "Ouvriers",
    }
    fig = go.Figure()


    # ========================================================
    # Séries
    # ========================================================

    for indicateur in [
        "Santé perçue bonne ou très bonne",
        "Limitation d'activité",
        "Diabète déclaré",
    ]:

        subset = data[
            data["Indicateur"] == indicateur
        ].copy()


        if subset.empty:
            continue


        subset[config["colonne"]] = pd.Categorical(
            subset[config["colonne"]],
            categories=config["ordre"],
            ordered=True,
        )


        subset = subset.sort_values(
            config["colonne"]
        )


        style = SOCIAL_STYLES[indicateur]


        # Les PCS ne forment pas une échelle continue :
        # on ne relie donc pas les catégories entre elles.
        mode = (
            "markers"
            if variable == "pcs"
            else "lines+markers"
        )
        
        if variable == "pcs":
            x_values = [
                pcs_labels.get(value, value)
                for value in subset[config["colonne"]]
            ]
        else:
            x_values = subset[config["colonne"]]


        fig.add_trace(
            go.Scatter(

                x=x_values,

                y=subset[
                    "Estimation"
                ],

                mode=mode,

                name=indicateur,

                line=dict(
                    color=style["color"],
                    width=2.5,
                ),

                marker=dict(
                    color=style["color"],
                    symbol=style["symbol"],
                    size=10,

                    line=dict(
                        color="white",
                        width=1.5,
                    ),
                ),

                error_y=dict(
                    type="data",
                    symmetric=False,

                    array=(
                        subset["ic_sup"]
                        - subset["Estimation"]
                    ),

                    arrayminus=(
                        subset["Estimation"]
                        - subset["ic_inf"]
                    ),

                    color=style["color"],

                    thickness=1.2,

                    width=4,
                ),

                customdata=list(
                    zip(
                        subset[config["colonne"]].astype(str),
                        subset["ic_inf"],
                        subset["ic_sup"],
                    )
                ),

                hovertemplate=(
                    "<b>%{fullData.name}</b><br>"
                    "%{customdata[0]}<br><br>"
                    "<b>%{y:.1f} %</b><br>"
                    "IC 95 % : "
                    "%{customdata[1]:.1f} – "
                    "%{customdata[2]:.1f} %"
                    "<extra></extra>"
                ),
            )
        )


    # ========================================================
    # Mise en forme
    # ========================================================

    fig.update_layout(

        title=dict(
            text=config["titre"],

            x=0,

            xanchor="left",

            font=dict(
                family="Outfit, Arial, sans-serif",
                size=20,
                color=COLOR_NAVY,
            ),
        ),


        font=dict(
            family="Outfit, Arial, sans-serif",

            color=COLOR_TEXT,

            size=13,
        ),


        plot_bgcolor=PLOT_BACKGROUND,

        paper_bgcolor=PLOT_BACKGROUND,


        height=510,


        margin=dict(
            l=70,
            r=30,
            t=115,
            b=145,
        ),


        hovermode=(
            "x unified"
            if variable != "pcs"
            else "closest"
        ),


        hoverlabel=dict(
            bgcolor="white",

            bordercolor="#D5DEE8",

            font=dict(
                color=COLOR_TEXT,
                family="Outfit, Arial, sans-serif",
            ),
        ),


        legend=dict(

            orientation="h",

            yanchor="bottom",
            y=1.02,

            xanchor="left",
            x=0,

            title=None,

            font=dict(
                size=12,
                color=COLOR_TEXT,
            ),

            bgcolor="rgba(0,0,0,0)",
        ),


        showlegend=True,
    )


    # ========================================================
    # Axe X
    # ========================================================

    fig.update_xaxes(

    title=dict(
        text=config["axe"],
        font=dict(
            size=13,
            color=COLOR_MUTED,
        ),
    ),

    showgrid=False,

    showline=True,

    linecolor="#D5DEE8",

    linewidth=1,

    tickfont=dict(
        color=COLOR_TEXT,
        size=11,
    ),

    tickangle=0,

    automargin=True,

    ticks="",
)


    # ========================================================
    # Axe Y
    # ========================================================

    fig.update_yaxes(
        title=dict(
            text="Part de la population (%)",
            font=dict(
                size=13,
                color=COLOR_MUTED,
            ),
        ),

        # Même échelle pour les trois dimensions sociales
        range=[0, 100],

        tickmode="linear",
        tick0=0,
        dtick=20,

        showgrid=True,
        gridcolor=COLOR_GRID,
        gridwidth=1,

        zeroline=False,
        showline=False,

        tickfont=dict(
            color=COLOR_TEXT,
            size=12,
        ),

        ticksuffix=" %",
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
            "color": COLOR_HEALTH,
        },

        "limitation": {
            "colonne": "limitation_activite",
            "libelle": "Limitation d'activité",
            "axe_y": "Population déclarant une limitation d'activité (%)",
            "titre": (
                "La relation entre défavorisation et limitation "
                "d'activité est moins nette"
            ),
            "color": COLOR_RASPBERRY,
        },

        "diabete": {
            "colonne": "diabete_declare",
            "libelle": "Diabète déclaré",
            "axe_y": "Population déclarant un diabète (%)",
            "titre": (
                "Le diabète déclaré est plus fréquent "
                "dans les territoires plus défavorisés"
            ),
            "color": COLOR_ORANGE,
        },
    }

    config = configurations[indicateur]

    # --------------------------------------------------------
    # Préparation des écarts à la moyenne
    # --------------------------------------------------------

    regions_plot = regions.copy()

    # Moyenne de l'indicateur sélectionné
    moyenne_indicateur = regions_plot[config["colonne"]].mean()

    # Écart à la moyenne, en points de pourcentage
    regions_plot["ecart_moyenne"] = (
        regions_plot[config["colonne"]]
        - moyenne_indicateur
    )

    # --------------------------------------------------------
    # Échelle commune aux trois indicateurs
    # --------------------------------------------------------

    colonnes_sante = [
        "sante_percue",
        "limitation_activite",
        "diabete_declare",
    ]

    ecarts_max = []

    for colonne in colonnes_sante:
        moyenne = regions[colonne].mean()

        ecarts = (
            regions[colonne]
            - moyenne
        ).abs()

        ecarts_max.append(ecarts.max())

    max_abs_global = max(ecarts_max)

    # 15 % de marge autour de l'écart maximal
    max_abs_global *= 1.15


    def nice_step(value):
        """
        Retourne un pas de graduation lisible :
        1, 2, 5, 10, 20, 50...
        """
        if value <= 0:
            return 1

        exponent = math.floor(math.log10(value))
        fraction = value / (10 ** exponent)

        if fraction <= 1:
            nice_fraction = 1
        elif fraction <= 2:
            nice_fraction = 2
        elif fraction <= 5:
            nice_fraction = 5
        else:
            nice_fraction = 10

        return nice_fraction * (10 ** exponent)


    # Environ 6 à 8 intervalles sur l'ensemble de l'axe
    tick_step = nice_step(
        (2 * max_abs_global) / 8
    )

    # Borne symétrique autour de 0
    limite_y = (
        math.ceil(max_abs_global / tick_step)
        * tick_step
    )

    stats = relations.loc[
        relations["indicateur"] == config["libelle"]
    ].iloc[0]

    correlation = stats["correlation_fdep"]
    p_value = stats["p_value_fdep"]

    # --------------------------------------------------------
    # Droite de tendance sur les écarts à la moyenne
    # --------------------------------------------------------

    covariance = regions_plot[
        ["fdep_pondere", "ecart_moyenne"]
    ].cov().iloc[0, 1]

    pente = (
        covariance
        / regions_plot["fdep_pondere"].var()
    )

    intercept = (
        regions_plot["ecart_moyenne"].mean()
        - pente * regions_plot["fdep_pondere"].mean()
    )

    tendance = regions_plot[
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

    # Droite de tendance
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
                color=config["color"],
            ),
            opacity=0.55,
        )
    )

    # Régions
    fig.add_trace(
        go.Scatter(
            x=regions_plot["fdep_pondere"],
            y=regions_plot["ecart_moyenne"],
            mode="markers",
            name="Régions",

            marker=dict(
                size=13,
                color=config["color"],
                opacity=0.88,

                line=dict(
                    color="white",
                    width=1.8,
                ),
            ),

            customdata=regions_plot[
                [
                    "region",
                    config["colonne"],
                ]
            ].values,

            hovertemplate=(
                "<b>%{customdata[0]}</b><br><br>"
                "FDep : %{x:.2f}<br>"
                "Valeur : %{customdata[1]:.1f} %<br>"
                "Écart à la moyenne : %{y:+.1f} point(s)"
                "<extra></extra>"
            ),
        )
    )

    # --------------------------------------------------------
    # Bornes de l'axe X
    # --------------------------------------------------------

    fdep_min = regions["fdep_pondere"].min()
    fdep_max = regions["fdep_pondere"].max()

    amplitude = fdep_max - fdep_min

    x_min = min(
        fdep_min - 0.10 * amplitude,
        0
    )

    x_max = max(
        fdep_max + 0.10 * amplitude,
        0
    )

    # --------------------------------------------------------
    # Mise en forme
    # --------------------------------------------------------

    fig.update_layout(

        title=dict(
            text=config["titre"],
            x=0,
            xanchor="left",

            font=dict(
                family="Outfit, Arial, sans-serif",
                size=20,
                color=COLOR_NAVY,
            ),
        ),

        font=dict(
            family="Outfit, Arial, sans-serif",
            size=13,
            color=COLOR_TEXT,
        ),

        plot_bgcolor=PLOT_BACKGROUND,
        paper_bgcolor=PLOT_BACKGROUND,

        height=510,

        margin=dict(
            l=85,
            r=40,
            t=120,
            b=155,
        ),

        showlegend=False,

        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#D5DEE8",
            font=dict(
                family="Outfit, Arial, sans-serif",
                color=COLOR_TEXT,
            ),
        ),

        annotations=[
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

                font=dict(
                    size=12,
                    color=COLOR_MUTED,
                ),
            ),
        ],
    )

    # --------------------------------------------------------
    # Axe X
    # --------------------------------------------------------

    fig.update_xaxes(
        title=dict(
            text="Indice FDep",
            standoff=65,

            font=dict(
                size=13,
                color=COLOR_MUTED,
            ),
        ),

        range=[x_min, x_max],

        showgrid=False,

        zeroline=False,

        showline=True,
        linecolor="#D5DEE8",
        linewidth=1,

        tickfont=dict(
            color=COLOR_TEXT,
            size=12,
        ),

        ticks="",
    )

    # --------------------------------------------------------
    # Axe Y
    # --------------------------------------------------------

    fig.update_yaxes(
        title=dict(
            text="Écart à la moyenne régionale (points de %)",

            font=dict(
                size=13,
                color=COLOR_MUTED,
            ),
        ),

        range=[
            -limite_y,
            limite_y,
        ],

        tickmode="linear",
        tick0=0,
        dtick=tick_step,

        showgrid=True,
        gridcolor=COLOR_GRID,
        gridwidth=1,

        zeroline=True,
        zerolinecolor="#98A8B8",
        zerolinewidth=1.5,

        showline=False,

        tickfont=dict(
            color=COLOR_TEXT,
            size=12,
        ),

        ticksuffix=" pt",
    )

    # --------------------------------------------------------
    # Aide à la lecture du FDep
    # --------------------------------------------------------

    aide_color = "#98A8B8"

    # Ligne gauche
    fig.add_shape(
        type="line",
        x0=0,
        x1=x_min,
        y0=-0.12,
        y1=-0.12,
        xref="x",
        yref="paper",

        line=dict(
            width=1.2,
            color=aide_color,
        ),
    )

    # Ligne droite
    fig.add_shape(
        type="line",
        x0=0,
        x1=x_max,
        y0=-0.12,
        y1=-0.12,
        xref="x",
        yref="paper",

        line=dict(
            width=1.2,
            color=aide_color,
        ),
    )

    # Trait central
    fig.add_shape(
        type="line",
        x0=0,
        x1=0,
        y0=-0.105,
        y1=-0.135,
        xref="x",
        yref="paper",

        line=dict(
            width=1.2,
            color=aide_color,
        ),
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

        font=dict(
            size=9,
            color=aide_color,
        ),
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

        font=dict(
            size=9,
            color=aide_color,
        ),
    )

    # Libellé gauche
    fig.add_annotation(
        x=(x_min + 0) / 2,
        y=-0.19,
        xref="x",
        yref="paper",

        text="Moins défavorisées",

        showarrow=False,

        xanchor="center",

        font=dict(
            size=11,
            color=COLOR_MUTED,
        ),
    )

    # Libellé droite
    fig.add_annotation(
        x=(0 + x_max) / 2,
        y=-0.19,
        xref="x",
        yref="paper",

        text="Plus défavorisées",

        showarrow=False,

        xanchor="center",

        font=dict(
            size=11,
            color=COLOR_MUTED,
        ),
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

    # ========================================================
    # Traits reliant les deux mesures
    # ========================================================

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
                    color="#D9E1EA",
                ),
                showlegend=False,
                hoverinfo="skip",
            )
        )

    # ========================================================
    # Association brute
    # ========================================================

    fig.add_trace(
        go.Scatter(
            x=data["correlation_apl"],
            y=data["label"],
            mode="markers+text",
            name="Association brute",
            marker=dict(
                size=12,
                symbol="circle",
                color=COLOR_HEALTH,
                line=dict(
                    color="white",
                    width=1.5,
                ),
            ),
            text=[
                f"{value:.2f}"
                for value in data["correlation_apl"]
            ],
            textposition=[
                "top left",
                "bottom center",
                "top center",
            ],
            textfont=dict(
                size=11,
                color=COLOR_TEXT,
            ),
            customdata=data["p_value_apl"],
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Association brute avec l'APL : <b>%{x:.2f}</b><br>"
                "p-value : %{customdata:.3f}"
                "<extra></extra>"
            ),
        )
    )

    # ========================================================
    # Après prise en compte du FDep
    # ========================================================

    fig.add_trace(
        go.Scatter(
            x=data["correlation_partielle_apl_fdep"],
            y=data["label"],
            mode="markers+text",
            name="Après prise en compte du FDep",
            marker=dict(
                size=12,
                symbol="diamond",
                color=COLOR_RASPBERRY,
                line=dict(
                    color="white",
                    width=1.5,
                ),
            ),
            text=[
                f"{value:.2f}"
                for value in data["correlation_partielle_apl_fdep"]
            ],
            textposition=[
                "bottom right",
                "top center",
                "bottom center",
            ],
            textfont=dict(
                size=11,
                color=COLOR_TEXT,
            ),
            customdata=data["p_value_apl_apres_fdep"],
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Après prise en compte du FDep : <b>%{x:.2f}</b><br>"
                "p-value : %{customdata:.3f}"
                "<extra></extra>"
            ),
        )
    )

    # ========================================================
    # Ligne repère
    # ========================================================

    fig.add_vline(
        x=0,
        line_dash="dash",
        line_width=1.2,
        line_color="#9FB0C3",
    )

    # ========================================================
    # Mise en forme
    # ========================================================

    fig.update_layout(
        title=None,

        font=dict(
            family="Outfit, Arial, sans-serif",
            color=COLOR_TEXT,
            size=13,
        ),

        plot_bgcolor=PLOT_BACKGROUND,
        paper_bgcolor=PLOT_BACKGROUND,

        height=420,

        margin=dict(
            l=150,
            r=40,
            t=95,
            b=80,
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            title=None,
            font=dict(
                size=12,
                color=COLOR_TEXT,
            ),
            bgcolor="rgba(0,0,0,0)",
        ),
    )

    fig.update_xaxes(
        title=dict(
            text="Coefficient de corrélation avec l'APL (r)",
            font=dict(
                size=13,
                color=COLOR_MUTED,
            ),
        ),
        range=[-1, 1],
        tickvals=[-1, -0.5, 0, 0.5, 1],
        ticktext=["−1", "−0,5", "0", "0,5", "1"],
        showgrid=True,
        gridcolor=COLOR_GRID,
        gridwidth=1,
        zeroline=False,
        showline=False,
        tickfont=dict(
            color=COLOR_TEXT,
            size=12,
        ),
    )

    fig.update_yaxes(
        title=None,
        categoryorder="array",
        categoryarray=ordre[::-1],
        showgrid=False,
        showline=False,
        tickfont=dict(
            color=COLOR_TEXT,
            size=12,
        ),
    )

    return fig