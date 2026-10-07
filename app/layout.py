from dash import dcc, html

from charts import (
    create_social_chart,
    create_fdep_health_chart,
    create_apl_comparison_chart,
    create_diabetes_age_sex_chart,
)

# ============================================================
# CONFIGURATION COMMUNES POUR SOULAGER LE CODE
# ============================================================

GRAPH_CONFIG = {
    "displayModeBar": False,
    "responsive": True,
    "scrollZoom": False,
    "doubleClick": False,
}

MAP_CONFIG = {
    **GRAPH_CONFIG,
    "scrollZoom": False,
}

# ============================================================
# ACCUEIL
# ============================================================

def create_home_tab():

    return html.Div(
        [

            # ----------------------------------------------------
            # Introduction
            # ----------------------------------------------------

            html.P(
                "ODISSÉ DATAVIZ CHALLENGE 2026 · DÉFI 3",
                className="eyebrow",
            ),

            html.H1(
                "La santé ne se résume pas à l’accès aux soins"
            ),

            html.P(
                "En 2024, 68 % des adultes de 18 à 79 ans déclarent être en bonne ou très bonne "
                "santé, tandis que 26 % déclarent être limités depuis au moins six mois dans leurs "
                "activités habituelles à cause d’un problème de santé. Derrière ces moyennes se "
                "cachent d’importants écarts sociaux et territoriaux. "
                "Cette visualisation suit ces écarts depuis les groupes sociaux jusqu’aux territoires "
                "pour comprendre comment contexte social, accessibilité aux médecins généralistes "
                "et état de santé se combinent.",
                className="intro",
            ),
            
            html.P(
                [
                    "Source des chiffres d’introduction : ",
                    html.A(
                        "Santé publique France — Santé générale, Baromètre 2024",
                        href=(
                            "https://www.santepubliquefrance.fr/sites/default/files/"
                            "rdd/document/907125_spf00006377.pdf"
                        ),
                        target="_blank",
                    ),
                    ".",
                ],
                className="source-note",
            ),
            
            # ----------------------------------------------------
            # Problématique
            # ----------------------------------------------------

            html.Div(
                [
                    html.P(
                        "QUESTION DE DÉPART",
                        className="section-label",
                    ),

                    html.H2(
                        "Comment les inégalités sociales et territoriales de santé "
                        "se combinent-elles avec l'accessibilité aux médecins généralistes pour "
                        "caractériser différents profils régionaux en France métropolitaine ?"
                    ),

                ], 
                className="question-block",
            ),

            # ----------------------------------------------------
            # Parcours
            # ----------------------------------------------------

            html.H2(
                "Du constat social aux profils territoriaux"
            ),

            html.Div(
                [
                    html.Div(
                        [
                            html.P("01", className="step-number"),
                            html.H3("Inégalités sociales"),
                            html.P(
                                "Observer comment plusieurs dimensions sociales, notamment la situation "
                                "financière, le diplôme et la catégorie socioprofessionnelle, "
                                "s'accompagnent de différences de santé."
                            ),
                        ], 
                        className="step-card",
                    ),

                    html.Div(
                        [
                            html.P("02", className="step-number"),
                            html.H3("Territoires & soins"),
                            html.P(
                                    "Examiner si la défavorisation des territoires et "
                                    "l'accessibilité aux médecins généralistes sont associées "
                                    "aux différences de santé observées entre régions."
                                ),
                        ], 
                        className="step-card",
                    ),

                    html.Div(
                        [
                            html.P("03", className="step-number"),
                            html.H3("Profils territoriaux"),
                            html.P(
                                "Combiner six indicateurs pour faire émerger différentes "
                                "configurations régionales et comprendre ce qui les distingue."
                            ),
                        ], 
                        className="step-card",
                    ),
                ], 
                className="steps"
            ),

            # ----------------------------------------------------
            # Détail Accueil
            # ----------------------------------------------------

            html.Details(
                [
                    html.Summary(
                        "Voir les données et sources mobilisées"
                    ),
                    
                    html.Div(
                        [
                            html.P(
                                "Cette exploration croise plusieurs sources publiques "
                                "portant sur la santé, la défavorisation sociale, "
                                "l'accessibilité aux médecins généralistes et la population. "
                                "Les données mobilisées couvrent principalement la période 2020–2024."
                            ),

                            html.Ul(
                                [
                                    html.Li(
                                        [
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
                                        ]
                                    ),

                                    html.Li(
                                        [
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
                                        ]
                                    ),

                                    html.Li(
                                        [
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
                                        ]
                                    ),

                                    html.Li(
                                        [
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
                                            ]
                                    ),
                                    
                                    html.Li(
                                        [
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
                                        ]
                                    ),

                                    html.Li(
                                        [
                                            html.A(
                                                "Populations 2023",
                                                href="https://www.insee.fr/fr/statistiques/8680726",
                                                target="_blank",
                                            ),
                                            " · Insee",
                                        ]
                                    ),
                            
                                ],
                                className="sources-list",
                            ),
                        
                            html.P(
                                [
                                    html.Strong("Source de contexte : "),
                                    "les chiffres nationaux présentés en introduction "
                                    "proviennent de la synthèse Santé générale du Baromètre de "
                                    "Santé publique France 2024."
                                ],
                                className="note",
                            ),
                        ],
                        className="sources-block",
                    ),
                ],
                className="home-details",
            ),
                            
            # ----------------------------------------------------
            # A propos du projet
            # ----------------------------------------------------

            html.P(
                "Projet réalisé dans le cadre de l’Odissé Dataviz Challenge 2026 "
                "à partir de données ouvertes de Santé publique France et de sources complémentaires.",
                className="home-project-note",
            ),
                                        
            # ----------------------------------------------------
            # Transition
            # ----------------------------------------------------
                                            
            html.Div(
                [
                    html.P(
                        "Commençons par regarder si les écarts de santé apparaissent "
                        "déjà entre groupes sociaux."
                    ),

                    html.Button(
                        [
                            html.Span(
                                className="transition-arrow",
                                **{"aria-hidden": "true"},
                            ),
                            html.Span("Commencer l'exploration"),
                        ],
                        id="go-to-social",
                        className="transition-link",
                        n_clicks=0,
                    ),
                ],
                className="transition",
            ),
        ],
        className="tab-content",
    )

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
        "Limitation d'activité": "Limitations habituelles",
        "Diabète déclaré": "Diabète déclaré",
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

            if dimension == "finance":

                sous_titre = (
                    "Difficultés financières comparées à une situation « à l'aise »"
                )

            elif dimension == "diplome":

                sous_titre = (
                    "Aucun diplôme ou diplôme inférieur au Bac comparé "
                    "à un diplôme supérieur au Bac"
                )

            else:

                sous_titre = (
                    "Écart entre les catégories présentant les valeurs extrêmes"
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

                valeurs_groupes = {
                    groupe_comparaison: valeur_comparaison,
                    groupe_reference: valeur_reference,
                }

                groupe_cadres = next(
                    g for g in valeurs_groupes
                    if "Cadres" in g
                )

                groupe_ouvriers = next(
                    g for g in valeurs_groupes
                    if "Ouvriers" in g
                )

                detail = [
                    html.Span(
                        f"{groupe_cadres} : "
                        f"{format_number(valeurs_groupes[groupe_cadres])} %"
                    ),
                    html.Br(),
                    html.Span(
                        f"{groupe_ouvriers} : "
                        f"{format_number(valeurs_groupes[groupe_ouvriers])} %"
                    ),
                ]

            else:

                signe = "+" if ecart > 0 else "−" if ecart < 0 else ""

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

def create_social_tab(
    finance,
    synthese_sociale,
    ):
    
    # ----------------------------------------------------
    # Introduction
    # ----------------------------------------------------

    return html.Div([
        
        html.P(
            "01 · INÉGALITÉS SOCIALES",
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
        # Présentation des données
        # ----------------------------------------------------

        html.Div(
            [
                html.P(
                    "COMPRENDRE LES DONNÉES",
                    className="dashboard-eyebrow",
                ),

                html.H3(
                    "Le Baromètre de Santé publique France 2024"
                ),

                html.P(
                    "Le Baromètre est une enquête nationale menée auprès de "
                    "34 940 personnes âgées de 18 à 79 ans. Les répondants ont été "
                    "interrogés par internet ou téléphone. Les estimations sont pondérées "
                    "afin de tenir compte du plan d'échantillonnage, de la participation "
                    "et de la structure de la population."
                ),

                html.P(
                    "Les estimations nationales sont accompagnées d'intervalles de confiance à 95 %. "
                    "Les indicateurs présentés ici sont déclaratifs : ils correspondent "
                    "aux réponses fournies par les personnes interrogées."
                ),

                html.Div(
                    [
                        html.Span(
                            "2024",
                            className="context-tag",
                        ),
                        html.Span(
                            "34 940 répondants",
                            className="context-tag",
                        ),
                        html.Span(
                            "18–79 ans",
                            className="context-tag",
                        ),
                        html.Span(
                            "Estimations pondérées · IC 95 %",
                            className="context-tag",
                        ),
                    ],
                    className="context-tags",
                ),
            ],
            className="learning-card",
        ),
    

        # ----------------------------------------------------
        # Définitions
        # ----------------------------------------------------

        html.Div(
            [
                html.P(
                    "COMPRENDRE LES INDICATEURS",
                    className="dashboard-eyebrow",
                ),
                
                html.H3(
                    "Trois dimensions complémentaires de l'état de santé"
                ),

                html.P(
                    "Les trois indicateurs ne décrivent pas exactement la même chose : "
                    "ils renseignent respectivement sur la perception générale de la santé, "
                    "les conséquences durables d'un problème de santé dans la vie quotidienne "
                    "et la présence déclarée d'un diabète.",
                ),

                html.Div(
                    [

                        html.Div(
                            [
                                html.Strong("Bonne ou très bonne santé perçue"),

                                html.P(
                                    "Part des personnes répondant « bon » ou « très bon » "
                                    "à la question sur leur état de santé général."
                                ),

                                html.P(
                                    "Une valeur élevée correspond à une situation plus favorable.",
                                    className="indicator-direction",
                                ),
                            ],
                            className="indicator-card",
                        ),

                        html.Div(
                            [
                                html.Strong(
                                    "Limitation dans les activités habituelles"
                                ),

                                html.P(
                                    "Part des adultes déclarant être limités ou fortement limités, "
                                    "depuis au moins six mois et à cause d'un problème de santé, "
                                    "dans les activités que les gens font habituellement."
                                ),

                                html.P(
                                    "Une valeur élevée correspond à une situation plus défavorable.",
                                    className="indicator-direction",
                                ),
                            ],
                            className="indicator-card",
                        ),

                        html.Div(
                            [
                                html.Strong("Diabète déclaré"),

                                html.P(
                                    "Part des personnes déclarant être atteintes de diabète."
                                ),

                                html.P(
                                    "Une valeur élevée correspond à une situation plus défavorable.",
                                    className="indicator-direction",
                                ),
                            ],
                            className="indicator-card",
                        ),

                    ],
                    className="indicator-grid",
                ),
            ],
            className="reading-guide",
        ),

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
                            className="selector",
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
                                    config=GRAPH_CONFIG,
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
                "Les écarts les plus marqués concernent la situation financière "
                "et le diplôme",
                className="section-heading",
            ),

            html.P(
                "Les écarts entre les situations comparées "
                "apparaissent dans les trois indicateurs étudiés."
            ),

            create_social_summary(synthese_sociale),

            html.P(
                "Note : pour la catégorie socioprofessionnelle, les valeurs "
                "correspondent à l'écart entre les catégories présentant "
                "les valeurs extrêmes observées. Les PCS ne constituent "
                "pas une échelle sociale continue.",
                className="note",
            ),

        ], className="social-summary"),

        # ----------------------------------------------------
        # À retenir
        # ----------------------------------------------------

        html.Div(
            [
                html.P(
                    "À RETENIR",
                    className="section-label",
                ),

                html.P(
                    [
                        html.Strong(
                            "Les écarts de santé sont déjà visibles entre groupes sociaux. "
                        ),
                        "La situation financière, le niveau de diplôme et la catégorie "
                        "socioprofessionnelle s'accompagnent de différences sur les trois "
                        "indicateurs étudiés. Les écarts sont particulièrement marqués "
                        "pour la situation financière et le diplôme."
                    ]
                ),
            ],
            className="takeaway",
        ),

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

        html.Div(
            [
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

                html.Span(
                    " — Santé publique France, Odissé."
                ),
            ], 
            className="sources"
        ),
        
        html.P(
            "Les comparaisons présentées dans cet onglet portent sur les estimations "
            "nationales du Baromètre 2024. L’analyse territoriale suivante se concentre "
            "ensuite sur les 13 régions de France métropolitaine.",
            className="note",
        ),

        # ----------------------------------------------------
        # CHOIX DE POURSUITE - TRANSITIONS
        # ----------------------------------------------------

        html.Div(
            [   
                html.P(
                    "POURSUIVRE L'EXPLORATION",
                    className="section-label",
                ),

                html.Div(
                    [

                        # ----------------------------------------
                        # Parcours principal
                        # ----------------------------------------
                        
                        html.Div(
                            [

                                html.P(
                                    "PARCOURS PRINCIPAL",
                                    className="dashboard-eyebrow",
                                ),
                    
                                html.P(
                                    "Ces écarts apparaissent entre groupes sociaux. "
                                    "Mais les retrouve-t-on également lorsque l'on change d'échelle "
                                    "pour comparer les territoires ?"
                                ),
                                
                                html.Button(
                                    [
                                        html.Span(
                                            className="transition-arrow",
                                            **{"aria-hidden": "true"},
                                        ),
                                        html.Span("Continuer vers Territoires & soins"),
                                    ],
                                    id="go-to-territoires",
                                    className="transition-link",
                                    n_clicks=0,
                                ),
                            ],
                            className="transition transition-choice",
                        ),
        
                        # ----------------------------------------------------
                        # Transition complémentaire du cas d'étude Diabète
                        # ----------------------------------------------------     
                        
                        html.Div(
                            [
                                html.P(
                                    "APPROFONDISSEMENT",
                                    className="dashboard-eyebrow",
                                ),

                                html.P(
                                    "Un focus complémentaire sur le diabète permet "
                                    "d'approfondir les inégalités sociales et démographiques "
                                    "à travers un cas d'étude."
                                ),
                                
                                html.Button(
                                    [
                                        html.Span(
                                            className="transition-arrow",
                                            **{"aria-hidden": "true"},
                                        ),
                                        html.Span(
                                            "Explorer le focus diabète"
                                        ),
                                    ],
                                    id="go-to-diabete",
                                    className="transition-link",
                                    n_clicks=0,
                                ),
                            ],
                            className="transition transition-choice",
                        ),
                    ],
                    className="transition-choices",
                ),
            ],
            className="transition-section",
        )
    ], 
    className="tab-content")

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
            "02 · TERRITOIRES & SOINS",
            className="section-label",
        ),

        html.H1(
            "Le contexte social des territoires est lié à la santé, "
            "mais l'accessibilité aux médecins généralistes ne raconte pas toute l'histoire"
        ),

        html.P(
            "Après avoir observé des écarts entre groupes sociaux, l'analyse change "
            "d'échelle. Les 13 régions métropolitaines sont comparées selon "
            "leur contexte social, puis selon leur accessibilité aux médecins "
            "généralistes. L'objectif est de déterminer si ces deux dimensions racontent "
            "la même géographie des inégalités de santé ou, au contraire, des réalités différentes.",
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
                    "Avant d’examiner l’accessibilité aux médecins, regardons si le contexte social "
                    "des territoires est déjà associé aux différences de santé observées entre régions."
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
                        
                        html.P(
                            "Pour cette analyse, les valeurs communales ont été ramenées à l'échelle "
                            "régionale par une moyenne pondérée selon la population communale. "
                            "La valeur présentée caractérise donc le contexte moyen de la région ; "
                            "elle ne décrit pas la situation individuelle de chacun de ses habitants."
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
                            "Comment la santé varie-t-elle avec la défavorisation territoriale ?",
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
                                    "label": "Limitation dans les activités habituelles",
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
                                    config=GRAPH_CONFIG,
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
                    "Une meilleure accessibilité aux médecins va-t-elle toujours "
                    "avec de meilleurs indicateurs de santé ?",
                    className="section-heading",
                ),

                html.P(
                    "Le premier constat est clair : la défavorisation territoriale est associée "
                    "à plusieurs dimensions de santé, avec une relation particulièrement marquée "
                    "pour la santé perçue et le diabète déclaré. Mais le contexte social ne suffit "
                    "pas à caractériser un territoire. L’accessibilité aux médecins généralistes "
                    "apporte-t-elle une autre lecture ?"
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
                                    "Pour vérifier si la relation entre accessibilité et santé subsiste "
                                    "une fois prise en compte son association avec la défavorisation territoriale."
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
                            "Que reste-t-il de la relation avec l’APL après prise en compte du contexte social ?"
                        ),

                        html.P(
                            "Pour chacun des trois indicateurs de santé, comparez la relation avec l’APL "
                            "avant et après prise en compte du FDep afin de distinguer ce qui est associé "
                            "à l’accessibilité de ce qui est déjà lié au contexte social du territoire."
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
                                    config=GRAPH_CONFIG,
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
                                            "La prise en compte du contexte social modifie peu "
                                            "les relations avec l'APL",
                                            className="dashboard-reading-title",
                                        ),

                                        html.P(
                                            "Les relations avec la santé perçue et le diabète déclaré restent faibles. "
                                            "La relation la plus marquée concerne les limitations dans les activités habituelles "
                                            "et varie peu après prise en compte du FDep. Avec seulement 13 régions, "
                                            "elle reste toutefois incertaine.",
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
                                            "Plus le coefficient r est éloigné de 0, "
                                            "plus la relation linéaire est marquée."
                                        ),

                                        html.P(
                                            "L’écart entre les deux symboles montre comment la relation évolue "
                                            "après prise en compte du contexte social."
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

        html.Div(
            [
                html.P(
                    "À RETENIR",
                    className="section-label",
                ),

                html.P(
                    [
                        html.Strong(
                            "À l'échelle régionale, l'accessibilité aux médecins généralistes "
                            "ne suffit pas à résumer les inégalités de santé. "
                        ),
                        "La défavorisation territoriale présente des associations nettes "
                        "avec la santé perçue et le diabète déclaré, tandis qu'une meilleure "
                        "accessibilité aux médecins généralistes ne s'accompagne pas systématiquement "
                        "de meilleurs indicateurs de santé."
                    ]
                ),

            ],
            className="takeaway",
        ),

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

        html.Div(
            [
                html.P(
                    "Aucune dimension prise isolément ne suffit donc à caractériser "
                    "les territoires. Que révèle leur combinaison ?"
                ),
                
                html.Button(
                    [
                        html.Span(
                            className="transition-arrow",
                            **{"aria-hidden": "true"},
                        ),
                        html.Span("Continuer vers Profils territoriaux"),
                    ],
                    id="go-to-profils",
                    className="transition-link",
                    n_clicks=0,
                ),
            ],
            className="transition",
        ),

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
            "03 · PROFILS TERRITORIAUX",
            className="section-label",
        ),

        html.H1(
            "Quatre profils montrent qu'il n'existe pas "
            "une seule géographie des inégalités de santé"
        ),

        html.P(
            "Lorsqu'on combine défavorisation territoriale, accessibilité aux médecins "
            "généralistes et trois indicateurs de santé, les 13 régions métropolitaines "
            "ne s'ordonnent pas simplement des plus aux moins favorisées. "
            "Quatre configurations distinctes apparaissent.",
            className="intro",
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
                
                html.H3(
                    "Six indicateurs pour caractériser les régions"
                ),
                
                html.P(
                    "La typologie combine deux indices de défavorisation territoriale "
                    "(FDep et F-EDI), l'accessibilité aux médecins généralistes (APL) "
                    "et trois indicateurs de santé : santé perçue, limitation dans les "
                    "activités habituelles et diabète déclaré."
                ),

                html.P(
                    [
                        html.Strong("Indicateurs territoriaux : "),
                        "FDep, F-EDI et APL proviennent de données territoriales plus fines "
                        "et sont ramenés à l'échelle régionale par moyenne pondérée selon "
                        "la population communale 2023."
                    ]
                ),
                
                html.P(
                     [
                        html.Strong("Indicateurs de santé : "),
                        "les estimations du Baromètre 2024 sont déjà disponibles à l'échelle "
                        "régionale et sont utilisées telles que fournies."
                    ]
                ),

                html.Div(
                    [
                        html.Span("FDep : 2020", className="context-tag"),
                        html.Span("F-EDI : 2021", className="context-tag"),
                        html.Span("APL : 2023", className="context-tag"),
                        html.Span("Santé : 2024", className="context-tag"),
                    ],
                    className="context-tags",
                ),

                html.Div(
                    [
                        html.Strong(
                            "Point de vigilance"
                        ),

                        html.P(
                            "Les indices FDep et F-EDI décrivent le contexte social "
                            "des territoires et non la situation individuelle de leurs habitants."
                        ),
                    ],
                    className="learning-subnote",
                ),
            ],
            className="learning-card",
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
                            [
                                "Les régions ne s’ordonnent pas simplement des plus aux moins favorisées : "
                                "les mêmes niveaux d’accessibilité peuvent coexister avec des contextes sociaux "
                                "et des états de santé différents. La combinaison des six indicateurs fait ainsi apparaître ",

                                html.Strong(
                                    "quatre configurations territoriales distinctes.",
                                ),
                            ]
                        ),
                    ],
                    className="result-note",
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
                            config=MAP_CONFIG,
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
        # MÉTHODE
        # ====================================================


        html.Details(
            [
                html.Summary(
                    "Voir comment les quatre profils ont été construits"
                ),

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
                                        "Point de vigilance : ",
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
                                                "Contrôle de robustesse : ",
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
                    ],
                    className="method-flow-block",
                ),
            ],
            className="method-details",
        ),

        # ====================================================
        # RÉPONSE À LA QUESTION DE DÉPART
        # ====================================================

        html.Div(
            [
                html.P(
                    "RÉPONSE À LA QUESTION DE DÉPART",
                    className="section-label",
                ),

                html.P(
                    [
                        html.Strong(
                            "Les inégalités territoriales de santé ne suivent pas un axe unique. "
                        ),

                        "Les 13 régions étudiées combinent différemment contexte social, "
                        "accessibilité aux médecins généralistes et état de santé. Certaines "
                        "cumulent défavorisation et faible accessibilité, tandis que d'autres "
                        "présentent des indicateurs de santé plus fragiles malgré une meilleure "
                        "accessibilité. ",

                        html.Strong(
                            "L'accessibilité aux médecins généralistes contribue donc à caractériser les territoires, "
                            "mais ne suffit pas à elle seule à résumer leurs inégalités de santé."
                        ),

                        html.Br(),
                        html.Br(),

                        "Comprendre ces inégalités suppose ainsi de considérer simultanément le "
                        "contexte social, l'accessibilité aux médecins généralistes "
                        "et l'état de santé des populations."
                    ]
                ),
            ],
            className="takeaway",
        ),


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
                            "Temporalités et limites des données"
                        ),

                        html.P(
                            "Les sources mobilisées ne portent pas toutes sur la même période : "
                            "FDep à partir de données socio-économiques 2020, F-EDI 2021, "
                            "APL et population 2023, indicateurs de santé du Baromètre 2024. "
                             "La typologie décrit donc des configurations territoriales proches "
                            "dans le temps, et non une photographie strictement simultanée."
                        ),
                        
                        html.P(
                            "FDep, F-EDI et APL sont agrégés à l'échelle régionale en pondérant "
                            "les valeurs communales par la population, tandis que les indicateurs "
                            "de santé correspondent directement aux estimations régionales du "
                            "Baromètre 2024."
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
# FOCUS — DIABÈTE
# ============================================================

def create_diabetes_focus(
    diabete_age_sexe,
    diabete_ecart_sexe_age,
    synthese_sociale,
):
    # ========================================================
    # Lecture dynamique — âge et sexe
    # ========================================================

    ecarts_age_sexe = (
        diabete_ecart_sexe_age
        .dropna(subset=["ecart_hommes_femmes"])
        .sort_values("ordre_age")
        .copy()
    )

    # Première classe d'âge où l'estimation des hommes
    # devient supérieure à celle des femmes
    premier_ecart_positif = ecarts_age_sexe[
        ecarts_age_sexe["ecart_hommes_femmes"] > 0
    ].iloc[0]

    # Classe d'âge la plus élevée disponible
    age_max = ecarts_age_sexe.iloc[-1]
    
    # ========================================================
    # Lecture dynamique — dimensions sociales
    # ========================================================

    diplome_focus = (
        synthese_sociale.loc[
            (synthese_sociale["dimension"] == "diplome")
            & (synthese_sociale["indicateur"] == "Diabète déclaré")
        ]
        .iloc[0]
    )
    
    def format_number(value):
        return f"{value:.1f}".replace(".", ",")

    return html.Div(
        [
            
            # ====================================================
            # INTRODUCTION DU FOCUS
            # ====================================================

            html.P(
                "FOCUS · DIABÈTE",
                className="section-label",
            ),

            html.H1(
                "Le diabète comme cas d’étude des inégalités de santé"
            ),
            
            html.P(
                [
                    "L’analyse des inégalités sociales a déjà montré que le diabète déclaré "
                    "varie selon la situation financière, le niveau de diplôme et la catégorie "
                    "socioprofessionnelle. Parmi ces dimensions, le niveau de diplôme présente "
                    "l’écart le plus marqué : ",
                    html.Strong(
                        f"{format_number(abs(diplome_focus['ecart']))} points"
                    ),
                    " séparent ",
                    html.Strong(
                        diplome_focus["groupe_comparaison"]
                    ),
                    " de ",
                    html.Strong(
                        diplome_focus["groupe_reference"]
                    ),
                    ". Ce focus prolonge cette lecture en examinant maintenant une autre "
                    "dimension : l’âge et le sexe.",
                ],
                className="intro",
            ),
            
            # ====================================================
            # 1. ÂGE ET SEXE
            # ====================================================

            html.Div(
                [

                    html.Div(
                        [

                            html.H2(
                                "Le diabète déclaré augmente avec l’âge, "
                                "mais pas de la même manière chez les femmes et les hommes"
                            ),

                            html.P(
                                "Le Baromètre 2024 permet d'observer comment la fréquence "
                                "du diabète déclaré évolue selon l'âge et le sexe."
                            ),

                        ],
                        className="dashboard-header",
                    ),

                    html.Div(
                        [
                            html.Div(
                                [

                                    dcc.Graph(
                                        id="diabetes-age-sex-chart",

                                        figure=create_diabetes_age_sex_chart(
                                            diabete_age_sexe
                                        ),
                                        config=GRAPH_CONFIG,
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

                                            html.H3(
                                                "L’écart entre femmes et hommes "
                                                "s’accentue avec l’âge",
                                                className="dashboard-reading-title",
                                            ),

                                                                                        html.P(
                                                [
                                                    "À partir de ",
                                                    html.Strong(
                                                        premier_ecart_positif["classe_age"]
                                                    ),
                                                    ", le diabète déclaré devient plus fréquent chez les hommes. "
                                                    "Dans la classe ",
                                                    html.Strong(
                                                        age_max["classe_age"]
                                                    ),
                                                    ", ",
                                                    html.Strong(
                                                        f"{format_number(age_max['Hommes'])} %"
                                                    ),
                                                    " des hommes déclarent un diabète contre ",
                                                    html.Strong(
                                                        f"{format_number(age_max['Femmes'])} %"
                                                    ),
                                                    " des femmes, soit un écart de ",
                                                    html.Strong(
                                                        f"{format_number(age_max['ecart_hommes_femmes'])} points"
                                                    ),
                                                    ".",
                                                ],
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
                                                "Chaque point représente une estimation "
                                                "pour une classe d'âge et un sexe."
                                            ),

                                            html.P(
                                                "Les barres indiquent les intervalles "
                                                "de confiance à 95 %."
                                            ),

                                            html.P(
                                                "Les estimations non diffusées "
                                                "ne sont pas représentées."
                                            ),

                                            html.P(
                                                "Unité : part de la population (%)"
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
            
            # ====================================================
            # 2. TERRITOIRES ?
            # ====================================================
            
            
            # ====================================================
            # À RETENIR
            # ====================================================

            html.Div(
                [

                    html.P(
                        "À RETENIR",
                        className="section-label",
                    ),

                    html.P(
                        [
                            html.Strong(
                                "Le diabète déclaré cumule plusieurs dimensions d’inégalités. "
                            ),
                            "Les écarts sociaux observés précédemment se prolongent par des différences "
                            "démographiques nettes : avec l’âge, le diabète déclaré augmente fortement "
                            "et l’écart entre femmes et hommes devient particulièrement marqué dans "
                            "les classes d’âge les plus élevées."
                        ]
                    ),

                    html.P(
                        "Ces résultats restent descriptifs. Ils ne permettent pas, à eux seuls, "
                        "d’isoler un effet propre de chaque caractéristique.",
                        className="note",
                    ),

                ],
                className="takeaway",
            ),
            
            # ====================================================
            # SOURCES
            # ====================================================

            html.Div(
                [

                    html.Strong(
                        "Source : "
                    ),

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
                        " — Santé publique France, Odissé."
                    ),

                ],
                className="sources",
            ),
            
            # ====================================================
            # RETOUR AU PARCOURS PRINCIPAL
            # ====================================================

            html.Div(
                [

                    html.P(
                        "Ce focus constitue un approfondissement complémentaire. "
                        "Pour poursuivre l'exploration principale, revenons maintenant "
                        "à l'analyse des territoires."
                    ),

                    html.Button(
                        [
                            html.Span(
                                className="transition-arrow",
                                **{"aria-hidden": "true"},
                            ),
                            html.Span("Continuer vers Territoires & soins"),
                        ],
                        id="go-to-territoires-from-diabete",
                        className="transition-link",
                        n_clicks=0,
                    ),
                ],
                className="transition",
            ),
        ],
        className="tab-content",
    )

# ============================================================
# LAYOUT PRINCIPAL
# ============================================================

def create_layout(
    finance,
    synthese_sociale,
    analyse_regions,
    relations_territoriales,
    regions,
    profils_clusters,
    map_figure,
    diabete_age_sexe,
    diabete_ecart_sexe_age,
):

    return html.Div([
        
        dcc.Store(id="scroll-trigger"),
        
        dcc.Store(id="mobile-nav-close-trigger"),
        # ----------------------------------------------------
        # Navigation mobile
        # ----------------------------------------------------

        html.Details(
            [
                html.Summary(
                    [
                        html.Span(
                            "☰",
                            className="mobile-nav-icon",
                            **{"aria-hidden": "true"},
                        ),

                        html.Span(
                            "Accueil",
                            id="mobile-nav-current",
                            className="mobile-nav-current",
                        ),

                        html.Span(
                            "⌄",
                            className="mobile-nav-chevron",
                            **{"aria-hidden": "true"},
                        ),
                    ]
                ),

                html.Div(
                    [
                        html.Button(
                            "Accueil",
                            id="mobile-go-accueil",
                            className="mobile-nav-item",
                            n_clicks=0,
                        ),

                        html.Button(
                            "1 · Inégalités sociales",
                            id="mobile-go-social",
                            className="mobile-nav-item",
                            n_clicks=0,
                        ),

                        html.Button(
                            "2 · Territoires & soins",
                            id="mobile-go-territoires",
                            className="mobile-nav-item",
                            n_clicks=0,
                        ),

                        html.Button(
                            "3 · Profils territoriaux",
                            id="mobile-go-profils",
                            className="mobile-nav-item",
                            n_clicks=0,
                        ),
                        
                        html.Button(
                            "Bonus · Focus diabète",
                            id="mobile-go-diabete",
                            className="mobile-nav-item",
                            n_clicks=0,
                        ),
                        
                    ],
                    className="mobile-nav-menu",
                ),
            ],
            id="mobile-nav",
            className="mobile-nav",
            open=False,
        ),
        
        # ----------------------------------------------------
        # Onglets Dash + contenu de l'application
        # ----------------------------------------------------

        dcc.Tabs(
            id="main-tabs",
            value="accueil",
            mobile_breakpoint=0,
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
                
                dcc.Tab(
                    label="Bonus · Focus diabète",
                    value="diabete",
                    className="app-tab",
                    selected_className="app-tab app-tab--selected",

                    children=create_diabetes_focus(
                        diabete_age_sexe,
                        diabete_ecart_sexe_age,
                        synthese_sociale,
                    ),
                ),

            ],
        ),

    ], className="app-container")