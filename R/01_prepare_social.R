# 01_prepare_social
# Préparation des indicateurs sociaux et de santé

# Packages
  
library(tidyverse)

# Chemins

raw_dir <- "../data/raw"
processed_dir <- "../data/processed"

dir.create(
  processed_dir,
  recursive = TRUE,
  showWarnings = FALSE
)

# Importation des données

## Santé générale

sante <- read_csv(
  file.path(
    raw_dir,
    "sante_generale_indicateurs_barometre_2024.csv"
  ),
  show_col_types = FALSE
)

## Diabète déclaré

diabete <- read_csv(
  file.path(
    raw_dir,
    "diabete-indicateurs-du-barometre-2024.csv"
  ),
  show_col_types = FALSE
)

# Préparation des données

# Les variables numériques utilisées dans l'analyse sont converties explicitement afin de sécuriser les traitements ultérieurs.

sante <- sante |>
  mutate(
    Estimation = as.numeric(Estimation),
    ic_inf = as.numeric(ic_inf),
    ic_sup = as.numeric(ic_sup),
    Effectif.Brut = as.numeric(`Effectif Brut`),
    Année = as.integer(Année)
  )

diabete |>
  summarise(
    nb_moins30_estimation = sum(Estimation == -30, na.rm = TRUE),
    nb_moins30_ic_inf = sum(ic_inf == -30, na.rm = TRUE),
    nb_moins30_ic_sup = sum(ic_sup == -30, na.rm = TRUE)
  )

# Les estimations égales à -30 correspondent à des valeurs non diffusées
# en raison d'un effectif de répondants inférieur au seuil de 30.

diabete <- diabete |>
  mutate(
    Estimation = as.numeric(Estimation),
    Estimation = na_if(Estimation, -30),
    
    ic_inf = as.numeric(ic_inf),
    ic_sup = as.numeric(ic_sup),
    Effectif.Brut = as.numeric(`Effectif Brut`),
    Année = as.integer(Année)
  )

sante <- sante |>
  filter(Année == 2024)

diabete <- diabete |>
  filter(Année == 2024)

# Contrôle des données importées

diabete |>
  summarise(
    nb_ic_inf_codees_moins30 = sum(ic_inf == -30, na.rm = TRUE),
    nb_ic_sup_codees_moins30 = sum(ic_sup == -30, na.rm = TRUE)
  )

sante |>
  summarise(
    nb_observations = n(),
    nb_indicateurs = n_distinct(Indicateur),
    nb_regions = n_distinct(`Nouvelles régions`),
    nb_annees = n_distinct(Année),
    nb_estimation_manquante = sum(is.na(Estimation))
  )

diabete |>
  summarise(
    nb_observations = n(),
    nb_indicateurs = n_distinct(Indicateur),
    nb_regions = n_distinct(`Nouvelles régions`),
    nb_annees = n_distinct(Année),
    nb_estimation_manquante = sum(is.na(Estimation))
  )

# Sélection des indicateurs étudiés

# Trois indicateurs sont retenus :
 # - santé perçue bonne ou très bonne ;
 # - limitation d'activité ;
 # - diabète déclaré.


sante_indicateurs <- sante |> 
  filter(
    Indicateur %in% c(
      "Limitation d'activité",
      "Santé perçue bonne ou très bonne"
      )
    )


diabete_declare <- diabete |> 
  filter(
    Indicateur == "Diabète déclaré"
    )


# Préparation des indicateurs régionaux

# Les analyses territoriales utilisent les estimations régionales pour l'ensemble de la population, 
# sans ventilation par sexe, âge, diplôme, PCS ou situation financière.


sante_regions <- sante_indicateurs |>
  filter(
    Sexe == "Tous",
    `Classe d'âge` == "Tous",
    Diplôme == "Tous",
    PCS == "Tous",
    `Situation financière perçue` == "Tous",
    `Nouvelles régions` != "Tous"
  )


diabete_regions <- diabete_declare |>
  filter(
    Sexe == "Tous",
    `Classe d'âge` == "Tous",
    Diplôme == "Tous",
    PCS == "Tous",
    `Situation financière perçue` == "Tous",
    `Nouvelles régions` != "Tous"
  )


## Contrôle des données régionales

sante_regions |>
  summarise(
    nb_observations = n(),
    nb_regions = n_distinct(`Nouvelles régions`),
    nb_indicateurs = n_distinct(Indicateur),
    nb_estimations_manquantes = sum(is.na(Estimation))
  )

diabete_regions |>
  summarise(
    nb_observations = n(),
    nb_regions = n_distinct(`Nouvelles régions`),
    nb_indicateurs = n_distinct(Indicateur),
    nb_estimations_manquantes = sum(is.na(Estimation))
  )


sante_regions |>
  distinct(`Nouvelles régions`) |>
  arrange(`Nouvelles régions`)

diabete_regions |>
  distinct(`Nouvelles régions`) |>
  arrange(`Nouvelles régions`)


