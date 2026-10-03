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
            "La santé ne se distribue pas uniformément dans la population "
            "ni sur le territoire. Cette datavisualisation explore les liens "
            "entre situation sociale, caractéristiques territoriales, "
            "accessibilité aux soins et état de santé.",
            className="intro",
        ),

        # ----------------------------------------------------
        # Problématique
        # ----------------------------------------------------

        html.Div([

            html.P(
                "NOTRE QUESTION",
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
            "Trois étapes pour explorer la question"
        ),

        html.Div([

            html.Div([
                html.P("01", className="step-number"),
                html.H3("Inégalités sociales"),
                html.P(
                    "Observer les différences de santé selon la situation "
                    "financière, le diplôme et la catégorie socioprofessionnelle."
                ),
            ], className="step-card"),

            html.Div([
                html.P("02", className="step-number"),
                html.H3("Territoires & soins"),
                html.P(
                    "Étudier les relations entre défavorisation territoriale, "
                    "accessibilité aux médecins généralistes et santé."
                ),
            ], className="step-card"),

            html.Div([
                html.P("03", className="step-number"),
                html.H3("Profils territoriaux"),
                html.P(
                    "Combiner ces dimensions pour explorer différents "
                    "profils régionaux."
                ),
            ], className="step-card"),

        ], className="steps"),

        # ----------------------------------------------------
        # Données
        # ----------------------------------------------------

        html.Div([

            html.H2("Données mobilisées"),

            html.P(
                "Cette exploration croise des données de santé, "
                "de défavorisation sociale, d'accessibilité aux soins "
                "et de population."
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
                "Cette datavisualisation a été réalisée dans le cadre "
                "de l'Odissé Dataviz Challenge 2026, autour des "
                "inégalités sociales et territoriales de santé."
            ),

        ], className="about-challenge"),

    ], className="tab-content")


# ============================================================
# 01 — INÉGALITÉS SOCIALES
# ============================================================

