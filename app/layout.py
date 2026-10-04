from dash import dcc, html

from charts import (
    create_social_chart,
    create_fdep_health_chart,
    create_apl_comparison_chart,
)


# ============================================================
# ACCUEIL
# ============================================================

def create_home_tab():

    return html.Div([

        # ----------------------------------------------------
        # Introduction
        # ----------------------------------------------------

        html.P(
            "ODISSÉ DATAVIZ CHALLENGE 2026",
            className="eyebrow",
        ),

        html.H1(
            "Inégalités sociales et territoriales de santé"
        ),

        html.P(
            "Selon notre situation sociale et notre territoire de vie, "
            "nous ne sommes pas tous exposés aux mêmes conditions de santé. "
            "Cette datavisualisation explore comment contexte social, "
            "défavorisation territoriale, accessibilité aux soins et état "
            "de santé se combinent en France.",
            className="intro",
        ),

        # ----------------------------------------------------
        # Problématique
        # ----------------------------------------------------

        html.Div([

            html.P(
                "QUESTION DE DÉPART",
                className="section-label",
            ),

            html.H2(
                "Comment les inégalités sociales et territoriales de santé "
                "se combinent-elles avec l'accessibilité aux soins pour "
                "caractériser différents profils de territoires en France ?"
            ),

        ], className="question-block"),

        # ----------------------------------------------------
        # Parcours
        # ----------------------------------------------------

        html.H2(
            "Du constat social aux profils territoriaux"
        ),

        html.Div([

            html.Div([
                html.P("01", className="step-number"),
                html.H3("Inégalités sociales"),
                html.P(
                    "Observer comment plusieurs dimensions sociales — situation "
                    "financière, diplôme et catégorie socioprofessionnelle — "
                    "s'accompagnent de différences de santé."
                ),
            ], className="step-card"),

            html.Div([
                html.P("02", className="step-number"),
                html.H3("Territoires & soins"),
                html.P(
                        "Examiner si la défavorisation des territoires et "
                        "l'accessibilité aux médecins généralistes sont associées "
                        "aux différences de santé observées entre régions."
                    ),
            ], className="step-card"),

            html.Div([
                html.P("03", className="step-number"),
                html.H3("Profils territoriaux"),
                html.P(
                    "Combiner six indicateurs pour faire émerger différentes "
                    "configurations régionales et comprendre ce qui les distingue."
                ),
            ], className="step-card"),

        ], className="steps"),

        # ----------------------------------------------------
        # Données
        # ----------------------------------------------------

        html.Div([

            html.H2("Données mobilisées"),

            html.P(
                "Cette exploration croise plusieurs sources publiques portant "
                "sur la santé, la défavorisation sociale, l'accessibilité aux "
                "médecins généralistes et la population."
            ),

            html.Ul([

                html.Li([
                    html.A(
                        "Santé générale — Baromètre 2024",
                        href=(
                            "https://odisse.santepubliquefrance.fr/"
                            "explore/assets/"
                            "sante_generale_indicateurs_barometre_2024/"
                        ),
                        target="_blank",
                    ),
                    " · Santé publique France — Odissé",
                ]),

                html.Li([
                    html.A(
                        "Diabète — Baromètre 2024",
                        href=(
                            "https://odisse.santepubliquefrance.fr/"
                            "explore/assets/"
                            "diabete-indicateurs-du-barometre-2024/"
                        ),
                        target="_blank",
                    ),
                    " · Santé publique France — Odissé",
                ]),

                html.Li([
                    html.A(
                        "Indice de défavorisation sociale FDep",
                        href=(
                            "https://odisse.santepubliquefrance.fr/"
                            "explore/assets/"
                            "indice-de-defavorisation-sociale-fdep-par-commune/"
                        ),
                        target="_blank",
                    ),
                    " · Santé publique France — Odissé",
                ]),

                html.Li([
                    html.A(
                        "French European Deprivation Index (F-EDI) 2021",
                        href=(
                            "https://odisse.santepubliquefrance.fr/"
                            "explore/assets/"
                            "french-european-deprivation-index-f-edi-2021-par-commune/"
                        ),
                        target="_blank",
                    ),
                    " · Santé publique France — Odissé",
                ]),

                html.Li([
                    html.A(
                        "Accessibilité potentielle localisée (APL) "
                        "aux médecins généralistes",
                        href=(
                            "https://www.observatoire-des-territoires.gouv.fr/"
                            "accessibilite-potentielle-localisee-apl-"
                            "aux-medecins-generalistes"
                        ),
                        target="_blank",
                    ),
                    " · Observatoire des territoires",
                ]),

                html.Li([
                    html.A(
                        "Populations 2023",
                        href="https://www.insee.fr/fr/statistiques/8680726",
                        target="_blank",
                    ),
                    " · Insee",
                ]),

            ], className="sources-list"),

        ], className="sources-block"),

        # ----------------------------------------------------
        # Challenge
        # ----------------------------------------------------

        html.Div([

            html.H2(
                "À propos du projet"
            ),

            html.P(
                "Cette datavisualisation a été réalisée dans le cadre de "
                "l'Odissé Dataviz Challenge 2026. Elle propose une exploration "
                "des inégalités sociales et territoriales de santé à partir "
                "de données publiques françaises."
            ),

        ], className="about-challenge"),

    ], className="tab-content")


