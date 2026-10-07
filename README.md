# Odissé Dataviz Challenge 2026 - Inégalités sociales et territoriales de santé

**Équipe :** Chloé Martin  
**Mail de contact :** mailto:chloe_martin45@outlook.com   
**Défi :** Défi 3 — Inégalités sociales et territoriales de santé  

## Notre question

**Comment les inégalités sociales et territoriales de santé se combinent-elles avec l’accessibilité aux médecins généralistes pour caractériser différents profils régionaux en France métropolitaine ?**

La visualisation propose un parcours en trois étapes : 
- partir des écarts de santé observés selon plusieurs caractéristiques sociales, 
- changer ensuite d’échelle pour étudier les différences entre territoires, 
- puis combiner plusieurs dimensions afin de faire émerger différents profils régionaux.

Un **focus complémentaire sur le diabète** prolonge ce parcours sous la forme d’un cas d’étude. Il suit un même indicateur de santé à travers plusieurs angles d’analyse, social, démographique et territorial, afin d’illustrer concrètement le caractère multidimensionnel des inégalités de santé.
## Notre visualisation

**Lien vers l’application :** https://odisse-dataviz-challenge26-sante.onrender.com

L’application est hébergée gratuitement via Render. Un léger temps de chargement peut être nécessaire lors de la première ouverture après une période d’inactivité. 

La version mobile est fonctionnelle, mais l’affichage est plus confortable sur ordinateur.

La production prend la forme d’une **application web interactive développée avec Dash et Plotly**.

Elle est organisée autour de trois parties principales, complétées par un cas d’étude sur le diabète :

1. **Inégalités sociales**  
   Exploration des différences de santé selon la situation financière perçue, le niveau de diplôme et la catégorie socioprofessionnelle.

2. **Territoires & soins**  
   Analyse des relations entre défavorisation territoriale, accessibilité aux médecins généralistes et indicateurs de santé à l’échelle des 13 régions métropolitaines.

3. **Profils territoriaux**  
   Combinaison de six indicateurs afin d’identifier quatre configurations régionales, puis exploration interactive de chaque région à travers une carte et un profil standardisé.

**Focus · Diabète — cas d’étude complémentaire**  
Le diabète déclaré est suivi selon plusieurs dimensions : niveau de diplôme, âge, sexe et contexte territorial. Une analyse régionale compare également le niveau observé de diabète à la valeur suggérée par la tendance avec le FDep afin de repérer les régions qui s’en écartent davantage.

L’objectif n’est pas d’établir un classement des régions, mais de montrer que les inégalités de santé résultent de configurations multidimensionnelles. Une meilleure accessibilité aux médecins généralistes ne coïncide notamment pas systématiquement avec des indicateurs de santé plus favorables, et un même indicateur comme le diabète peut faire apparaître des écarts différents selon l’angle d’analyse retenu.

## Les données utilisées

| Source | Jeu de données | Lien |
|---|---|---|
| Santé publique France — Odissé | Santé générale — Indicateurs du Baromètre 2024 | https://odisse.santepubliquefrance.fr/explore/assets/sante_generale_indicateurs_barometre_2024/ |
| Santé publique France — Odissé | Diabète — Indicateurs du Baromètre 2024 | https://odisse.santepubliquefrance.fr/explore/assets/diabete-indicateurs-du-barometre-2024/ |
| Santé publique France — Odissé | Indice de défavorisation sociale FDep par commune | https://odisse.santepubliquefrance.fr/explore/assets/indice-de-defavorisation-sociale-fdep-par-commune/ |
| Santé publique France — Odissé | French European Deprivation Index — F-EDI 2021 | https://odisse.santepubliquefrance.fr/explore/assets/french-european-deprivation-index-f-edi-2021-par-commune/ |
| Observatoire des territoires | Accessibilité potentielle localisée (APL) aux médecins généralistes — 2023 | https://www.observatoire-des-territoires.gouv.fr/accessibilite-potentielle-localisee-apl-aux-medecins-generalistes |
| Insee | Populations communales 2023 | https://www.insee.fr/fr/statistiques/8680726 |