def create_social_summary(synthese_sociale):

    # Ordre d'affichage
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
        "Limitation d'activité": "Limitation d'activité",
        "Diabète déclaré": "Diabète déclaré",
    }

    # --------------------------------------------------------
    # En-têtes
    # --------------------------------------------------------

    elements = [
        html.Div(
            "",
            className="summary-cell summary-header",
        )
    ]

    for indicateur in indicateurs:
        elements.append(
            html.Div(
                labels_indicateurs[indicateur],
                className="summary-cell summary-header",
            )
        )

    # --------------------------------------------------------
    # Lignes de la synthèse
    # --------------------------------------------------------

    for dimension in dimensions:

        donnees_dimension = synthese_sociale[
            synthese_sociale["dimension"] == dimension
        ]

        if donnees_dimension.empty:
            continue

        dimension_label = donnees_dimension[
            "dimension_label"
        ].iloc[0]

        # Comparaisons utilisées
        comparaisons = (
            donnees_dimension[
                ["groupe_reference", "groupe_comparaison"]
            ]
            .drop_duplicates()
        )

        # Finance et diplôme :
        # la comparaison est identique pour les trois indicateurs.
        if len(comparaisons) == 1:

            groupe_reference = comparaisons.iloc[0][
                "groupe_reference"
            ]

            groupe_comparaison = comparaisons.iloc[0][
                "groupe_comparaison"
            ]

            comparaison_label = (
                f"{groupe_comparaison} vs "
                f"{groupe_reference}"
            )

        # PCS :
        # les catégories extrêmes peuvent dépendre
        # de l'indicateur.
        else:
            comparaison_label = (
                "Valeurs extrêmes observées*"
            )

        elements.append(
            html.Div(
                [
                    html.Strong(dimension_label),
                    html.Span(
                        comparaison_label,
                        className="summary-comparison",
                    ),
                ],
                className="summary-cell summary-row-label",
            )
        )

        # ----------------------------------------------------
        # Valeurs des trois indicateurs
        # ----------------------------------------------------

        for indicateur in indicateurs:

            ligne = donnees_dimension[
                donnees_dimension["indicateur"]
                == indicateur
            ]

            if ligne.empty:
                elements.append(
                    html.Div(
                        "—",
                        className="summary-cell",
                    )
                )
                continue

            ligne = ligne.iloc[0]

            ecart = ligne["ecart"]
            type_comparaison = ligne["type_comparaison"]

            valeur = (
                f"{abs(ecart):.1f}"
                .replace(".", ",")
            )

            # PCS : amplitude entre les extrêmes observés
            if type_comparaison == "extremes_observes":

                texte_direction = " d'écart"

            # Finance / diplôme :
            # direction de l'écart par rapport à la référence
            elif ecart < 0:

                texte_direction = " de moins"

            else:

                texte_direction = " de plus"

            elements.append(
                html.Div(
                    [
                        html.Strong(
                            f"{valeur} pts"
                        ),
                        html.Span(
                            texte_direction
                        ),
                    ],
                    className="summary-cell",
                    title=(
                        f"{ligne['groupe_comparaison']} : "
                        f"{ligne['valeur_comparaison']:.1f} % | "
                        f"{ligne['groupe_reference']} : "
                        f"{ligne['valeur_reference']:.1f} %"
                    ),
                )
            )

    return html.Div(
        elements,
        className="summary-grid",
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
        ),

        html.P(
            "Lecture : chaque point représente une région métropolitaine. "
            "Le coefficient r mesure l'intensité et le sens de la relation "
            "linéaire entre les deux indicateurs.",
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

def create_profiles_tab(map_figure):

    return html.Div([

        # ----------------------------------------------------
        # Introduction
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # Méthode simplifiée
        # ----------------------------------------------------

        html.Div([

            html.H2(
                "Six indicateurs pour comparer les territoires"
            ),

            html.P(
                "Les 13 régions métropolitaines sont comparées à partir "
                "de six indicateurs décrivant leur contexte social, "
                "leur accessibilité aux médecins généralistes et "
                "l'état de santé de leur population."
            ),

            html.Div([

                html.Div([
                    html.Strong("Défavorisation"),
                    html.P("FDep et F-EDI"),
                ], className="indicator-card"),

                html.Div([
                    html.Strong("Accessibilité aux soins"),
                    html.P(
                        "APL aux médecins généralistes"
                    ),
                ], className="indicator-card"),

                html.Div([
                    html.Strong("Santé"),
                    html.P(
                        "Santé perçue, limitation d'activité "
                        "et diabète déclaré"
                    ),
                ], className="indicator-card"),

            ], className="indicator-grid"),

            html.P(
                "Une classification exploratoire rapproche les régions "
                "présentant des caractéristiques similaires. "
                "Quatre profils territoriaux se dégagent de cette analyse.",
                className="graph-note",
            ),

        ], className="reading-guide"),

        # ----------------------------------------------------
        # Les quatre profils
        # ----------------------------------------------------

        html.H2(
            "Quatre profils territoriaux se dégagent"
        ),

        html.P(
            "Ces profils ne constituent pas un classement des régions. "
            "Ils décrivent différentes combinaisons des caractéristiques "
            "sociales, de l'accessibilité aux soins et de la santé."
        ),

        html.Div([

            html.Div([
                html.Strong(
                    "Profil francilien atypique"
                ),
                html.P(
                    "Un profil propre à l'Île-de-France, qui se distingue "
                    "des autres régions par une combinaison particulière "
                    "des indicateurs étudiés."
                ),
                html.P(
                    "1 région : Île-de-France",
                    className="profile-regions",
                ),
            ], className="profile-card"),

            html.Div([
                html.Strong(
                    "Profil territorial globalement favorable"
                ),
                html.P(
                    "Des régions présentant globalement des indicateurs "
                    "plus favorables que la moyenne des régions étudiées "
                    "sur plusieurs dimensions."
                ),
                html.P(
                    "3 régions : Pays de la Loire, Bretagne "
                    "et Auvergne-Rhône-Alpes",
                    className="profile-regions",
                ),
            ], className="profile-card"),

            html.Div([
                html.Strong(
                    "Profil de santé contrasté"
                ),
                html.P(
                    "Des territoires dont les indicateurs ne vont pas "
                    "tous dans le même sens, faisant apparaître une "
                    "configuration de santé plus contrastée."
                ),
                html.P(
                    "4 régions : Nouvelle-Aquitaine, Occitanie, "
                    "Provence-Alpes-Côte d'Azur et Corse",
                    className="profile-regions",
                ),
            ], className="profile-card"),

            html.Div([
                html.Strong(
                    "Profil de défavorisation et de santé défavorable"
                ),
                html.P(
                    "Des régions qui cumulent davantage de caractéristiques "
                    "territoriales et sanitaires défavorables relativement "
                    "aux autres régions étudiées."
                ),
                html.P(
                    "5 régions : Centre-Val de Loire, "
                    "Bourgogne-Franche-Comté, Normandie, "
                    "Hauts-de-France et Grand Est",
                    className="profile-regions",
                ),
            ], className="profile-card"),

        ], className="profiles-grid"),

        # ----------------------------------------------------
        # Carte
        # ----------------------------------------------------

        html.H2(
            "Comment ces profils se répartissent-ils "
            "sur le territoire ?"
        ),

        html.P(
            "La carte représente le profil auquel appartient chaque "
            "région métropolitaine étudiée. Cliquez sur une région "
            "pour explorer ses indicateurs."
        ),

        dcc.Graph(
            id="map-profiles",
            figure=map_figure,
            config={
                "scrollZoom": False,
                "displayModeBar": False,
                "doubleClick": False,
            },
        ),

        # ----------------------------------------------------
        # Exploration d'une région
        # ----------------------------------------------------

        html.Div(
            id="region-details",
            children=[

                html.H2(
                    "Explorer une région"
                ),

                html.P(
                    "Sélectionnez une région sur la carte pour afficher "
                    "ses indicateurs et situer son profil par rapport "
                    "aux 13 régions étudiées."
                ),

            ],
            className="region-details",
        ),

        # Le graphique sera masqué tant qu'aucune région
        # n'est sélectionnée grâce au callback.

        html.Div(
            id="region-profile-container",
            children=[

                html.Div([

                    html.H3(
                        "Comment lire ce graphique ?"
                    ),

                    html.P(
                        "Les indicateurs sont standardisés par rapport "
                        "aux 13 régions étudiées. La ligne 0 représente "
                        "leur moyenne. Ils ont été orientés dans le même "
                        "sens : une valeur positive correspond à une "
                        "situation relativement plus défavorable et une "
                        "valeur négative à une situation relativement "
                        "plus favorable."
                    ),

                ], className="reading-guide"),

                dcc.Graph(
                    id="region-profile"
                ),

            ],
            style={"display": "none"},
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
                "Les régions ne se différencient pas selon une seule "
                "dimension. La combinaison de la défavorisation "
                "territoriale, de l'accessibilité aux soins et des "
                "indicateurs de santé fait apparaître plusieurs "
                "configurations territoriales. L'accès aux soins "
                "contribue ainsi à caractériser les territoires, "
                "mais ne résume pas à lui seul les inégalités de "
                "santé observées."
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
                "Cette typologie est exploratoire et porte sur "
                "13 régions métropolitaines. Elle décrit des proximités "
                "entre territoires à partir des indicateurs retenus "
                "et ne constitue ni un classement ni une typologie "
                "définitive des régions françaises."
            ),

            html.P(
                "Le profil francilien est constitué de la seule "
                "Île-de-France. Son interprétation doit donc être "
                "particulièrement prudente."
            ),

        ], className="method-note"),

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
    map_figure,
):

    return html.Div([

        dcc.Tabs(
            id="main-tabs",
            value="accueil",

            children=[

                dcc.Tab(
                    label="Accueil",
                    value="accueil",
                    children=create_home_tab(),
                ),

                dcc.Tab(
                    label="1 · Inégalités sociales",
                    value="social",
                    children=create_social_tab(
                        finance,
                        synthese_sociale,
                    ),
                ),

                dcc.Tab(
                    label="2 · Territoires & soins",
                    value="territoires",
                    children=create_territorial_tab(
                        analyse_regions,
                        relations_territoriales,
                    ),
                ),

                dcc.Tab(
                    label="3 · Profils territoriaux",
                    value="profils",
                    children=create_profiles_tab(
                        map_figure
                    ),
                ),

            ],
        ),

    ], className="app-container")