# ============================================================
# 01 — INÉGALITÉS SOCIALES
# ============================================================

def create_social_summary(synthese_sociale):

    dimensions = [
        "finance",
        "diplome",
        "pcs",
    ]

    indicateurs = [
        "Santé perçue bonne ou très bonne",
        "Limitation d'activité",
        "Diabète déclaré",
    ]

    labels_indicateurs = {
        "Santé perçue bonne ou très bonne": "Santé perçue",
        "Limitation d'activité": "Limitation",
        "Diabète déclaré": "Diabète",
    }

    def format_number(value):
        return f"{value:.1f}".replace(".", ",")

    cards = []

    # ========================================================
    # Une carte par dimension sociale
    # ========================================================

    for dimension in dimensions:

        donnees_dimension = synthese_sociale[
            synthese_sociale["dimension"] == dimension
        ].copy()

        if donnees_dimension.empty:
            continue

        dimension_label = donnees_dimension[
            "dimension_label"
        ].iloc[0]

        comparaisons = (
            donnees_dimension[
                ["groupe_reference", "groupe_comparaison"]
            ]
            .drop_duplicates()
        )

        # ----------------------------------------------------
        # Sous-titre
        # ----------------------------------------------------

        if len(comparaisons) == 1:

            groupe_reference = comparaisons.iloc[0][
                "groupe_reference"
            ]

            groupe_comparaison = comparaisons.iloc[0][
                "groupe_comparaison"
            ]

            sous_titre = (
                f"{groupe_comparaison} "
                f"par rapport à {groupe_reference}"
            )

        else:

            sous_titre = (
                "Écart entre les catégories présentant "
                "les valeurs extrêmes"
            )

        # ----------------------------------------------------
        # Lignes d'indicateurs
        # ----------------------------------------------------

        indicateurs_elements = []

        for indicateur in indicateurs:

            ligne = donnees_dimension[
                donnees_dimension["indicateur"] == indicateur
            ]

            if ligne.empty:
                continue

            ligne = ligne.iloc[0]

            ecart = ligne["ecart"]

            valeur_reference = ligne["valeur_reference"]
            valeur_comparaison = ligne["valeur_comparaison"]

            groupe_reference = ligne["groupe_reference"]
            groupe_comparaison = ligne["groupe_comparaison"]

            type_comparaison = ligne["type_comparaison"]

            # ------------------------------------------------
            # Valeur principale
            # ------------------------------------------------

            if type_comparaison == "extremes_observes":

                valeur_ecart = (
                    f"{format_number(abs(ecart))} pts"
                )

                detail = (
                    f"{groupe_comparaison} "
                    f"{format_number(valeur_comparaison)} % "
                    f"↔ {groupe_reference} "
                    f"{format_number(valeur_reference)} %"
                )

            else:

                signe = "+" if ecart > 0 else "−"

                valeur_ecart = (
                    f"{signe}{format_number(abs(ecart))} pts"
                )

                detail = (
                    f"{format_number(valeur_comparaison)} % "
                    f"contre "
                    f"{format_number(valeur_reference)} %"
                )

            indicateurs_elements.append(

                html.Div(
                    [

                        html.Div(
                            [
                                html.Span(
                                    labels_indicateurs[indicateur],
                                    className="summary-indicator-name",
                                ),

                                html.Strong(
                                    valeur_ecart,
                                    className="summary-value",
                                ),
                            ],
                            className="summary-indicator-top",
                        ),

                        html.Span(
                            detail,
                            className="summary-detail",
                        ),

                    ],
                    className="summary-indicator",
                )
            )

        # ----------------------------------------------------
        # Carte
        # ----------------------------------------------------

        cards.append(

            html.Div(
                [

                    html.Div(
                        [
                            html.H3(
                                dimension_label,
                                className="summary-card-title",
                            ),

                            html.P(
                                sous_titre,
                                className="summary-card-subtitle",
                            ),
                        ],
                        className="summary-card-header",
                    ),

                    html.Div(
                        indicateurs_elements,
                        className="summary-indicators",
                    ),

                ],
                className=f"summary-card summary-card-{dimension}",
            )
        )

    return html.Div(
        cards,
        className="summary-cards",
    )