**Source de contexte pour l’introduction :** les chiffres nationaux mentionnés au début de l’application, notamment les 68 % d’adultes déclarant une bonne ou très bonne santé et les 26 % déclarant une limitation dans leurs activités habituelles depuis au moins six mois, proviennent de la publication *Santé générale — Baromètre de Santé publique France 2024* :  
https://www.santepubliquefrance.fr/sites/default/files/rdd/document/907125_spf00006377.pdf

Les données mobilisées ne correspondent pas toutes exactement à la même année : 
- FDep repose sur des données socio-économiques 2020 ;
- F-EDI sur 2021 ;
- l’APL et la population sur 2023 ;
- les indicateurs de santé sur le Baromètre 2024.

Pour les analyses régionales, le FDep, le F-EDI et l’APL sont agrégés à l’échelle régionale par **moyenne pondérée par la population communale 2023**. Les indicateurs du Baromètre 2024 sont utilisés directement à leur échelle régionale.

## Démarche d'analyse

Le projet est organisé en trois niveaux distincts : **exploration**, **préparation/analyse**, puis **datavisualisation**.

### 1. Exploration des données

Une première phase exploratoire a été réalisée dans des fichiers **Quarto (`.qmd`)**.

Ces fichiers ont servi à :

- découvrir la structure des différentes bases ;
- vérifier la qualité et la disponibilité des variables ;
- tester des rapprochements entre sources ;
- explorer plusieurs pistes d’analyse ;
- produire les premières statistiques et visualisations ;
- identifier les axes finalement retenus pour la datavisualisation.

Ces notebooks constituent donc une phase de recherche et d’exploration en amont du pipeline final.

### 2. Préparation et analyse sous R

```text
R/
├── 01_prepare_social.R
├── 02_prepare_territoire.R
├── 03_prepare_region.R
├── 04_analyses.R
└── 05_focus_diabete.R
```
Ces scripts assurent notamment :

- le nettoyage et l’harmonisation des données ;
- les jointures entre les différentes sources ;
- l’agrégation des indicateurs territoriaux ;
- la pondération par la population ;
- la préparation des indicateurs sociaux ;
- les analyses de corrélation ;
- la standardisation des variables ;
- la construction des profils territoriaux ;
- les analyses de sensibilité ;
- la préparation du focus diabète selon l’âge et le sexe ;
- l’estimation d’un modèle linéaire exploratoire entre FDep régional et diabète déclaré, puis le calcul des résidus régionaux.
  
Les fichiers utilisés par l’application Python sont exclusivement des exports produits à l’issue de cette chaîne de préparation sous R.

Autrement dit, l’application Dash ne refait pas les traitements statistiques lourds au démarrage : elle charge des fichiers déjà nettoyés, agrégés et préparés en amont.

Les résultats intermédiaires et finaux sont exportés vers :

```text
data/
├── raw/
│   └── données téléchargées depuis les sources initiales
│
└── processed/
    └── fichiers CSV et GeoJSON produits par les scripts R
```

Cette organisation permet de séparer clairement :

```text
Données brutes
      ↓
Exploration dans les fichiers .qmd
      ↓
Préparation et analyses sous R
      ↓
Exports dans data/processed
      ↓
Application Python / Dash
```

## Méthode

Les analyses territoriales portent sur les **13 régions métropolitaines**.

La dernière partie de la visualisation combine six indicateurs :

- FDep ;
- F-EDI ;
- APL aux médecins généralistes ;
- santé perçue ;
- limitation d’activité ;
- diabète déclaré.

Les indicateurs sont standardisés afin de les rendre comparables malgré leurs unités différentes.

Leur orientation est harmonisée : 
- une valeur positive correspond à une situation relativement plus défavorable ;
- une valeur négative à une situation relativement plus favorable.

Une **classification hiérarchique** permet ensuite de rapprocher les régions présentant les configurations les plus similaires. Quatre profils territoriaux ont été retenus.

Des analyses de sensibilité ont également été réalisées en faisant varier le nombre de groupes et en retirant successivement le F-EDI et l’APL.

### Focus diabète : lecture complémentaire

Le focus diabète reprend un seul indicateur de santé afin d’observer comment les écarts varient selon plusieurs dimensions.

Deux analyses complémentaires sont proposées :

