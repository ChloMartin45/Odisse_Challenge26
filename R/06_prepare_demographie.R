# Packages

library(tidyverse)
library(readxl)

# Chemins
raw_dir <- "../data/raw"
processed_dir <- "../data/processed"

dir.create(
  processed_dir,
  recursive = TRUE,
  showWarnings = FALSE
)

# Importation des données Insee

population_age <- read_excel(
  file.path(
    raw_dir,
    "TD_POP1_2023.xlsx"
    ),
  sheet = "COM",
  col_types = "text"
)

# Identification des communes
population_age <- population_age %>%
  rename(
    code_commune = `Code géographique`,
    commune = `Libellé géographique`
  )

glimpse(population_age)

# Vérification des identifiants communaux INSEE

stopifnot(
  !anyNA(population_age$code_commune),
  !anyDuplicated(population_age$code_commune),
  all(nchar(population_age$code_commune) == 5)
)

# Préparation des classes d'âge

# Colonnes contenant les effectifs par sexe et par âge
colonnes_age <- names(population_age) %>%
  str_subset("^(Homme|Femme)\\n")

# Construire la correspondance entre colonnes et âges
referentiel_age <- tibble(
  colonne = colonnes_age,
  age = as.integer(
    str_extract(colonnes_age, "\\d+(?= an)")
  )
)

# Conversion des effectifs
population_age <- population_age %>%
  mutate(
    across(all_of(colonnes_age), as.numeric)
  )

# Classes d'âge du Baromètre Santé publique France 2024
classes_age <- list(
  pop_18_29 = 18:29,
  pop_30_39 = 30:39,
  pop_40_49 = 40:49,
  pop_50_59 = 50:59,
  pop_60_69 = 60:69,
  pop_70_79 = 70:79
)

# Calcul de chaque classe
for (nom_classe in names(classes_age)) {
  
  colonnes <- referentiel_age %>%
    filter(age %in% classes_age[[nom_classe]]) %>%
    pull(colonne)
  
  stopifnot(
    length(colonnes) == 2 * length(classes_age[[nom_classe]])
  )
  
  population_age[[nom_classe]] <- rowSums(
    population_age[, colonnes],
    na.rm = FALSE
  )
}

# Calcul de la population communale des 18-79 ans

population_commune_age <- population_age %>%
  select(
    code_commune,
    commune,
    all_of(names(classes_age))
  ) %>%
  mutate(
    pop_18_79 = rowSums(
      pick(all_of(names(classes_age))),
      na.rm = FALSE
    )
  )

glimpse(population_commune_age)

summary(population_commune_age$pop_18_79)

# Référentiel communes-régions
referentiel <- read_csv(
  file.path(processed_dir, "territoires_communes.csv"),
  col_types = cols(
    code_commune = col_character(),
    code_region = col_character(),
    .default = col_guess()
  )
) %>%
  select(code_commune, code_region, region) %>%
  distinct()

# Corrections géographiques identifiées lors du contrôle
# Paris, Lyon, Marseille et communes absentes du référentiel FDep/F-EDI

corrections_geographiques <- tribble(
  ~code_commune, ~code_region, ~region,
  
  "75056", "11", "Île-de-France",
  "69123", "84", "Auvergne-Rhône-Alpes",
  "13055", "93", "Provence-Alpes-Côte d'Azur",
  
  "49126", "52", "Pays de la Loire",
  "69114", "84", "Auvergne-Rhône-Alpes",
  "14581", "28", "Normandie",
  "12218", "76", "Occitanie",
  "85212", "52", "Pays de la Loire",
  "85165", "52", "Pays de la Loire",
  "60694", "32", "Hauts-de-France",
  
  "15035", "84", "Auvergne-Rhône-Alpes",
  "15031", "84", "Auvergne-Rhône-Alpes",
  "15171", "84", "Auvergne-Rhône-Alpes",
  "15047", "84", "Auvergne-Rhône-Alpes",
  
  "55039", "44", "Grand Est",
  "55050", "44", "Grand Est",
  "55139", "44", "Grand Est",
  "55189", "44", "Grand Est",
  "55239", "44", "Grand Est",
  "55307", "44", "Grand Est"
)