def create_social_tab(finance, synthese_sociale):

    return html.Div([

        # ----------------------------------------------------
        # Introduction
        # ----------------------------------------------------

        html.P(
            "01 — INÉGALITÉS SOCIALES",
            className="section-label",
        ),

        html.H1(
            "Les inégalités sociales apparaissent-elles "
            "sur plusieurs dimensions de santé ?"
        ),

        html.P(
            "Le Baromètre 2024 permet d'observer les différences "
            "de santé selon plusieurs caractéristiques sociales. "
            "Trois dimensions sont explorées ici : la situation "
            "financière perçue, le niveau de diplôme et la catégorie "
            "socioprofessionnelle.",
            className="intro",
        ),

        # ----------------------------------------------------
        # Repères de lecture
        # ----------------------------------------------------

        html.Div([

            html.H3("Trois indicateurs de santé"),

            html.Div([

                html.Div([
                    html.Strong("Santé perçue"),
                    html.P(
                        "Part déclarant une santé bonne "
                        "ou très bonne."
                    ),
                    html.P(
                        "↑ valeur élevée = situation plus favorable",
                        className="indicator-direction",
                    ),
                ], className="indicator-card"),

                html.Div([
                    html.Strong("Limitation d'activité"),
                    html.P(
                        "Part déclarant une limitation d'activité."
                    ),
                    html.P(
                        "↑ valeur élevée = situation plus défavorable",
                        className="indicator-direction",
                    ),
                ], className="indicator-card"),

                html.Div([
                    html.Strong("Diabète déclaré"),
                    html.P(
                        "Part déclarant un diabète."
                    ),
                    html.P(
                        "↑ valeur élevée = situation plus défavorable",
                        className="indicator-direction",
                    ),
                ], className="indicator-card"),

            ], className="indicator-grid"),

        ], className="reading-guide"),

        # ----------------------------------------------------
        # Exploration
        # ----------------------------------------------------

        html.H2(
            "Explorez les écarts selon la situation sociale"
        ),

        html.P(
            "Sélectionnez une dimension sociale pour comparer "
            "les trois indicateurs de santé."
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
            className="selector",
        ),

        dcc.Graph(
            id="social-chart",
            figure=create_social_chart(
                finance,
                "finance",
            ),
            config = {"displayModeBar": False },
            className="chart-container",
        ),

        html.P(
            "Les estimations sont accompagnées de leur "
            "intervalle de confiance à 95 %.",
            className="graph-note",
        ),

        # ----------------------------------------------------
        # Synthèse
        # ----------------------------------------------------

        html.Div([

            html.H2(
                "Des écarts qui concernent plusieurs "
                "dimensions de santé"
            ),

            html.P(
                "Les écarts entre les situations comparées "
                "apparaissent dans les trois indicateurs étudiés."
            ),

            create_social_summary(synthese_sociale),

            html.P(
                "* Pour la catégorie socioprofessionnelle, les valeurs "
                "correspondent à l'écart entre les catégories présentant "
                "les valeurs extrêmes observées. Les PCS ne constituent "
                "pas une échelle sociale continue.",
                className="note",
            ),

        ], className="social-summary"),

        # ----------------------------------------------------
        # À retenir
        # ----------------------------------------------------

        html.Div([

            html.P(
                "À RETENIR",
                className="section-label",
            ),

            html.P(
                "Les écarts de santé apparaissent selon plusieurs dimensions sociales. "
                "Ils sont particulièrement marqués selon la situation financière et le niveau de diplôme : "
                "les situations les moins favorables s'accompagnent d'une moins bonne santé perçue et de niveaux plus élevés de limitation d'activité et de diabète déclaré. "
                "Les différences entre catégories socioprofessionnelles vont également dans ce sens, sans constituer un gradient social continu."
            ),

        ], className="takeaway"),

        # ----------------------------------------------------
        # Précautions
        # ----------------------------------------------------

        html.Div([

            html.H3("Précautions de lecture"),

            html.P(
                "Ces résultats décrivent des différences observées "
                "entre groupes. Ils ne permettent pas, à eux seuls, "
                "d'établir qu'une caractéristique sociale est la cause "
                "des différences de santé observées."
            ),

        ], className="method-note"),

        # ----------------------------------------------------
        # Sources
        # ----------------------------------------------------

        html.Div([

            html.Strong("Sources : "),

            html.A(
                "Santé générale — Baromètre 2024",
                href=(
                    "https://odisse.santepubliquefrance.fr/"
                    "explore/assets/"
                    "sante_generale_indicateurs_barometre_2024/"
                ),
                target="_blank",
            ),

            html.Span(" · "),

            html.A(
                "Diabète — Baromètre 2024",
                href=(
                    "https://odisse.santepubliquefrance.fr/"
                    "explore/assets/"
                    "diabete-indicateurs-du-barometre-2024/"
                ),
                target="_blank",
            ),

            html.Span(" — Santé publique France, Odissé."),

        ], className="sources"),

        # ----------------------------------------------------
        # Transition
        # ----------------------------------------------------

        html.Div([

            html.P(
                "Ces différences apparaissent entre groupes sociaux. "
                "Mais observe-t-on également des écarts de santé entre "
                "territoires aux caractéristiques sociales différentes ?"
            ),

        ], className="transition"),

    ], className="tab-content")

