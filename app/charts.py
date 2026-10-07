import pandas as pd
import plotly.graph_objects as go
import math

# ============================================================
# Identité graphique
# ============================================================

    # ============================================================
    # Indicateurs de santé
    # ============================================================

COLOR_HEALTH = "#4A84C2"       # Santé perçue
COLOR_LIMITATION = "#CA1C60"   # limitation activité
COLOR_DIABETE = "#EC9955"      # Diabète déclaré

    # ============================================================
    # Indicateurs territoriaux
    # ============================================================

COLOR_FDEP = "#884AA0"          # Défavorisation territoriale principale
COLOR_FEDI = "#C392D8"          # Même famille, plus clair
COLOR_APL = "#3EA36D"           # Accessibilité aux soins

    # ============================================================
    # Sexe
    # ============================================================

COLOR_SEX_ALL = "#7C8DA1"
COLOR_SEX_WOMEN = "#C74E6C"
COLOR_SEX_MEN = "#114B8A"

    # ============================================================
    # Autres dimensions
    # ============================================================

COLOR_FINANCE = "#357F57"       # Vert
COLOR_DIPLOME = "#C9A426"       # Ocre
COLOR_PCS = "#BD7A44"           # Brun

SYMBOL_FINANCE = "circle"
SYMBOL_DIPLOME = "diamond"
SYMBOL_PCS = "square"


    # ============================================================
    # Couleurs fonctionnelles
    # ============================================================

