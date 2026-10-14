
# Packages
library(tidyverse)

# Chemins
raw_dir <- "../data/raw"
processed_dir <- "../data/processed"

# Codes des 13 régions métropolitaines
codes_regions <- c(
  "11", "24", "27", "28", "32", "44", "52",
  "53", "75", "76", "84", "93", "94"
)

# Importation des données
activite <- read_csv(
  file.path(
    raw_dir,
    "activite-physique-indicateurs-du-barometre-de-sante-publique-detail-region.csv"
  ),
  show_col_types = FALSE
)

sedentarite <- read_csv(
  file.path(
    raw_dir,
    "sedentarite-indicateurs-du-barometre-de-sante-publique-france-2024-detail-region.csv"
  ),
  show_col_types = FALSE
)

tabagisme <- read_csv(
  file.path(
    raw_dir,
    "tabagisme-indicateurs-du-barometre-de-sante-publique-france-2024-detail-region.csv"
  ),
  show_col_types = FALSE
)

# 1. Activité physique

activite_regions <- activite %>%
  filter(
    sexe == "Tous",
    `Classe d'âge` == "Tous",
    Indicateur %in% c(
      "Pratique d'activités physiques lors des loisirs : régulièrement",
      "Pratique d'activités physiques lors des loisirs : jamais"
    )
  ) %>%
  transmute(
    code_region = str_pad(
      as.character(`Région Code`),
      width = 2,
      pad = "0"
    ),
    indicateur = dplyr::recode(
      Indicateur,
      "Pratique d'activités physiques lors des loisirs : régulièrement" =
        "activite_reguliere",
      "Pratique d'activités physiques lors des loisirs : jamais" =
        "activite_jamais"
    ),
    estimation = as.numeric(Estimation)
  ) %>%
  filter(code_region %in% codes_regions)

# 2. Sédentarité

sedentarite_regions <- sedentarite %>%
  filter(
    Sexe == "Tous",
    is.na(`Classe d'âge`),
    Diplôme == "Tous",
    PCS == "Tous",
    `Situation financière perçue` == "Tous",
    Indicateur == "Sédentarité élevée"
  ) %>%
  transmute(
    code_region = str_pad(
      as.character(`Nouvelles régions`),
      width = 2,
      pad = "0"
    ),
    indicateur = "sedentarite_elevee",
    estimation = as.numeric(Estimation)
  ) %>%
  filter(code_region %in% codes_regions)

# 3. Tabagisme

tabagisme_regions <- tabagisme %>%
  filter(
    sexe == "Hommes et Femmes",
    `Classe d'âge` == "Tous",
    `Situation professionnelle` == "Tous",
    Diplôme == "Tous",
    PCS == "Tous",
    `Situation financière perçue` == "Tous",
    Indicateur == "Tabagisme quotidien"
  ) %>%
  transmute(
    code_region = str_pad(
      as.character(`Nouvelles régions`),
      width = 2,
      pad = "0"
    ),
    indicateur = "tabagisme_quotidien",
    estimation = as.numeric(Estimation)
  ) %>%
  filter(code_region %in% codes_regions)

# Contrôle des sélections avant consolidation

verifier_selection <- function(donnees, nb_indicateurs) {
  
  stopifnot(
    nrow(donnees) == 13 * nb_indicateurs,
    
    !anyDuplicated(
      donnees[c("code_region", "indicateur")]
    ),
    
    setequal(
      unique(donnees$code_region),
      codes_regions
    ),
    
    !anyNA(donnees$estimation),
    
    all(
      donnees$estimation >= 0 &
        donnees$estimation <= 100
    )
  )
}

verifier_selection(activite_regions, 2)
verifier_selection(sedentarite_regions, 1)
verifier_selection(tabagisme_regions, 1)

# 4. Consolidation des quatre indicateurs

comportements_regions <- bind_rows(
  activite_regions,
  sedentarite_regions,
  tabagisme_regions
) %>%
  pivot_wider(
    names_from = indicateur,
    values_from = estimation
  ) %>%
  arrange(code_region)

# 5. Contrôles de qualité

controle_comportements <- comportements_regions %>%
  summarise(
    nb_regions = n(),
    nb_codes_uniques = n_distinct(code_region),
    nb_valeurs_manquantes = sum(
      is.na(across(everything()))
    )
  )

print(controle_comportements)

stopifnot(
  controle_comportements$nb_regions == 13,
  controle_comportements$nb_codes_uniques == 13,
  controle_comportements$nb_valeurs_manquantes == 0
)

# Affichage des résultats
print(comportements_regions, n = 13)

# 6. Export

write_csv(
  comportements_regions,
  file.path(
    processed_dir,
    "comportements_regions_2024.csv"
  )
)