# ============================================================
# 02 — TERRITOIRES & SOINS
# ============================================================

def create_territorial_tab(
    analyse_regions,
    relations_territoriales,
):

    return html.Div([

        # ----------------------------------------------------
        # Introduction
        # ----------------------------------------------------

        html.P(
            "02 — TERRITOIRES & SOINS",
            className="section-label",
        ),

        html.H1(
            "Les inégalités de santé se retrouvent-elles "
            "à l'échelle des territoires ?"
        ),

        html.P(
            "Après avoir observé des différences de santé entre groupes sociaux, "
            "l'analyse se déplace à l'échelle territoriale. Les 13 régions "
            "métropolitaines sont comparées selon leur niveau de défavorisation, "
            "leur accessibilité aux médecins généralistes et leurs indicateurs "
            "de santé.",
            className="intro",
        ),

        # ----------------------------------------------------
        # FDep
        # ----------------------------------------------------

        html.H2(
            "Défavorisation territoriale et santé"
        ),

        html.P(
            "Les régions plus défavorisées présentent-elles "
            "des indicateurs de santé différents ?"
        ),

        # Repère de lecture FDep

        html.Div([

            html.Strong(
                "FDep — défavorisation territoriale"
            ),

            html.P(
                "Le FDep est un indice synthétique construit à partir de "
                "caractéristiques socio-économiques des territoires. "
                "Une valeur plus élevée correspond à un territoire "
                "plus défavorisé."
            ),

            html.P(
                "Il caractérise le contexte socio-économique d'un territoire "
                "et non la situation sociale individuelle de ses habitants.",
                className="indicator-direction",
            ),

        ], className="reading-guide"),

        # Sélecteur

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
            className="selector",
        ),

        # Graphique FDep

        dcc.Graph(
            id="fdep-health-chart",
            figure=create_fdep_health_chart(
                analyse_regions,
                relations_territoriales,
                "sante",
            ),
            config = {"displayModeBar": False },
            className="chart-container",
        ),

        html.P(
            "Lecture : chaque point représente une région métropolitaine. "
            "L’axe vertical indique l’écart à la moyenne des 13 régions : "
            "une valeur positive correspond à un niveau supérieur à la moyenne, "
            "une valeur négative à un niveau inférieur. "
            "Le coefficient r mesure l’intensité et le sens de la relation linéaire "
            "entre la défavorisation territoriale et l’indicateur de santé.",
            className="graph-note",
        ),

        # Commentaire dynamique
        # Le contenu sera piloté par le même sélecteur que le graphique.

        html.Div(
            id="fdep-interpretation",
            className="result-note",
        ),

        # ----------------------------------------------------
        # APL
        # ----------------------------------------------------

        html.H2(
            "Accessibilité aux soins"
        ),

        html.P(
            "L'accessibilité aux médecins généralistes apporte-t-elle "
            "une information supplémentaire à la défavorisation territoriale ?"
        ),

        # Repère de lecture APL

        html.Div([

            html.Strong(
                "APL — accessibilité aux médecins généralistes"
            ),

            html.P(
                "L'Accessibilité potentielle localisée mesure l'accessibilité "
                "à l'offre de médecins généralistes en tenant compte de l'offre "
                "disponible et de la demande potentielle. Une valeur plus élevée "
                "correspond à une meilleure accessibilité."
            ),

        ], className="reading-guide"),

        # Explication de l'ajustement

        html.Div([

            html.Strong(
                "Pourquoi prendre en compte le FDep ?"
            ),

            html.P(
                "L'objectif est d'examiner si la relation entre accessibilité "
                "aux soins et santé subsiste une fois isolée statistiquement "
                "la relation linéaire avec la défavorisation territoriale."
            ),

        ], className="method-note"),

        # Graphique APL

        dcc.Graph(
            id="apl-comparison-chart",
            figure=create_apl_comparison_chart(
                relations_territoriales
            ),
            config = {"displayModeBar": False },
            className="chart-container",
        ),
        
        html.P(
            "Lecture : chaque ligne compare la corrélation entre l’APL et un indicateur de santé, "
            "avant puis après prise en compte du FDep. Plus r est proche de −1 ou de +1, plus la relation "
            "linéaire est marquée ; une valeur proche de 0 traduit une relation faible. "
            "Ici, la limitation d’activité reste l’indicateur le plus lié à l’APL après prise en compte "
            "de la défavorisation territoriale.",
            className="graph-note",
        ),

        # ----------------------------------------------------
        # À retenir
        # ----------------------------------------------------

        html.Div([

            html.P(
                "À RETENIR",
                className="section-label",
            ),

            html.P(
                "La défavorisation territoriale est nettement associée à "
                "plusieurs indicateurs de santé, notamment la santé perçue "
                "et le diabète déclaré. L'accessibilité aux médecins "
                "généralistes apporte une lecture différente : après prise "
                "en compte du FDep, la relation la plus marquée concerne "
                "la limitation d'activité, mais elle reste incertaine compte "
                "tenu du faible nombre de régions étudiées."
            ),

        ], className="takeaway"),

        # ----------------------------------------------------
        # Précautions
        # ----------------------------------------------------

        html.Div([

            html.H3(
                "Précautions de lecture"
            ),

            html.P(
                "Ces analyses sont exploratoires et portent sur 13 régions "
                "métropolitaines. Les corrélations décrivent des associations "
                "entre caractéristiques régionales et ne permettent d'établir "
                "ni causalité ni relation individuelle. Avec seulement "
                "13 observations, les résultats doivent être interprétés "
                "avec prudence."
            ),

        ], className="method-note"),

        # ----------------------------------------------------
        # Sources
        # ----------------------------------------------------

        html.Div([

            html.Strong("Sources : "),

            html.A(
                "Indice de défavorisation sociale FDep",
                href=(
                    "https://odisse.santepubliquefrance.fr/"
                    "explore/assets/"
                    "indice-de-defavorisation-sociale-fdep-par-commune/"
                ),
                target="_blank",
            ),

            html.Span(" · "),

            html.A(
                "Accessibilité potentielle localisée (APL)",
                href=(
                    "https://www.observatoire-des-territoires.gouv.fr/"
                    "accessibilite-potentielle-localisee-apl-"
                    "aux-medecins-generalistes"
                ),
                target="_blank",
            ),

            html.Span(" · "),

            html.A(
                "Santé générale — Baromètre 2024",
                href=(
                    "https://odisse.santepubliquefrance.fr/"
                    "explore/assets/"
                    "sante_generale_indicateurs_barometre_2024/"
                ),
                target="_blank",
            ),

            html.Span(" · "),

            html.A(
                "Diabète — Baromètre 2024",
                href=(
                    "https://odisse.santepubliquefrance.fr/"
                    "explore/assets/"
                    "diabete-indicateurs-du-barometre-2024/"
                ),
                target="_blank",
            ),

            html.Span(
                " — Santé publique France, Odissé "
                "et Observatoire des territoires."
            ),

        ], className="sources"),

        # ----------------------------------------------------
        # Transition
        # ----------------------------------------------------

        html.Div([

            html.P(
                "Les territoires ne se distinguent donc pas selon une seule "
                "dimension. Que se passe-t-il lorsque défavorisation, "
                "accessibilité aux soins et état de santé sont considérés "
                "simultanément ?"
            ),

        ], className="transition"),

    ], className="tab-content")