COLOR_NAVY = "#002B59"       # Structure / titres
COLOR_BLUE = "#114B8A"
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
        "color": COLOR_LIMITATION,
        "symbol": "diamond",
    },

    "Diabète déclaré": {
        "color": COLOR_DIABETE,
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
    "z_limitation": "Limitation d'activités",
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
            "label_complet": "Défavorisation territoriale — FDep",
            "color": COLOR_FDEP,
        },
        {
            "colonne": "z_fedi",
            "label": "F-EDI",
            "label_complet": "Défavorisation territoriale — F-EDI",
            "color": COLOR_FEDI,
        },
        {
            "colonne": "z_apl",
            "label": "Accessibilité faible",
            "label_complet": "Faible accessibilité aux médecins généralistes",
            "color": COLOR_APL,
        },
        {
            "colonne": "z_sante",
            "label": "Santé perçue défavorable",
            "label_complet": "Santé perçue défavorable",
            "color": COLOR_HEALTH,
        },
        {
            "colonne": "z_limitation",
            "label": "Limitations habituelles",
            "label_complet": "Limitation dans les activités habituelles",
            "color": COLOR_LIMITATION,
        },
        {
            "colonne": "z_diabete",
            "label": "Diabète déclaré",
            "label_complet": "Diabète déclaré",
            "color": COLOR_DIABETE,
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

        line_width=1.7,

        line_dash="dash",

        line_color="#7F92A6",
    )
    
    fig.add_annotation(
        x=-limite * 0.6,
        y=-0.23,
        xref="x",
        yref="paper",
        text="Plus favorable",
        showarrow=False,
        font=dict(
            size=10,
            color=COLOR_MUTED,
        ),
    )

    fig.add_annotation(
        x=limite * 0.6,
        y=-0.23,
        xref="x",
        yref="paper",
        text="Plus défavorable",
        showarrow=False,
        font=dict(
            size=10,
            color=COLOR_MUTED,
        ),
    )


    # ========================================================
    # Mise en forme
    # ========================================================

    fig.update_layout(
        dragmode=False,

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
            b=56,
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
        fixedrange=True,
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
        fixedrange=True,

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
                "La santé se dégrade avec "
                "les difficultés financières"
            ),

            "axe": "Situation financière perçue",
        },


        "diplome": {
            "colonne": "Diplôme",

            "ordre": [
                "Supérieur au Bac",
                "Bac",
                "Aucun diplôme ou inférieur au Bac",
            ],

            "titre": (
                "Le niveau de diplôme s’accompagne " 
                "d’écarts nets de santé"
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
                "Des écarts existent entre catégories, " 
                "sans gradient social continu"
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
    display_names = {
        "Santé perçue bonne ou très bonne": "Bonne ou très bonne santé perçue",
        "Limitation d'activité": "Limitation dans les activités habituelles",
        "Diabète déclaré": "Diabète déclaré",
    }
    
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

                name=display_names[indicateur],

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
        dragmode=False,
        title=dict(
            text=config["titre"],

            x=0,

            xanchor="left",

            font=dict(
                family="Outfit, Arial, sans-serif",
                size=18,
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


        height=500,


        margin=dict(
            l=70,
            r=30,
            t=160,
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
            
            itemclick=False,
            itemdoubleclick=False,
        ),


        showlegend=True,
    )


    # ========================================================
    # Axe X
    # ========================================================

    fig.update_xaxes(
    fixedrange=True,
    title=dict(
        text=config["axe"],
        font=dict(
            size=13,
            color=COLOR_MUTED,
        ),
        standoff=18,
    ),
    
    categoryorder="array",
    categoryarray=(
        [
            pcs_labels.get(value, value)
            for value in config["ordre"]
        ]
        if variable == "pcs"
        else config["ordre"]
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

    ticks="",
)

    # ========================================================
    # Axe Y
    # ========================================================

    fig.update_yaxes(
        fixedrange=True,
        title=dict(
            text="Part de la population (%)",
            font=dict(
                size=13,
                color=COLOR_MUTED,
            ),
            standoff=12,
        ),

        # Même échelle pour les trois dimensions sociales
        range=[0, 100],

        tickmode="array",
        tickvals=[0, 20, 40, 60, 80, 100],
        ticktext=[
            "0 %",
            "20 %",
            "40 %",
            "60 %",
            "80 %",
            "100 %",
        ],

        showgrid=True,
        gridcolor=COLOR_GRID,
        gridwidth=1,

        zeroline=False,
        showline=False,

        tickfont=dict(
            color=COLOR_TEXT,
            size=12,
        ),

        ticks="",
    )


    return fig

# ============================================================
# Focus diabète — âge et sexe
# ============================================================

def create_diabetes_age_sex_chart(data):
    """
    Visualise la part de personnes déclarant un diabète
    selon l'âge et le sexe.

    Les estimations non diffusées restent manquantes
    et ne sont pas représentées.
    """

    data_plot = data.copy()

    # ========================================================
    # Ordre des classes d'âge
    # ========================================================

    data_plot = data_plot.sort_values(
        [
            "ordre_age",
            "sexe",
        ]
    )

    ordre_age = (
        data_plot[
            ["classe_age", "ordre_age"]
        ]
        .drop_duplicates()
        .sort_values("ordre_age")
        ["classe_age"]
        .tolist()
    )


    # ========================================================
    # Configuration des trois séries
    # ========================================================

    styles = {

        "Tous": {
            "label": "Ensemble",
            "color": COLOR_SEX_ALL,
            "symbol": "circle",
            "dash": "dot",
            "width": 1.8,
            "opacity": 0.75,
        },

        "Femmes": {
            "label": "Femmes",
            "color": COLOR_SEX_WOMEN,
            "symbol": "diamond",
            "dash": "solid",
            "width": 2.7,
            "opacity": 1,
        },

        "Hommes": {
            "label": "Hommes",
            "color": COLOR_SEX_MEN,
            "symbol": "circle",
            "dash": "solid",
            "width": 2.7,
            "opacity": 1,
        },
    }


    # ========================================================
    # Figure
    # ========================================================

    fig = go.Figure()


    # ========================================================
    # Séries
    # ========================================================

    for sexe in [
        "Tous",
        "Femmes",
        "Hommes",
    ]:

        subset = data_plot[
            data_plot["sexe"] == sexe
        ].copy()

        if subset.empty:
            continue

        style = styles[sexe]

        fig.add_trace(
            go.Scatter(

                x=subset["classe_age"],

                y=subset["estimation"],

                mode="lines+markers",

                name=style["label"],

                connectgaps=False,

                line=dict(
                    color=style["color"],
                    width=style["width"],
                    dash=style["dash"],
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

                opacity=style["opacity"],

                error_y=dict(
                    type="data",
                    symmetric=False,

                    array=(
                        subset["ic_sup"]
                        - subset["estimation"]
                    ),

                    arrayminus=(
                        subset["estimation"]
                        - subset["ic_inf"]
                    ),

                    color=style["color"],
                    thickness=1.2,
                    width=4,
                ),

                customdata=list(
                    zip(
                        subset["ic_inf"],
                        subset["ic_sup"],
                        subset["effectif_brut"],
                    )
                ),

                hovertemplate=(
                    "<b>%{fullData.name}</b><br>"
                    "%{x}<br><br>"
                    "<b>%{y:.1f} %</b><br>"
                    "IC 95 % : "
                    "%{customdata[0]:.1f} – "
                    "%{customdata[1]:.1f} %<br>"
                    "Effectif brut : %{customdata[2]:,.0f}"
                    "<extra></extra>"
                ),
            )
        )


    # ========================================================
    # Mise en forme
    # ========================================================

    fig.update_layout(

        dragmode=False,

        title=dict(
            text=(
                "Avec l’âge, le diabète déclaré augmente "
                "plus fortement chez les hommes"
            ),

            x=0,
            xanchor="left",

            font=dict(
                family="Outfit, Arial, sans-serif",
                size=18,
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

        height=500,

        margin=dict(
            l=70,
            r=30,
            t=130,
            b=100,
        ),

        hovermode="closest",

        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#D5DEE8",

            font=dict(
                family="Outfit, Arial, sans-serif",
                color=COLOR_TEXT,
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

            itemclick=False,
            itemdoubleclick=False,
        ),
    )


    # ========================================================
    # Axe X
    # ========================================================

    fig.update_xaxes(

        fixedrange=True,

        title=dict(
            text="Classe d'âge",

            font=dict(
                size=13,
                color=COLOR_MUTED,
            ),

            standoff=18,
        ),

        categoryorder="array",
        categoryarray=ordre_age,

        showgrid=False,

        showline=True,
        linecolor="#D5DEE8",
        linewidth=1,

        tickfont=dict(
            color=COLOR_TEXT,
            size=11,
        ),

        ticks="",
    )


    # ========================================================
    # Axe Y
    # ========================================================

    max_value = data_plot["ic_sup"].max(
        skipna=True
    )

    y_max = math.ceil(
        max_value / 5
    ) * 5


    fig.update_yaxes(

        fixedrange=True,

        title=dict(
            text="Population déclarant un diabète (%)",

            font=dict(
                size=13,
                color=COLOR_MUTED,
            ),

            standoff=12,
        ),

        range=[
            0,
            y_max,
        ],

        dtick=5,

        ticksuffix=" %",

        showgrid=True,
        gridcolor=COLOR_GRID,
        gridwidth=1,

        zeroline=False,
        showline=False,

        tickfont=dict(
            color=COLOR_TEXT,
            size=12,
        ),

        ticks="",
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
                "Une plus forte défavorisation est associée "
                "à une moins bonne santé perçue"
            ),
            "color": COLOR_HEALTH,
        },

        "limitation": {
            "colonne": "limitation_activite",
            "libelle": "Limitation d'activité",
            "axe_y": "Population limitée dans ses activités habituelles (%)",
            "titre": (
                "Les limitations progressent avec la défavorisation, "
                "mais de façon moins régulière"
            ),
            "color": COLOR_LIMITATION,
        },

        "diabete": {
            "colonne": "diabete_declare",
            "libelle": "Diabète déclaré",
            "axe_y": "Population déclarant un diabète (%)",
            "titre": (
                "Le diabète déclaré est plus fréquent "
                "dans les régions plus défavorisées"
            ),
            "color": COLOR_DIABETE,
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
    # Bornes de l'axe Y
    # --------------------------------------------------------
    

    Y_RANGE_FDEP = [-6, 6]
    Y_TICKS_FDEP = [-6, -4, -2, 0, 2, 4, 6]

    # --------------------------------------------------------
    # Bornes de l'axe X
    # --------------------------------------------------------
    
    X_RANGE_FDEP = [-1.0, 0.75]
    X_TICKS_FDEP = [-1.0, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75]
    
    # --------------------------------------------------------
    # Mise en forme
    # --------------------------------------------------------

    fig.update_layout(
        dragmode=False,
        title=dict(
            text=config["titre"],
            x=0,
            xanchor="left",

            font=dict(
                family="Outfit, Arial, sans-serif",
                size=18,
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
    )

    # --------------------------------------------------------
    # Axe X
    # --------------------------------------------------------

    fig.update_xaxes(
        fixedrange=True,
        title=dict(
            text="Indice FDep",
            standoff=65,

            font=dict(
                size=13,
                color=COLOR_MUTED,
            ),
        ),

        range=X_RANGE_FDEP,
        
        tickmode="array",
        tickvals=X_TICKS_FDEP,

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
        fixedrange=True,
        title=dict(
            text="Écart à la moyenne régionale (points de %)",

            font=dict(
                size=13,
                color=COLOR_MUTED,
            ),
        ),

        range=Y_RANGE_FDEP,

        tickmode="array",
        tickvals=Y_TICKS_FDEP,
        ticktext=[
            "−6 pt",
            "−4 pt",
            "−2 pt",
            "0 pt",
            "2 pt",
            "4 pt",
            "6 pt",
        ],

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

        ticks="",
    )

    # --------------------------------------------------------
    # Aide à la lecture du FDep
    # --------------------------------------------------------

    aide_color = "#98A8B8"
    
    x_min, x_max = X_RANGE_FDEP

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
        "Limitation d'activité": "Limitations dans les activités habituelles",
        "Diabète déclaré": "Diabète déclaré",
    }

    data = relations.copy()
    data["label"] = data["indicateur"].map(labels)

    ordre = [
        "Santé perçue",
        "Limitations dans les activités habituelles",
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
            name="Association brute avec l'APL",
            marker=dict(
                size=12,
                symbol="circle",
                color=COLOR_APL,
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
                color=COLOR_FDEP,
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
    # Ligne repère verticale sur 0
    # ========================================================

    fig.add_vline(
        x=0,
        line_dash="dash",
        line_width=1.4,
        line_color="#9FB0C3",
    )

    # ========================================================
    # Séparateurs horizontaux entre indicateurs
    # ========================================================

    fig.add_shape(
        type="line",
        x0=-1,
        x1=1,
        y0=0.5,
        y1=0.5,
        xref="x",
        yref="y",
        line=dict(
            color="#EEF2F6",
            width=1,
        ),
        layer="below",
    )

    fig.add_shape(
        type="line",
        x0=-1,
        x1=1,
        y0=1.5,
        y1=1.5,
        xref="x",
        yref="y",
        line=dict(
            color="#EEF2F6",
            width=1,
        ),
        layer="below",
    )

    # ========================================================
    # Mise en forme
    # ========================================================

    fig.update_layout(
        dragmode=False,
        title=None,

        font=dict(
            family="Outfit, Arial, sans-serif",
            color=COLOR_TEXT,
            size=13,
        ),

        plot_bgcolor=PLOT_BACKGROUND,
        paper_bgcolor=PLOT_BACKGROUND,

        height=430,

        margin=dict(
            l=150,
            r=35,
            t=75,
            b=80,
        ),

        legend=dict(
            orientation="h",
            
            yanchor="bottom",
            y=1.08,
            
            xanchor="center",
            x=0.5,
            
            title=None,
            
            font=dict(
                size=12,
                color=COLOR_TEXT,
            ),
            
            bgcolor="rgba(255,255,255,0.88)",
            bordercolor="#D5DEE8",
            borderwidth=1,
            
            itemclick=False,
            itemdoubleclick=False,
        ),

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
        fixedrange=True,
        title=dict(
            text="Coefficient de corrélation avec l'APL (r)",
            font=dict(
                size=13,
                color=COLOR_MUTED,
            ),
            standoff=14,
        ),
        
        range=[-1, 1],
        
        tickvals=[-1, -0.5, 0, 0.5, 1],
        ticktext=["−1", "−0,5", "0", "0,5", "1"],
        
        showgrid=True,
        gridcolor=COLOR_GRID,
        gridwidth=1,
        
        zeroline=False,

        showline=True,
        linecolor="#D5DEE8",
        linewidth=1,

        ticks="outside",
        ticklen=4,
        tickcolor="#B8C4D0",

        tickfont=dict(
            color=COLOR_TEXT,
            size=12,
        ),
    )

    # ========================================================
    # Axe Y
    # ========================================================

    fig.update_yaxes(
        fixedrange=True,
        title=None,
        
        categoryorder="array",
        categoryarray=ordre[::-1],
        
        # Même espace au-dessus de Santé perçue
        # et sous Diabète déclaré
        range=[-0.5, 2.5],
    
        showgrid=False,
        showline=False,
        ticks="",
        
        tickfont=dict(
            color=COLOR_TEXT,
            size=12,
        ),
    )

    return fig