# Indicateurs selon la situation financière perçue

# Les indicateurs nationaux sont extraits en maintenant les autres dimensions sociodémographiques à la modalité « Tous ».


sante_finance <- sante_indicateurs |>
  filter(
    Sexe == "Tous",
    `Classe d'âge` == "Tous",
    Diplôme == "Tous",
    PCS == "Tous",
    !is.na(`Situation financière perçue`),
    `Situation financière perçue` != "Tous",
    `Nouvelles régions` == "Tous"
  ) |>
  select(
    Indicateur,
    `Situation financière perçue`,
    Estimation,
    ic_inf,
    ic_sup,
    Effectif.Brut
  )

diabete_finance <- diabete_declare |>
  filter(
    Sexe == "Tous",
    `Classe d'âge` == "Tous",
    Diplôme == "Tous",
    PCS == "Tous",
    !is.na(`Situation financière perçue`),
    `Situation financière perçue` != "Tous",
    `Nouvelles régions` == "Tous"
  ) |>
  select(
    Indicateur,
    `Situation financière perçue`,
    Estimation,
    ic_inf,
    ic_sup,
    Effectif.Brut
  )


indicateurs_finance <- bind_rows(
  sante_finance,
  diabete_finance
) |>
  mutate(
    situation_financiere = case_when(
      `Situation financière perçue` ==
        "Vous êtes à l’aise" ~ "À l'aise",

      `Situation financière perçue` ==
        "Ça va" ~ "Ça va",

      `Situation financière perçue` ==
        "C’est juste, il faut faire attention" ~ "C'est juste",

      `Situation financière perçue` ==
        "Vous y arrivez difficilement ou vous ne pouvez pas y arriver sans faire de dette" ~
        "Difficultés financières",

      TRUE ~ `Situation financière perçue`
    ),

    situation_financiere = factor(
      situation_financiere,
      levels = c(
        "À l'aise",
        "Ça va",
        "C'est juste",
        "Difficultés financières"
      )
    )
  )


# Indicateurs selon le niveau de diplôme


sante_diplome <- sante_indicateurs |>
  filter(
    Sexe == "Tous",
    `Classe d'âge` == "Tous",
    Diplôme != "Tous",
    PCS == "Tous",
    `Situation financière perçue` == "Tous",
    `Nouvelles régions` == "Tous"
  ) |>
  select(
    Indicateur,
    Diplôme,
    Estimation,
    ic_inf,
    ic_sup,
    Effectif.Brut
  )

diabete_diplome <- diabete_declare |>
  filter(
    Sexe == "Tous",
    `Classe d'âge` == "Tous",
    !is.na(Diplôme),
    Diplôme != "Tous",
    PCS == "Tous",
    `Situation financière perçue` == "Tous",
    `Nouvelles régions` == "Tous"
  ) |>
  select(
    Indicateur,
    Diplôme,
    Estimation,
    ic_inf,
    ic_sup,
    Effectif.Brut
  )



indicateurs_diplome <- bind_rows(
  sante_diplome,
  diabete_diplome
) |>
  mutate(
    Diplôme = factor(
      Diplôme,
      levels = c(
        "Aucun diplôme ou inférieur au Bac",
        "Bac",
        "Supérieur au Bac"
      )
    )
  )


# Indicateurs selon la catégorie socioprofessionnelle


sante_pcs <- sante_indicateurs |>
  filter(
    Sexe == "Tous",
    `Classe d'âge` == "Tous",
    Diplôme == "Tous",
    !is.na(PCS),
    PCS != "Tous",
    `Situation financière perçue` == "Tous",
    `Nouvelles régions` == "Tous"
  ) |>
  select(
    Indicateur,
    PCS,
    Estimation,
    ic_inf,
    ic_sup,
    Effectif.Brut
  )

diabete_pcs <- diabete_declare |>
  filter(
    Sexe == "Tous",
    `Classe d'âge` == "Tous",
    Diplôme == "Tous",
    !is.na(PCS),
    PCS != "Tous",
    `Situation financière perçue` == "Tous",
    `Nouvelles régions` == "Tous"
  ) |>
  select(
    Indicateur,
    PCS,
    Estimation,
    ic_inf,
    ic_sup,
    Effectif.Brut
  )


indicateurs_pcs <- bind_rows(
  sante_pcs,
  diabete_pcs
)


# Synthèse des écarts sociaux de santé

  #La synthèse utilisée dans l'application compare les situations extrêmes pour chaque dimension sociale.

  #Pour la situation financière et le diplôme, les catégories comparées sont définies par l'ordre de la variable.

  #Pour la catégorie socioprofessionnelle, qui ne constitue pas une échelle ordonnée, l'écart correspond uniquement 
  #à l'amplitude entre les valeurs minimale et maximale observées pour chaque indicateur.

## Situation financière


