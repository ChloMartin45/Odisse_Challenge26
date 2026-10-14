# Packages
library(tidyverse)

# Chemins
processed_dir <- "../data/processed"

# Fonction d'importation : codes régionaux en texte
lire_regions <- function(fichier) {
  read_csv(
    file.path(processed_dir, fichier),
    col_types = cols(
      code_region = col_character(),
      .default = col_guess()
    )
  )
}

# Importation
analyse_regions <- lire_regions("analyse_regions.csv")

demographie <- lire_regions("demographie_regions_2023.csv")

comportements <- lire_regions("comportements_regions_2024.csv")

ald <- lire_regions("ald_regions_2024.csv")

# Consolidation
analyse_regions_v2 <- analyse_regions %>%
  left_join(
    demographie %>%
      select(
        code_region,
        pop_18_79,
        starts_with("part_pop_")
      ),
    by = "code_region",
    relationship = "one-to-one"
  ) %>%
  left_join(
    comportements,
    by = "code_region",
    relationship = "one-to-one"
  ) %>%
  left_join(
    ald %>%
      select(code_region, ald_sans_medecin_traitant),
    by = "code_region",
    relationship = "one-to-one"
  )

# Vérifier l'absence de colonnes dupliquées après jointure
stopifnot(
  !anyDuplicated(names(analyse_regions_v2)),
  !any(grepl("\\.[xy]$", names(analyse_regions_v2)))
)

# Contrôles
stopifnot(
  nrow(analyse_regions_v2) == 13,
  n_distinct(analyse_regions_v2$code_region) == 13,
  !anyNA(analyse_regions_v2$code_region)
)

# Vérifier les indicateurs ajoutés
nouvelles_variables <- c(
  "part_pop_60_79",
  "activite_reguliere",
  "activite_jamais",
  "sedentarite_elevee",
  "tabagisme_quotidien",
  "ald_sans_medecin_traitant"
)

controle_v2 <- analyse_regions_v2 %>%
  summarise(
    nb_regions = n(),
    nb_valeurs_manquantes = sum(
      is.na(across(all_of(nouvelles_variables)))
    )
  )

print(controle_v2)

stopifnot(controle_v2$nb_valeurs_manquantes == 0)

# Contrôle de la base analytique complète

variables_numeriques <- analyse_regions_v2 %>%
  select(where(is.numeric))

stopifnot(
  all(is.finite(as.matrix(variables_numeriques))),
  
  setequal(
    analyse_regions_v2$code_region,
    c(
      "11", "24", "27", "28", "32", "44", "52",
      "53", "75", "76", "84", "93", "94"
    )
  )
)

# Vérification de la structure démographique

variables_age <- c(
  "part_pop_18_29",
  "part_pop_30_39",
  "part_pop_40_49",
  "part_pop_50_59",
  "part_pop_60_69",
  "part_pop_70_79"
)

stopifnot(
  all(
    abs(
      rowSums(analyse_regions_v2[, variables_age]) - 100
    ) < 1e-8
  )
)

# Export
write_csv(
  analyse_regions_v2,
  file.path(processed_dir, "analyse_regions_v2.csv")
)
