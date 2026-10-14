# Packages
library(tidyverse)

# Chemins
processed_dir <- "../data/processed"

# Importation des données
analyse_regions <- read_csv(
  file.path(processed_dir, "analyse_regions.csv"),
  col_types = cols(
    code_region = col_character(),
    .default = col_guess()
  )
)

ald_regions <- read_csv(
  file.path(processed_dir, "ald_regions_2024.csv"),
  col_types = cols(
    code_region = col_character(),
    .default = col_guess()
  )
)

# Jointure
analyse_acces <- analyse_regions %>%
  left_join(
    ald_regions %>%
      select(code_region, ald_sans_medecin_traitant),
    by = "code_region",
    relationship = "one-to-one"
  )

# Contrôles de la jointure

codes_regions <- c(
  "11", "24", "27", "28", "32", "44", "52",
  "53", "75", "76", "84", "93", "94"
)

stopifnot(
  nrow(analyse_acces) == 13,
  
  n_distinct(analyse_acces$code_region) == 13,
  
  setequal(
    analyse_acces$code_region,
    codes_regions
  ),
  
  !anyNA(analyse_acces$ald_sans_medecin_traitant)
)

# Corrélation entre ALD sans médecin traitant
# et les indicateurs territoriaux existants
variables_analyse <- c(
  "ald_sans_medecin_traitant",
  "apl_pondere",
  "fdep_pondere",
  "fedi_pondere",
  "diabete_declare",
  "limitation_activite",
  "sante_percue"
)

matrice_acces <- cor(
  analyse_acces[, variables_analyse],
  method = "pearson"
)

# Corrélations avec l'absence de médecin traitant en ALD

print(
  round(
    matrice_acces["ald_sans_medecin_traitant", ],
    3
  )
)