- une comparaison du diabète déclaré selon **l’âge et le sexe**, avec les intervalles de confiance à 95 % fournis par le Baromètre 2024 ;
- une analyse territoriale exploratoire reliant le **FDep régional** au **diabète déclaré** à l’aide d’un modèle linéaire simple.

Pour chaque région, l’écart entre la valeur observée et la valeur estimée par cette tendance est calculé. Un résidu positif correspond à davantage de diabète déclaré que ne le suggère la tendance générale, tandis qu’un résidu négatif correspond à une valeur plus faible.

Cette analyse porte sur seulement 13 régions métropolitaines. Elle sert à décrire des écarts à une tendance générale et ne constitue ni un classement des régions ni une démonstration causale.

Ces analyses restent exploratoires : les relations observées ne permettent pas d’établir de causalité et les indices de défavorisation utilisés sont des indicateurs écologiques caractérisant les territoires, et non la situation individuelle de leurs habitants.

Les définitions des indicateurs, leurs unités et leur sens de lecture, ainsi que les principales précautions d’interprétation et la méthode de construction des profils territoriaux, sont également présentés directement dans l’interface de l’application. La partie consacrée aux profils détaille notamment la standardisation des indicateurs, la classification hiérarchique, le choix des quatre groupes et les analyses de sensibilité réalisées.

## Les outils employés

### Exploration, préparation et analyse des données

- **R**
- **Quarto** (`.qmd`)
- tidyverse
- sf
- analyses statistiques
- standardisation
- classification hiérarchique

### Datavisualisation et application

- **Python**
- Dash
- Plotly
- pandas
- HTML / CSS

L’identité visuelle de l’application s’appuie sur les couleurs de la charte graphique d’Odissé, adaptées à l’interface afin de conserver une cohérence visuelle avec l’univers du challenge tout en assurant la lisibilité des visualisations.

### Gestion de l'environnement Python

- **uv**

`uv` est utilisé pour gérer l'environnement Python, les dépendances du projet et l'exécution de l'application de manière reproductible.

## Structure du projet

```
Odisse_Challenge26/
│
├── README.md
├── pyproject.toml
├── uv.lock
│
├── exploration/
│   └── fichiers .qmd utilisés pour l’exploration initiale
│
├── R/
│   ├── 01_prepare_social.R
│   ├── 02_prepare_territoire.R
│   ├── 03_prepare_region.R
│   ├── 04_analyses.R
│   └── 05_focus_diabete.R
│
├── data/
│   ├── raw/
│   │   └── données téléchargées depuis les sources initiales
│   │
│   └── processed/
│       └── données préparées et exportées depuis R
│
└── app/
    ├── app.py
    ├── callbacks.py
    ├── charts.py
    ├── data.py
    ├── layout.py
    ├── maps.py
    │
    └── assets/
        └── style.css
```

## Organisation de l'application

- `app.py` : initialisation de l’application et chargement des données ;
- `data.py` : lecture des fichiers préparés présents dans data/processed ;
- `layout.py` : structure et contenu de l’interface ;
- `callbacks.py` : gestion des interactions ;
- `charts.py` : construction des graphiques Plotly ;
- `maps.py` : construction des cartes des profils territoriaux et du focus diabète ;
- `assets/style.css` : mise en forme de l’application.

Cette organisation permet de conserver une séparation entre **traitement des données**, **analyse statistique**, **visualisation** et **interface**.

## Lancer le projet localement 

### Prérequis 

Le projet utilise **Python** et **uv**.

Installer `uv` si nécessaire :

```bash
pip install uv
```

### Installation

Cloner le dépôt : 

```bash
git clone https://github.com/ChloMartin45/Odisse_Challenge26
cd Odisse_Challenge26
```

Installer l'environnement et les dépendances :
```bash
uv sync
```

### Lancement de l'application

Depuis la racine du projet :

```bash
uv run app/app.py
```

L’application est ensuite accessible à l’adresse indiquée dans le terminal.

## Licence

Le code source de ce projet est publié sous **licence MIT**.

Les contenus textuels et visuels produits dans le cadre du projet sont mis à disposition sous **Creative Commons CC-BY 4.0**.

Les données réutilisées conservent les licences définies par leurs producteurs, notamment la **Licence Ouverte 2.0** pour les données issues d’Odissé.