# Packages
library(tidyverse)

# Chemins
raw_dir <- "../data/raw"
processed_dir <- "../data/processed"

# Importation
ald <- read_delim(
  file.path(
    raw_dir,
    "patients-longueduree-annuelle.csv"
  ),
  delim = ";",
  col_types = cols(
    annee = col_integer(),
    region = col_character(),
    departement = col_character(),
    .default = col_guess()
  )
)

# Préparation régionale 2024
ald_regions <- ald %>%
  filter(
    annee == 2024,
    departement == "999",
    region %in% c(
      "11", "24", "27", "28", "32", "44", "52",
      "53", "75", "76", "84", "93", "94"
    )
  ) %>%
  transmute(
    code_region = region,
    region = if_else(
      libelle_region == "Ile-de-France",
      "Île-de-France",
      libelle_region
    ),
    ald_sans_medecin_traitant =
      as.numeric(taux_patients_ALD_sans_MT) * 100
  ) %>%
  arrange(code_region)

# Contrôles de qualité

codes_regions <- c(
  "11", "24", "27", "28", "32", "44", "52",
  "53", "75", "76", "84", "93", "94"
)

stopifnot(
  nrow(ald_regions) == 13,
  
  n_distinct(ald_regions$code_region) == 13,
  
  setequal(
    ald_regions$code_region,
    codes_regions
  ),
  
  !anyNA(ald_regions$region),
  
  !anyNA(ald_regions$ald_sans_medecin_traitant),
  
  all(
    is.finite(ald_regions$ald_sans_medecin_traitant)
  ),
  
  all(
    ald_regions$ald_sans_medecin_traitant >= 0 &
      ald_regions$ald_sans_medecin_traitant <= 100
  )
)

print(ald_regions, n = 13)

# Export
write_csv(
  ald_regions,
  file.path(
    processed_dir,
    "ald_regions_2024.csv"
  )
)