# Vérifier que les corrections ne créent pas de doublons
stopifnot(
  !anyDuplicated(referentiel$code_commune),
  !anyDuplicated(corrections_geographiques$code_commune),
  !any(corrections_geographiques$code_commune %in% referentiel$code_commune)
)

# Compléter le référentiel
referentiel_complet <- bind_rows(
  referentiel,
  corrections_geographiques
)

# Communes encore sans correspondance
communes_non_appariees <- population_commune_age %>%
  anti_join(
    referentiel_complet,
    by = "code_commune"
  )

# Vérifier que seules les communes ultramarines restent

stopifnot(
  nrow(communes_non_appariees) == 112,
  
  all(
    str_detect(
      communes_non_appariees$code_commune,
      "^(97|98)"
    )
  )
)

print(
  communes_non_appariees %>%
    summarise(nb_communes_outre_mer = n())
)

# Jointure population / référentiel
population_region <- population_commune_age %>%
  inner_join(
    referentiel_complet,
    by = "code_commune"
  )

# Harmonisation des noms des régions
population_region <- population_region %>%
  mutate(
    region = case_when(
      region == "Auvergne et Rhône-Alpes" ~
        "Auvergne-Rhône-Alpes",
      
      region == "Bourgogne et Franche-Comté" ~
        "Bourgogne-Franche-Comté",
      
      region == "Nouvelle Aquitaine" ~
        "Nouvelle-Aquitaine",
      
      TRUE ~ region
    )
  )

# Agrégation régionale

demographie_regions <- population_region %>%
  group_by(code_region, region) %>%
  summarise(
    across(
      all_of(c(names(classes_age), "pop_18_79")),
      ~ sum(.x, na.rm = FALSE)
    ),
    .groups = "drop"
  ) %>%
  mutate(
    across(
      all_of(names(classes_age)),
      ~ 100 * .x / pop_18_79,
      .names = "part_{.col}"
    ),
    
    # Indicateur synthétique de vieillissement
    part_pop_60_79 =
      part_pop_60_69 + part_pop_70_79
  ) %>%
  arrange(region)

# Contrôles de qualité

# Vérification des communes
stopifnot(
  nrow(population_region) ==
    n_distinct(population_region$code_commune),
  
  !anyNA(population_region$code_region),
  !anyNA(population_region$region)
)

# Vérification des régions
stopifnot(
  nrow(demographie_regions) == 13,
  n_distinct(demographie_regions$code_region) == 13
)

# Conservation de la population
stopifnot(
  isTRUE(all.equal(
    sum(population_region$pop_18_79),
    sum(demographie_regions$pop_18_79)
  ))
)

# Vérification des proportions
colonnes_parts <- paste0(
  "part_",
  names(classes_age)
)

somme_parts <- rowSums(
  demographie_regions[, colonnes_parts]
)

stopifnot(
  all(abs(somme_parts - 100) < 1e-8)
)

# Résumé des contrôles
controle_final <- demographie_regions %>%
  summarise(
    nb_regions = n(),
    population_18_79 = sum(pop_18_79),
    nb_valeurs_manquantes = sum(is.na(across(everything())))
  )

print(controle_final)

# Contrôles finaux avant export

stopifnot(
  controle_final$nb_valeurs_manquantes == 0,
  
  all(demographie_regions$pop_18_79 > 0),
  
  all(
    demographie_regions$part_pop_60_79 >= 0 &
      demographie_regions$part_pop_60_79 <= 100
  )
)

message("Contrôles internes de démographie validés.")

# Export

write_csv(
  demographie_regions,
  file.path(
    processed_dir,
    "demographie_regions_2023.csv"
  )
)
