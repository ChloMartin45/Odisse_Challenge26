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
                "Cette exploration croise plusieurs sources publiques portant sur "
                "la santé, la défavorisation sociale, l'accessibilité aux médecins "
                "généralistes et la population. Les données mobilisées couvrent "
                "principalement la période 2020–2024."
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
                "de données ouvertes françaises."
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

            html.P(
                "Ces trois indicateurs décrivent des dimensions complémentaires "
                "de l'état de santé déclaré.",
                className="reading-guide-intro",
            ),

            html.Div([

                html.Div([
                    html.Strong("Santé perçue"),
                    html.P(
                        "Part de la population déclarant un état de santé "
                        "bon ou très bon."
                    ),
                    html.P(
                        "Une valeur élevée correspond à une situation plus favorable.",
                        className="indicator-direction indicator-direction-positive",
                    ),
                ], className="indicator-card"),

                html.Div([
                    html.Strong("Limitation d'activité"),
                    html.P(
                        "Part de la population déclarant être limitée "
                        "dans ses activités."
                    ),
                    html.P(
                        "Une valeur élevée correspond à une situation plus défavorable.",
                        className="indicator-direction indicator-direction-negative",
                    ),
                ], className="indicator-card"),

                html.Div([
                    html.Strong("Diabète déclaré"),
                    html.P(
                        "Part de la population déclarant être atteinte "
                        "de diabète."
                    ),
                    html.P(
                        "Une valeur élevée correspond à une situation plus défavorable.",
                        className="indicator-direction indicator-direction-negative",
                    ),
                ], className="indicator-card"),

            ], className="indicator-grid"),

        ], className="reading-guide"),

       # ----------------------------------------------------
        # Exploration
        # ----------------------------------------------------

        html.Div(
            [

                # ====================================================
                # EN-TÊTE
                # ====================================================

                html.Div(
                    [
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
                            className="selector social-dashboard-selector",
                        ),
                    ],
                    className="dashboard-header",
                ),

                # ====================================================
                # CONTENU
                # ====================================================

                html.Div(
                    [

                        # --------------------------------------------
                        # Graphique
                        # --------------------------------------------

                        html.Div(
                            [
                                dcc.Graph(
                                    id="social-chart",
                                    figure=create_social_chart(
                                        finance,
                                        "finance",
                                    ),
                                    config={
                                        "displayModeBar": False,
                                        "responsive": True,
                                    },
                                    className="dashboard-chart",
                                ),
                            ],
                            className="dashboard-visual",
                        ),

                        # --------------------------------------------
                        # Colonne de lecture
                        # --------------------------------------------

                        html.Div(
                            [

                                html.Div(
                                    [
                                        html.P(
                                            "LECTURE",
                                            className="dashboard-eyebrow",
                                        ),

                                        html.Div(
                                            id="social-interpretation",
                                            className="dashboard-interpretation",
                                        ),
                                    ],
                                    className="dashboard-reading-block",
                                ),

                                html.Div(
                                    [
                                        html.P(
                                            "REPÈRES",
                                            className="dashboard-eyebrow",
                                        ),

                                        html.P(
                                            "Chaque point représente une estimation "
                                            "pour le groupe social considéré."
                                        ),

                                        html.P(
                                            "Les barres indiquent les intervalles "
                                            "de confiance à 95 %."
                                        ),

                                        html.P(
                                            "Unité : part de la population (%)"
                                        ),
                                    ],
                                    className="dashboard-info-block",
                                ),

                                html.Div(
                                    [
                                        html.P(
                                            "SOURCE",
                                            className="dashboard-eyebrow",
                                        ),

                                        html.P(
                                            "Baromètre de Santé publique France 2024."
                                        ),
                                    ],
                                    className="dashboard-source-block",
                                ),

                            ],
                            className="dashboard-side",
                        ),

                    ],
                    className="dashboard-body",
                ),

            ],
            className="dashboard-section",
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
            "Après avoir mis en évidence des écarts de santé entre groupes sociaux, "
            "l'analyse change d'échelle pour examiner si ces différences se retrouvent "
            "également entre territoires. Deux dimensions sont étudiées successivement : "
            "la défavorisation territoriale, puis l'accessibilité aux médecins généralistes. "
            "L'objectif est d'observer si elles apportent des informations complémentaires "
            "pour caractériser les écarts de santé entre les 13 régions métropolitaines.",
            className="intro",
        ),

        # ----------------------------------------------------
        # FDep
        # ----------------------------------------------------

        html.Div(
            [

                # ====================================================
                # Partie pédagogique
                # ====================================================

                html.H2(
                    "Défavorisation territoriale et santé",
                    className="section-heading",
                ),

                html.P(
                    "Première étape : observer si les régions relativement plus défavorisées "
                    "présentent également des indicateurs de santé moins favorables."
                ),

                html.Div(
                    [
                        html.P(
                            "COMPRENDRE L'INDICATEUR",
                            className="dashboard-eyebrow",
                        ),

                        html.H3(
                            "FDep20 — indice de défavorisation territoriale"
                        ),

                        html.P(
                            "Le FDep20 synthétise quatre dimensions socio-économiques : "
                            "revenu médian, niveau de diplôme, part d'ouvriers et chômage. "
                            "Une valeur plus élevée correspond à un territoire plus défavorisé."
                        ),

                        html.Div(
                            [
                                html.Span(
                                    "Données 2020",
                                    className="context-tag",
                                ),

                                html.Span(
                                    "Géographie communale 2023",
                                    className="context-tag",
                                ),

                                html.Span(
                                    "Agrégation régionale pondérée par la population",
                                    className="context-tag",
                                ),
                            ],
                            className="context-tags",
                        ),

                    ],
                    className="learning-card",
                ),


                # ====================================================
                # Exploration
                # ====================================================

                html.Div(
                    [
                        html.H2(
                            "Explorez la relation"
                        ),

                        html.P(
                            "Sélectionnez un indicateur de santé pour observer "
                            "sa relation avec la défavorisation territoriale."
                        ),

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

                    ],
                    className="dashboard-header",
                ),


                # ====================================================
                # Dashboard
                # ====================================================

                html.Div(
                    [

                        html.Div(
                            [
                                dcc.Graph(
                                    id="fdep-health-chart",
                                    figure=create_fdep_health_chart(
                                        analyse_regions,
                                        relations_territoriales,
                                        "sante",
                                    ),
                                    config={
                                        "displayModeBar": False,
                                        "responsive": True,
                                    },
                                    className="dashboard-chart",
                                ),
                            ],
                            className="dashboard-visual",
                        ),


                        html.Div(
                            [

                                html.Div(
                                    [
                                        html.P(
                                            "LECTURE",
                                            className="dashboard-eyebrow",
                                        ),

                                        html.Div(
                                            id="fdep-interpretation",
                                            className="dashboard-interpretation",
                                        ),
                                    ],
                                    className="dashboard-reading-block",
                                ),


                                html.Div(
                                    [
                                        html.P(
                                            "REPÈRES",
                                            className="dashboard-eyebrow",
                                        ),

                                        html.P(
                                            "Chaque point représente une région métropolitaine."
                                        ),

                                        html.P(
                                            "L’axe vertical indique l’écart à la moyenne des 13 régions : "
                                            "une valeur positive correspond à un niveau supérieur à la moyenne."
                                        ),

                                        html.P(
                                            "Le FDep augmente de gauche à droite : les régions situées à droite "
                                            "sont relativement plus défavorisées."
                                        ),

                                        html.P(
                                            "La ligne pointillée représente la tendance linéaire observée entre "
                                            "la défavorisation territoriale et l’indicateur de santé."
                                        ),
                                    ],
                                    className="dashboard-info-block",
                                ),
                            ],
                            className="dashboard-side",
                        ),

                    ],
                    className="dashboard-body",
                ),

            ],
            className="dashboard-section",
        ),
        
        # ----------------------------------------------------
        # APL
        # ----------------------------------------------------

        html.Div(
            [

                # ====================================================
                # Partie pédagogique
                # ====================================================

                html.H2(
                    "Accessibilité aux soins",
                    className="section-heading",
                ),

                html.P(
                    "Deuxième étape : examiner si l'accessibilité aux médecins généralistes "
                    "apporte une information supplémentaire sur les écarts de santé, une fois "
                    "prise en compte la relation avec la défavorisation territoriale."
                ),

                html.Div(
                    [
                        html.P(
                            "COMPRENDRE L'INDICATEUR",
                            className="dashboard-eyebrow",
                        ),

                        html.H3(
                            "APL — accessibilité aux médecins généralistes"
                        ),

                        html.P(
                            "L’Accessibilité potentielle localisée estime le nombre de "
                            "consultations ou visites de médecine générale accessibles "
                            "par habitant standardisé. Elle tient compte de l’offre "
                            "disponible, de l’activité des médecins, de la distance "
                            "d’accès et des besoins de soins liés à l’âge."
                        ),

                        html.P(
                            "Une valeur plus élevée correspond à une meilleure "
                            "accessibilité aux médecins généralistes."
                        ),

                        html.Div(
                            [
                                html.Span(
                                    "APL 2023",
                                    className="context-tag",
                                ),

                                html.Span(
                                    "Consultations / visites par habitant standardisé",
                                    className="context-tag",
                                ),

                                html.Span(
                                    "Structure d’âge prise en compte",
                                    className="context-tag",
                                ),
                                
                                html.Span(
                                    "Agrégation régionale pondérée par la population",
                                    className="context-tag",
                                ),
                            ],
                            className="context-tags",
                        ),

                        html.Div(
                            [
                                html.Strong(
                                    "Pourquoi prendre en compte le FDep ?"
                                ),

                                html.P(
                                    "Pour examiner si la relation entre accessibilité "
                                    "et santé reste visible une fois prise en compte "
                                    "la relation linéaire avec la défavorisation territoriale."
                                ),
                            ],
                            className="learning-subnote",
                        ),

                    ],
                    className="learning-card",
                ),


                # ====================================================
                # Exploration
                # ====================================================

                html.Div(
                    [
                        html.H2(
                            "Comparez les relations avant et après prise en compte du FDep"
                        ),

                        html.P(
                            "Pour chaque indicateur de santé, comparez la relation brute "
                            "avec l’APL à celle observée après prise en compte de la "
                            "défavorisation territoriale."
                        ),

                    ],
                    className="dashboard-header",
                ),


                # ====================================================
                # Dashboard
                # ====================================================

                html.Div(
                    [

                        # ------------------------------------------------
                        # Graphique
                        # ------------------------------------------------

                        html.Div(
                            [
                                dcc.Graph(
                                    id="apl-comparison-chart",
                                    figure=create_apl_comparison_chart(
                                        relations_territoriales
                                    ),
                                    config={
                                        "displayModeBar": False,
                                        "responsive": True,
                                    },
                                    className="dashboard-chart",
                                ),
                            ],
                            className="dashboard-visual",
                        ),


                        # ------------------------------------------------
                        # Lecture
                        # ------------------------------------------------

                        html.Div(
                            [

                                html.Div(
                                    [
                                        html.P(
                                            "LECTURE",
                                            className="dashboard-eyebrow",
                                        ),

                                        html.H3(
                                            "La limitation d’activité reste la relation "
                                            "la plus marquée avec l’APL",
                                            className="dashboard-reading-title",
                                        ),

                                        html.P(
                                            "Après prise en compte du FDep, la relation "
                                            "avec la limitation d’activité reste proche de "
                                            "celle observée initialement. "
                                            "Les relations avec la santé perçue "
                                            "et le diabète déclaré restent plus faibles.",
                                            className="dashboard-reading-text",
                                        ),

                                    ],
                                    className="dashboard-reading-block",
                                ),


                                html.Div(
                                    [
                                        html.P(
                                            "REPÈRES",
                                            className="dashboard-eyebrow",
                                        ),

                                        html.P(
                                            "Chaque ligne correspond à un indicateur de santé."
                                        ),

                                        html.P(
                                            "Le cercle représente la relation brute avec l’APL ; "
                                            "le losange la relation après prise en compte du FDep."
                                        ),

                                        html.P(
                                            "Plus le coefficient r est proche de −1 ou de +1, "
                                            "plus la relation linéaire est marquée. "
                                            "Une valeur proche de 0 traduit une relation faible."
                                        ),

                                        html.P(
                                            "Le déplacement entre les deux symboles montre "
                                            "comment la relation évolue après prise en compte "
                                            "de la défavorisation territoriale."
                                        ),

                                    ],
                                    className="dashboard-info-block",
                                ),

                            ],
                            className="dashboard-side",
                        ),

                    ],
                    className="dashboard-body",
                ),

            ],
            className="dashboard-section",
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

def create_profile_cards(regions, profils_clusters):
    """Construit les quatre cartes de profils à partir des exports R."""
        
    PROFILE_DESCRIPTIONS = {
        1: (
            "L’Île-de-France forme seule ce groupe et se distingue nettement "
            "des autres régions par la combinaison de ses indicateurs."
        ),

        2: (
            "Ce profil se caractérise surtout par des indicateurs de santé "
            "globalement plus favorables que dans les autres groupes."
        ),

        3: (
            "Ici, une défavorisation plus élevée se combine avec une accessibilité "
            "plus faible aux médecins généralistes, cumulant deux difficultés territoriales."
        ),

        4: (
            "Une meilleure accessibilité aux médecins généralistes coexiste ici avec "
            "des indicateurs de santé plus fragiles."
        ),
    }
    
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
                        PROFILE_DESCRIPTIONS[cluster],
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
            "Les analyses précédentes ont étudié séparément les écarts sociaux, "
            "la défavorisation territoriale et l'accessibilité aux médecins généralistes. "
            "Cette dernière étape change de perspective : il ne s'agit plus d'isoler "
            "une relation, mais d'observer comment plusieurs dimensions se combinent "
            "au sein d'un même territoire. L'objectif est d'identifier des configurations "
            "régionales récurrentes, sans établir de classement des régions.",
            className="intro",
        ),

        # ====================================================
        # MÉTHODE
        # ====================================================

        html.Div(
            [

                # ----------------------------------------------------
                # Introduction de la méthode
                # ----------------------------------------------------

                html.Div(
                    [
                        html.P(
                            "COMMENT SONT CONSTRUITS LES PROFILS ?",
                            className="method-flow-eyebrow",
                        ),

                        html.H2(
                            "De six indicateurs à quatre profils territoriaux"
                        ),

                        html.P(
                            "Les régions sont comparées simultanément selon leur contexte "
                            "social, leur accessibilité aux médecins généralistes et leurs "
                            "indicateurs de santé. L'objectif est de faire apparaître des "
                            "configurations territoriales similaires, et non d'établir "
                            "un classement.",
                            className="method-flow-intro",
                        ),
                    ],
                    className="method-flow-header",
                ),


                # ----------------------------------------------------
                # FDep / F-EDI
                # ----------------------------------------------------

                html.Div(
                    [
                        html.P(
                            "POURQUOI DEUX INDICES DE DÉFAVORISATION ?",
                            className="dashboard-eyebrow",
                        ),

                        html.H3(
                            "FDep et F-EDI apportent deux lectures complémentaires"
                        ),

                        html.P([
                            html.Span(
                                "FDep20 — ",
                                className="text-accent",
                            ),
                            "un indice synthétique de défavorisation socio-économique fondé sur "
                            "quatre dimensions : revenu médian, niveau de diplôme, part d'ouvriers "
                            "et chômage."
                        ]),

                        html.P([
                            html.Span(
                                "F-EDI — ",
                                className="text-accent",
                            ),
                            "un indice écologique de défavorisation sociale construit à partir de "
                            "l'enquête européenne EU-SILC et du recensement. Il mobilise dix "
                            "caractéristiques liées notamment à l'emploi, au diplôme, au logement, "
                            "à l'équipement automobile, à la propriété du logement et à la composition "
                            "des ménages."
                        ]),
                        
                        html.P([
                            html.Span(
                                "Point de vigilance — ",
                                className="text-accent-blue",
                            ),
                            "ces deux indices caractérisent le contexte social d'un territoire. "
                            "Ils ne mesurent pas la situation sociale individuelle de ses habitants."
                        ]),

                        html.Div(
                            [
                                html.Span(
                                    "FDep : 4 dimensions socio-économiques",
                                    className="context-tag",
                                ),

                                html.Span(
                                    "F-EDI : 10 dimensions sociales et matérielles",
                                    className="context-tag",
                                ),

                                html.Span(
                                    "F-EDI 2021",
                                    className="context-tag",
                                ),

                                html.Span(
                                    "Indices écologiques territoriaux",
                                    className="context-tag",
                                ),
                                
                                html.Span(
                                    "Agrégation régionale pondérée par la population",
                                    className="context-tag",
                                ),
                            ],
                            className="context-tags",
                        ),

                        html.Div(
                            [
                                html.Strong(
                                    "Pourquoi le F-EDI apparaît-il seulement ici ?"
                                ),

                                html.P([
                                    "Dans l'onglet précédent, le FDep a été retenu comme indicateur principal "
                                    "pour étudier des relations territoriales simples et lisibles. Ici, ",
                                    html.Span(
                                        "la question change : plusieurs dimensions sont considérées simultanément",
                                        className="text-accent-blue",
                                    ),
                                    " pour construire les profils. Le F-EDI complète donc le FDep par une "
                                    "mesure plus large du contexte social et matériel."
                                ]),

                                html.P([
                                    html.Span(
                                        "Contrôle de robustesse — ",
                                        className="text-accent",
                                    ),
                                    "le retrait du F-EDI ne modifie pas les quatre regroupements obtenus."
                                ]),
                            ],
                            className="learning-subnote",
                        ),

                    ],
                    className="learning-card",
                ),


                # ----------------------------------------------------
                # Parcours méthodologique
                # ----------------------------------------------------

                html.Div(
                    [

                        # ------------------------------------------------
                        # Étape 1
                        # ------------------------------------------------

                        html.Div(
                            [
                                html.Span(
                                    "01",
                                    className="method-step-number",
                                ),

                                html.Strong(
                                    "Décrire plusieurs dimensions"
                                ),

                                html.Div(
                                    [
                                        html.P([
                                            html.B("Contexte social"),
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


                        # ------------------------------------------------
                        # Étape 2
                        # ------------------------------------------------

                        html.Div(
                            [
                                html.Span(
                                    "02",
                                    className="method-step-number",
                                ),

                                html.Strong(
                                    "Rendre les indicateurs comparables"
                                ),

                                html.P([
                                    "Les six indicateurs sont standardisés afin de comparer la position "
                                    "relative de chaque région malgré des unités différentes. Leur sens est "
                                    "ensuite harmonisé : ",
                                    html.Span(
                                        "score positif = situation relativement plus défavorable",
                                        className="text-accent-blue",
                                    ),
                                    " ; ",
                                    html.Span(
                                        "score négatif = situation relativement plus favorable",
                                        className="text-accent-blue",
                                    ),
                                    "."
                                ]),

                            ],
                            className="method-step",
                        ),

                        html.Div(
                            "→",
                            className="method-arrow",
                        ),


                        # ------------------------------------------------
                        # Étape 3
                        # ------------------------------------------------

                        html.Div(
                            [
                                html.Span(
                                    "03",
                                    className="method-step-number",
                                ),

                                html.Strong(
                                    "Rapprocher les régions qui se ressemblent"
                                ),

                                html.P([
                                    "Une classification hiérarchique considère les six indicateurs "
                                    "simultanément et rapproche ",
                                    html.Span(
                                        "les régions présentant les configurations les plus similaires",
                                        className="text-accent-blue",
                                    ),
                                    "."
                                ]),

                                html.P(
                                    "Chaque indicateur intervient individuellement dans "
                                    "la construction des groupes.",
                                    className="method-step-note",
                                ),
                            ],
                            className="method-step",
                        ),


                        html.Div(
                            "→",
                            className="method-arrow",
                        ),


                        # ------------------------------------------------
                        # Étape 4
                        # ------------------------------------------------

                        html.Div(
                            [
                                html.Span(
                                    "04",
                                    className="method-step-number",
                                ),

                                html.Strong(
                                    "Retenir quatre profils interprétables"
                                ),

                                html.P([
                                    "La structure de la classification isole d'abord fortement l'Île-de-France. "
                                    "Avec trois groupes, les autres régions commencent à se différencier. ",
                                    html.Span(
                                        "Quatre groupes sont finalement retenus",
                                        className="text-highlight",
                                    ),
                                    " pour obtenir une lecture plus fine tout en conservant des profils interprétables."
                                ]),

                            ],
                            className="method-step method-step-result",
                        ),

                    ],
                    className="method-flow",
                ),
                
                # ----------------------------------------------------
                # Données et échelles
                # ----------------------------------------------------
                
                html.Div(
                    [
                        html.P(
                            "DONNÉES ET ÉCHELLES",
                            className="dashboard-eyebrow",
                        ),

                        html.P([
                            html.Span(
                                "FDep, F-EDI et APL — ",
                                className="text-accent",
                            ),
                            "ces indicateurs proviennent de données territoriales plus fines "
                            "et sont ramenés à l'échelle régionale par moyenne pondérée selon "
                            "la population communale 2023. Les communes les plus peuplées "
                            "contribuent donc davantage à la valeur régionale."
                        ]),

                        html.P([
                            html.Span(
                                "Santé perçue, limitation d'activité et diabète — ",
                                className="text-accent-blue",
                            ),
                            "ces indicateurs sont déjà disponibles à l'échelle régionale dans "
                            "le Baromètre 2024 et sont utilisés tels que fournis, sans nouvelle "
                            "agrégation communale."
                        ]),
                    ],
                    className="method-data-note",
                ),

                # ----------------------------------------------------
                # Robustesse
                # ----------------------------------------------------

                html.Div(
                    [
                        html.P(
                            "TESTER LA ROBUSTESSE",
                            className="dashboard-eyebrow",
                        ),

                        html.H3([
                            "Les profils ont été confrontés à ",
                            html.Span(
                                "plusieurs scénarios",
                                className="text-accent",
                            ),
                        ]),

                        html.P(
                            "La classification a été recalculée avec trois groupes, "
                            "puis à quatre groupes en retirant successivement le F-EDI "
                            "et l'APL. Ces tests servent à vérifier la stabilité générale "
                            "de la typologie, et non à rechercher a posteriori le découpage "
                            "le plus favorable."
                        ),

                        html.Div(
                            [
                                html.Span(
                                    "3 groupes : structure plus agrégée",
                                    className="context-tag",
                                ),

                                html.Span(
                                    "Sans F-EDI : mêmes 4 regroupements",
                                    className="context-tag",
                                ),

                                html.Span(
                                    "Sans APL : certaines régions changent de profil",
                                    className="context-tag",
                                ),
                            ],
                            className="context-tags",
                        ),
                    ],
                    className="learning-card",
                ),
            ],
            className="method-flow-block",
        ),
        
        html.Div(
            [
                html.P(
                    "La typologie retenue ne repose donc pas sur un seul indicateur : "
                    "elle résulte de la combinaison de plusieurs dimensions territoriales "
                    "et reste globalement stable lorsque certains choix méthodologiques "
                    "sont modifiés."
                ),
            ],
            className="result-note",
        ),

       # ====================================================
        # LES QUATRE PROFILS
        # ====================================================

        html.Div(
            [

                html.H2(
                    "Quatre configurations territoriales se distinguent",
                    className="section-heading",
                ),

                html.P(
                    "Les quatre profils combinent différemment contexte social, "
                    "accessibilité aux médecins généralistes et santé. Ils font apparaître "
                    "des situations de cumul, mais aussi des configurations plus contrastées.",
                    className="profiles-summary-intro",
                ),

                html.Div(
                    [
                        html.P(
                            "Une meilleure accessibilité aux médecins généralistes ne coïncide "
                            "pas systématiquement avec des indicateurs de santé plus favorables : "
                            "l'accès aux soins ne suffit donc pas, à lui seul, à résumer les "
                            "inégalités territoriales de santé."
                        ),
                    ],
                    className="result-note profiles-key-result",
                ),

                create_profile_cards(
                    regions,
                    profils_clusters,
                ),

                html.P(
                    "Les profils décrivent des configurations moyennes et ne constituent "
                    "pas un classement. Le profil francilien, composé d’une seule région, "
                    "doit être interprété avec prudence.",
                    className="note profiles-summary-note",
                ),

            ],
            className="profiles-summary-section",
        ),


        # ====================================================
        # EXPLORATION INTERACTIVE
        # ====================================================

        html.H2(
            "Explorer les profils région par région"
        ),

        html.P(
            "Sélectionnez une région pour découvrir les indicateurs qui caractérisent "
            "son territoire et situer sa position par rapport à la moyenne des "
            "13 régions métropolitaines étudiées."
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

        html.Div(
            [

                html.Div(
                    [
                        html.H3(
                            "Portée de l'analyse"
                        ),

                        html.P(
                            "Cette typologie est exploratoire et porte sur seulement "
                            "13 régions métropolitaines. Elle décrit des proximités "
                            "entre territoires à partir des six indicateurs retenus "
                            "et ne constitue ni un classement ni une typologie "
                            "définitive des régions françaises."
                        ),

                        html.P(
                            "Le profil francilien est constitué de la seule "
                            "Île-de-France. Son interprétation doit donc être "
                            "particulièrement prudente."
                        ),
                    ],
                    className="method-note",
                ),

                html.Div(
                    [
                        html.H3(
                            "Données et robustesse"
                        ),

                        html.P(
                            "Les sources mobilisées ne portent pas toutes sur la même période : "
                            "FDep à partir de données socio-économiques 2020, F-EDI 2021, "
                            "APL et population 2023, indicateurs de santé du Baromètre 2024. "
                            "FDep, F-EDI et APL sont agrégés à l'échelle régionale en pondérant "
                            "les valeurs communales par la population, tandis que les indicateurs "
                            "de santé correspondent directement aux estimations régionales du "
                            "Baromètre 2024."
                        ),

                        html.P(
                            "Des analyses de sensibilité ont été réalisées. "
                            "Le retrait du F-EDI ne modifie pas les regroupements. "
                            "Le retrait de l'APL modifie en revanche le classement "
                            "du Grand Est et des Hauts-de-France."
                        ),
                    ],
                    className="method-note",
                ),

            ],
            className="method-notes-grid",
        ),

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