synthese_finance <- indicateurs_finance |>
  filter(
    situation_financiere %in% c(
      "À l'aise",
      "Difficultés financières"
    )
  ) |>
  mutate(
    situation_financiere = as.character(situation_financiere)
  ) |>
  select(
    Indicateur,
    situation_financiere,
    Estimation
  ) |>
  pivot_wider(
    names_from = situation_financiere,
    values_from = Estimation
  ) |>
  transmute(
    dimension = "finance",
    dimension_label = "Situation financière",
    indicateur = Indicateur,

    groupe_reference = "À l'aise",
    valeur_reference = `À l'aise`,

    groupe_comparaison = "Difficultés financières",
    valeur_comparaison = `Difficultés financières`,

    ecart = valeur_comparaison - valeur_reference,

    type_comparaison = "categories_ordonnees"
  )


## Niveau de diplôme 

# Pour faciliter la lecture, la catégorie présentant le niveau de diplôme le plus élevé est utilisée comme référence.


synthese_diplome <- indicateurs_diplome |>
  filter(
    Diplôme %in% c(
      "Aucun diplôme ou inférieur au Bac",
      "Supérieur au Bac"
    )
  ) |>
  mutate(
    Diplôme = as.character(Diplôme)
  ) |>
  select(
    Indicateur,
    Diplôme,
    Estimation
  ) |>
  pivot_wider(
    names_from = Diplôme,
    values_from = Estimation
  ) |>
  transmute(
    dimension = "diplome",
    dimension_label = "Niveau de diplôme",
    indicateur = Indicateur,

    groupe_reference = "Supérieur au Bac",
    valeur_reference = `Supérieur au Bac`,

    groupe_comparaison = "Aucun diplôme ou inférieur au Bac",
    valeur_comparaison = `Aucun diplôme ou inférieur au Bac`,

    ecart = valeur_comparaison - valeur_reference,

    type_comparaison = "categories_ordonnees"
  )


## Catégorie socioprofessionnelle


synthese_pcs <- indicateurs_pcs |>
  filter(!is.na(Estimation)) |>
  group_by(Indicateur) |>
  summarise(
    groupe_reference = PCS[which.min(Estimation)],
    valeur_reference = min(Estimation),

    groupe_comparaison = PCS[which.max(Estimation)],
    valeur_comparaison = max(Estimation),

    ecart = valeur_comparaison - valeur_reference,

    .groups = "drop"
  ) |>
  mutate(
    dimension = "pcs",
    dimension_label = "Catégorie socioprofessionnelle",
    type_comparaison = "extremes_observes"
  ) |>
  select(
    dimension,
    dimension_label,
    indicateur = Indicateur,
    groupe_reference,
    valeur_reference,
    groupe_comparaison,
    valeur_comparaison,
    ecart,
    type_comparaison
  )


## Construction de la base de synthèse 


synthese_sociale <- bind_rows(
  synthese_finance,
  synthese_diplome,
  synthese_pcs
) |>
  mutate(
    indicateur = factor(
      indicateur,
      levels = c(
        "Santé perçue bonne ou très bonne",
        "Limitation d'activité",
        "Diabète déclaré"
      )
    ),

    dimension = factor(
      dimension,
      levels = c(
        "finance",
        "diplome",
        "pcs"
      )
    )
  ) |>
  arrange(
    dimension,
    indicateur
  )


## Contrôle de la synthèse

  # On attend trois dimensions sociales × trois indicateurs de santé, soit neuf comparaisons.


synthese_sociale

synthese_sociale |>
  count(dimension)

synthese_sociale |>
  summarise(
    nb_lignes = n(),
    nb_dimensions = n_distinct(dimension),
    nb_indicateurs = n_distinct(indicateur),
    nb_ecarts_manquants = sum(is.na(ecart))
  )


# Contrôle des estimations de diabète utilisées dans les analyses

bind_rows(
  regions = diabete_regions,
  finance = diabete_finance,
  diplome = diabete_diplome,
  pcs = diabete_pcs,
  .id = "analyse"
) |>
  group_by(analyse) |>
  summarise(
    nb_observations = n(),
    nb_estimations_manquantes = sum(is.na(Estimation)),
    .groups = "drop"
  )


# Export des données préparées 

  # Seules les bases nécessaires aux étapes suivantes du projet ou à l'application sont exportées.


write_csv(
  sante_regions,
  file.path(processed_dir, "sante_regions.csv")
)

write_csv(
  diabete_regions,
  file.path(processed_dir,"diabete_regions.csv")
)

write_csv(
  indicateurs_finance,
  file.path(processed_dir, "indicateurs_finance.csv")
)

write_csv(
  indicateurs_diplome,
  file.path(processed_dir, "indicateurs_diplome.csv")
)

write_csv(
  indicateurs_pcs,
  file.path(processed_dir, "indicateurs_pcs.csv")
)

write_csv(
  synthese_sociale,
  file.path(processed_dir, "synthese_sociale.csv")
)

