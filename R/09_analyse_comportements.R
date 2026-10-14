# Packages
library(tidyverse)

# Chemins
processed_dir <- "../data/processed"

# Importation
comportements_regions <- read_csv(
  file.path(
    processed_dir,
    "comportements_regions_2024.csv"
  ),
  col_types = cols(
    code_region = col_character(),
    .default = col_guess()
  )
)

# Matrice de corrélation
correlations_comportements <- comportements_regions %>%
  select(-code_region) %>%
  cor(method = "pearson")

print(round(correlations_comportements, 3))

# Rapprochement avec les indicateurs territoriaux existants

analyse_regions <- read_csv(
  file.path(processed_dir, "analyse_regions.csv"),
  col_types = cols(
    code_region = col_character(),
    .default = col_guess()
  )
)

analyse_comportements <- analyse_regions %>%
  left_join(
    comportements_regions,
    by = "code_region",
    relationship = "one-to-one"
  )

# Contrôles de la jointure

stopifnot(
  nrow(analyse_comportements) == 13,
  
  n_distinct(analyse_comportements$code_region) == 13,
  
  setequal(
    analyse_comportements$code_region,
    c(
      "11", "24", "27", "28", "32", "44", "52",
      "53", "75", "76", "84", "93", "94"
    )
  ),
  
  !anyNA(
    analyse_comportements[
      c(
        "activite_reguliere",
        "activite_jamais",
        "sedentarite_elevee",
        "tabagisme_quotidien"
      )
    ]
  )
)

# Corrélations entre comportements et indicateurs existants

variables_existantes <- c(
  "fdep_pondere",
  "fedi_pondere",
  "apl_pondere",
  "diabete_declare",
  "limitation_activite",
  "sante_percue"
)

variables_comportements <- c(
  "activite_reguliere",
  "sedentarite_elevee",
  "tabagisme_quotidien"
)

matrice_correlations <- cor(
  analyse_comportements[
    c(variables_existantes, variables_comportements)
  ],
  method = "pearson"
)

# Afficher uniquement les relations qui nous intéressent

print(round(
  matrice_correlations[
    variables_comportements,
    variables_existantes
  ],
  3
))