# ============================================================
# 03 — PROFILS TERRITORIAUX
# ============================================================

# ============================================================
# Helpers — Profils territoriaux
# ============================================================

def format_regions(regions):
    """Formate proprement une liste de régions en français."""

    regions = list(regions)

    if len(regions) == 1:
        return regions[0]

    if len(regions) == 2:
        return f"{regions[0]} et {regions[1]}"

    return (
        ", ".join(regions[:-1])
        + f" et {regions[-1]}"
    )


def describe_profile(profil):
    """
    Produit une description accessible d'un profil
    à partir de ses scores standardisés moyens.

    Convention :
    score positif = situation relativement plus défavorable
    score négatif = situation relativement plus favorable.
    """

    seuil = 0.25

    # --------------------------------------------------------
    # FDep
    # --------------------------------------------------------

    if profil["z_fdep"] > seuil:
        fdep = "un niveau de défavorisation FDep supérieur à la moyenne"

    elif profil["z_fdep"] < -seuil:
        fdep = "un niveau de défavorisation FDep inférieur à la moyenne"

    else:
        fdep = "un niveau de défavorisation FDep proche de la moyenne"


    # --------------------------------------------------------
    # F-EDI
    # --------------------------------------------------------

    if profil["z_fedi"] > seuil:
        fedi = "un F-EDI relativement plus défavorable"

    elif profil["z_fedi"] < -seuil:
        fedi = "un F-EDI relativement plus favorable"

    else:
        fedi = "un F-EDI proche de la moyenne"


    # --------------------------------------------------------
    # Accessibilité
    # z_apl positif = faible accessibilité
    # --------------------------------------------------------

    if profil["z_apl"] > seuil:
        apl = "une accessibilité aux médecins généralistes plus faible"

    elif profil["z_apl"] < -seuil:
        apl = "une accessibilité aux médecins généralistes meilleure"

    else:
        apl = "une accessibilité aux médecins généralistes proche de la moyenne"


    # --------------------------------------------------------
    # Santé
    # --------------------------------------------------------

    score_sante = (
        profil["z_sante"]
        + profil["z_limitation"]
        + profil["z_diabete"]
    ) / 3

    if score_sante > seuil:
        sante = "des indicateurs de santé globalement moins favorables"

    elif score_sante < -seuil:
        sante = "des indicateurs de santé globalement plus favorables"

    else:
        sante = "des indicateurs de santé globalement proches de la moyenne"


    return (
        "Par rapport aux 13 régions étudiées, ce profil associe "
        f"{fdep}, {fedi}, {apl} et {sante}."
    )


def create_profile_cards(regions, profils_clusters):
    """Construit les quatre cartes de profils à partir des exports R."""

    cards = []

    profils = profils_clusters.sort_values(
        "clust"
    )

    for _, profil in profils.iterrows():

        cluster = int(
            profil["clust"]
        )

        regions_cluster = (
            regions.loc[
                regions["clust"] == cluster,
                "region"
            ]
            .sort_values()
            .tolist()
        )

        nb_regions = len(regions_cluster)

        label_regions = (
            "1 région"
            if nb_regions == 1
            else f"{nb_regions} régions"
        )

        cards.append(
            html.Div(
                [

                    # ----------------------------------------
                    # Haut de carte
                    # ----------------------------------------

                    html.Div(
                        [
                            html.Span(
                                f"PROFIL {cluster}",
                                className="profile-number",
                            ),

                            html.Span(
                                label_regions,
                                className="profile-count",
                            ),
                        ],
                        className="profile-card-top",
                    ),


                    # ----------------------------------------
                    # Nom
                    # ----------------------------------------

                    html.H3(
                        profil["profil"],
                        className="profile-title",
                    ),


                    # ----------------------------------------
                    # Description
                    # ----------------------------------------

                    html.P(
                        describe_profile(profil),
                        className="profile-description",
                    ),


                    # ----------------------------------------
                    # Régions
                    # ----------------------------------------

                    html.Div(
                        [
                            html.Span(
                                "RÉGIONS",
                                className="profile-regions-label",
                            ),

                            html.P(
                                format_regions(regions_cluster),
                                className="profile-regions",
                            ),
                        ],
                        className="profile-regions-block",
                    ),

                ],
                className=(
                    f"profile-card "
                    f"profile-card-{cluster}"
                ),
            )
        )

    return html.Div(
        cards,
        className="profiles-grid",
    )


# ============================================================
# 03 — PROFILS TERRITORIAUX
# ============================================================

def create_profiles_tab(
    map_figure,
    regions,
    profils_clusters,
):

    return html.Div([

        # ====================================================
        # INTRODUCTION
        # ====================================================

        html.P(
            "03 — PROFILS TERRITORIAUX",
            className="section-label",
        ),

        html.H1(
            "Comment ces dimensions se combinent-elles "
            "selon les régions ?"
        ),

        html.P(
            "Les analyses précédentes ont étudié séparément la "
            "défavorisation territoriale, l'accessibilité aux soins "
            "et les indicateurs de santé. Cette dernière étape les "
            "considère simultanément afin d'identifier différentes "
            "configurations territoriales.",
            className="intro",
        ),


        # ====================================================
        # MÉTHODE
        # ====================================================

        html.Div(
            [

                html.Div(
                    [
                        html.P(
                            "COMMENT SONT CONSTRUITS LES PROFILS ?",
                            className="method-flow-eyebrow",
                        ),

                        html.H2(
                            "Six indicateurs, une lecture commune"
                        ),

                        html.P(
                            "Les 13 régions métropolitaines sont comparées à partir "
                            "de dimensions sociales, sanitaires et d'accessibilité "
                            "aux médecins généralistes.",
                            className="method-flow-intro",
                        ),
                    ],
                    className="method-flow-header",
                ),


                html.Div(
                    [

                        # ----------------------------------------
                        # Étape 1
                        # ----------------------------------------

                        html.Div(
                            [
                                html.Span(
                                    "01",
                                    className="method-step-number",
                                ),

                                html.Strong(
                                    "Décrire les territoires"
                                ),

                                html.Div(
                                    [
                                        html.P([
                                            html.B("Défavorisation"),
                                            html.Br(),
                                            "FDep · F-EDI",
                                        ]),

                                        html.P([
                                            html.B("Accessibilité"),
                                            html.Br(),
                                            "APL médecins généralistes",
                                        ]),

                                        html.P([
                                            html.B("Santé"),
                                            html.Br(),
                                            "Santé perçue · limitation · diabète",
                                        ]),
                                    ],
                                    className="method-dimensions",
                                ),
                            ],
                            className="method-step",
                        ),


                        html.Div(
                            "→",
                            className="method-arrow",
                        ),


                        # ----------------------------------------
                        # Étape 2
                        # ----------------------------------------

                        html.Div(
                            [
                                html.Span(
                                    "02",
                                    className="method-step-number",
                                ),

                                html.Strong(
                                    "Mettre sur une même échelle"
                                ),

                                html.P(
                                    "Les six indicateurs sont standardisés "
                                    "pour rendre leurs positions relatives comparables."
                                ),
                            ],
                            className="method-step",
                        ),


                        html.Div(
                            "→",
                            className="method-arrow",
                        ),


                        # ----------------------------------------
                        # Étape 3
                        # ----------------------------------------

                        html.Div(
                            [
                                html.Span(
                                    "03",
                                    className="method-step-number",
                                ),

                                html.Strong(
                                    "Regrouper les profils proches"
                                ),

                                html.P(
                                    "Une classification exploratoire rapproche "
                                    "les régions présentant les configurations "
                                    "les plus similaires."
                                ),
                            ],
                            className="method-step",
                        ),


                        html.Div(
                            "→",
                            className="method-arrow",
                        ),


                        # ----------------------------------------
                        # Résultat
                        # ----------------------------------------

                        html.Div(
                            [
                                html.Span(
                                    "04",
                                    className="method-step-number",
                                ),

                                html.Strong(
                                    "Faire émerger 4 profils"
                                ),

                                html.P(
                                    "Ils décrivent des combinaisons territoriales "
                                    "différentes, sans constituer un classement."
                                ),
                            ],
                            className="method-step method-step-result",
                        ),

                    ],
                    className="method-flow",
                ),

            ],
            className="method-flow-block",
        ),

        # ====================================================
        # LES QUATRE PROFILS
        # ====================================================

        html.H2(
            "Quatre profils territoriaux se dégagent"
        ),

        html.P(
            "Ces profils ne constituent pas un classement des régions. "
            "Ils décrivent différentes combinaisons de défavorisation "
            "territoriale, d'accessibilité aux médecins généralistes "
            "et d'indicateurs de santé."
        ),

        create_profile_cards(
            regions,
            profils_clusters,
        ),


        # ====================================================
        # EXPLORATION INTERACTIVE
        # ====================================================

        html.H2(
            "Explorer les profils région par région"
        ),

        html.P(
            "Cliquez sur une région de la carte pour afficher "
            "ses indicateurs et situer son profil par rapport "
            "aux 13 régions étudiées."
        ),


        html.Div(
            [

                # ============================================
                # COLONNE GAUCHE — CARTE
                # ============================================

                html.Div(
                    [

                        dcc.Graph(
                            id="map-profiles",
                            figure=map_figure,
                            className="profiles-map",
                            config={
                                "responsive": True,
                                "scrollZoom": False,
                                "displayModeBar": False,
                            },
                            style={
                                "height": "100%",
                                "width": "100%",
                            },
                        ),
                    ],
                    className="profiles-explorer-map",
                ),


                # ============================================
                # COLONNE DROITE
                # ============================================

                html.Div(
                    [

                        # ------------------------------------
                        # Fiche région
                        # ------------------------------------

                        html.Div(
                            id="region-details",
                            className="region-details",
                            children=[

                                html.Div(
                                    [
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
                            ],
                        ),

                        # ------------------------------------
                        # Profil standardisé
                        # ------------------------------------

                        html.Div(
                            id="region-profile-container",
                        ),

                    ],

                    className="profiles-explorer-details",
                ),

            ],

            className="profiles-explorer",
        ),


        # ====================================================
        # À RETENIR
        # ====================================================

        html.Div([

            html.P(
                "À RETENIR",
                className="section-label",
            ),

            html.P(
                "Les régions ne se différencient pas selon une seule "
                "dimension. Certains territoires associent une situation "
                "sociale et sanitaire globalement plus favorable, tandis "
                "que d'autres présentent des configurations plus contrastées. "
                "Surtout, une meilleure accessibilité aux médecins généralistes "
                "ne va pas systématiquement de pair avec des indicateurs "
                "de santé plus favorables. L'accès aux soins contribue donc "
                "à caractériser les territoires sans résumer, à lui seul, "
                "les inégalités territoriales de santé."
            ),

        ], className="takeaway"),


        # ====================================================
        # ROBUSTESSE ET PRÉCAUTIONS
        # ====================================================

        html.Div([

            html.H3(
                "Précautions de lecture"
            ),

            html.P(
                "Cette typologie est exploratoire et porte sur seulement "
                "13 régions métropolitaines. Elle décrit des proximités "
                "entre territoires à partir des six indicateurs retenus "
                "et ne constitue ni un classement ni une typologie "
                "définitive des régions françaises."
            ),

            html.P(
                "Des analyses de sensibilité ont été réalisées. "
                "Le retrait du F-EDI ne modifie pas les regroupements. "
                "Le retrait de l'APL modifie en revanche le classement "
                "du Grand Est et des Hauts-de-France, ce qui suggère que "
                "l'accessibilité apporte une information complémentaire "
                "dans la caractérisation des territoires."
            ),

            html.P(
                "Le profil francilien est constitué de la seule "
                "Île-de-France. Son interprétation doit donc être "
                "particulièrement prudente."
            ),

        ], className="method-note"),


        # ====================================================
        # SOURCES
        # ====================================================

        html.Div([

            html.Strong(
                "Sources : "
            ),

            html.A(
                "FDep",
                href=(
                    "https://odisse.santepubliquefrance.fr/"
                    "explore/assets/"
                    "indice-de-defavorisation-sociale-fdep-par-commune/"
                ),
                target="_blank",
            ),

            html.Span(" · "),

            html.A(
                "F-EDI 2021",
                href=(
                    "https://odisse.santepubliquefrance.fr/"
                    "explore/assets/"
                    "french-european-deprivation-index-f-edi-2021-par-commune/"
                ),
                target="_blank",
            ),

            html.Span(" · "),

            html.A(
                "APL aux médecins généralistes",
                href=(
                    "https://www.observatoire-des-territoires.gouv.fr/"
                    "accessibilite-potentielle-localisee-apl-"
                    "aux-medecins-generalistes"
                ),
                target="_blank",
            ),

            html.Span(" · "),

            html.A(
                "Baromètre 2024",
                href=(
                    "https://odisse.santepubliquefrance.fr/"
                    "explore/assets/"
                    "sante_generale_indicateurs_barometre_2024/"
                ),
                target="_blank",
            ),

            html.Span(
                " — Santé publique France, Odissé "
                "et Observatoire des territoires."
            ),

        ], className="sources"),

    ], className="tab-content")

# ============================================================
# LAYOUT PRINCIPAL
# ============================================================

def create_layout(
    finance,
    diplome,
    pcs,
    synthese_sociale,
    analyse_regions,
    relations_territoriales,
    regions,
    profils_clusters,
    map_figure,
):

    return html.Div([

        dcc.Tabs(
            id="main-tabs",
            value="accueil",
            className="tabs-container",

            children=[

                dcc.Tab(
                    label="Accueil",
                    value="accueil",
                    className="app-tab",
                    selected_className="app-tab app-tab--selected",
                    children=create_home_tab(),
                ),

                dcc.Tab(
                    label="1 · Inégalités sociales",
                    value="social",
                    className="app-tab",
                    selected_className="app-tab app-tab--selected",

                    children=create_social_tab(
                        finance,
                        synthese_sociale,
                    ),
                ),

                dcc.Tab(
                    label="2 · Territoires & soins",
                    value="territoires",
                    className="app-tab",
                    selected_className="app-tab app-tab--selected",

                    children=create_territorial_tab(
                        analyse_regions,
                        relations_territoriales,
                    ),
                ),

                dcc.Tab(
                    label="3 · Profils territoriaux",
                    value="profils",
                    className="app-tab",
                    selected_className="app-tab app-tab--selected",

                    children=create_profiles_tab(
                        map_figure,
                        regions,
                        profils_clusters,
                    ),
                ),

            ],
        ),

    ], className="app-container")