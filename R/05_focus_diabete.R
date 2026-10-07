# 05_focus_diabete.R
# Analyse complémentaire du diabète déclaré

# Packages

library(tidyverse)


# Chemins

processed_dir <- "../data/processed"

dir.create(
  processed_dir,
  recursive = TRUE,
  showWarnings = FALSE
)


# Importation des données préparées

diabete_age_sexe <- read_csv(
  file.path(
    processed_dir,
    "diabete_age_sexe.csv"
  ),
  show_col_types = FALSE
)

indicateurs_finance <- read_csv(
  file.path(
    processed_dir,
    "indicateurs_finance.csv"
  ),
  show_col_types = FALSE
)

indicateurs_diplome <- read_csv(
  file.path(
    processed_dir,
    "indicateurs_diplome.csv"
  ),
  show_col_types = FALSE
)

indicateurs_pcs <- read_csv(
  file.path(
    processed_dir,
    "indicateurs_pcs.csv"
  ),
  show_col_types = FALSE
)

synthese_sociale <- read_csv(
  file.path(
    processed_dir,
    "synthese_sociale.csv"
  ),
  show_col_types = FALSE
)

analyse_regions <- read_csv(
  file.path(
    processed_dir,
    "analyse_regions.csv"
  ),
  show_col_types = FALSE
)

# 1. Préparation âge x sexe

# Préparation des classes d'âge

ordre_age <- c(
  "18-29 ans",
  "30-39 ans",
  "40-49 ans",
  "50-59 ans",
  "60-69 ans",
  "70-79 ans"
)


diabete_age_sexe <- diabete_age_sexe |>
  mutate(
    classe_age = factor(
      `Classe d'âge`,
      levels = ordre_age
    )
  ) |>
  arrange(
    classe_age,
    Sexe
  )

print(
  diabete_age_sexe,
  n = Inf
)

# 2. Extraction des dimensions sociales du diabète

# Situation financière

diabete_finance <- indicateurs_finance |>
  filter(
    Indicateur == "Diabète déclaré"
  ) |>
  transmute(
    dimension = "finance",
    dimension_label = "Situation financière",
    groupe = situation_financiere,
    Estimation,
    ic_inf,
    ic_sup,
    Effectif.Brut
  )


# Niveau de diplôme

diabete_diplome <- indicateurs_diplome |>
  filter(
    Indicateur == "Diabète déclaré"
  ) |>
  transmute(
    dimension = "diplome",
    dimension_label = "Niveau de diplôme",
    groupe = Diplôme,
    Estimation,
    ic_inf,
    ic_sup,
    Effectif.Brut
  )


# Catégorie socioprofessionnelle

diabete_pcs <- indicateurs_pcs |>
  filter(
    Indicateur == "Diabète déclaré"
  ) |>
  transmute(
    dimension = "pcs",
    dimension_label = "Catégorie socioprofessionnelle",
    groupe = PCS,
    Estimation,
    ic_inf,
    ic_sup,
    Effectif.Brut
  )

diabete_social <- bind_rows(
  diabete_finance,
  diabete_diplome,
  diabete_pcs
)

# 3. Réutilisation de la synthèse

diabete_ecarts_sociaux <- synthese_sociale |>
  filter(
    indicateur == "Diabète déclaré"
  ) |>
  arrange(
    desc(abs(ecart))
  )

print(
  diabete_ecarts_sociaux
)

# 4. Bonus territorial

# Modèle exploratoire FDep -> diabète

modele_fdep_diabete <- lm(
  diabete_declare ~ fdep_pondere,
  data = analyse_regions
)


# Valeurs attendues et résidus

diabete_residus_regions <- analyse_regions |>
  mutate(
    diabete_attendu =
      predict(
        modele_fdep_diabete
      ),
    
    residu_diabete =
      resid(
        modele_fdep_diabete
      )
  ) |>
  select(
    region,
    fdep_pondere,
    diabete_declare,
    diabete_attendu,
    residu_diabete
  ) |>
  arrange(
    desc(residu_diabete)
  )

print(
  diabete_residus_regions,
  n = 13
)

# 5. Exports pour Dash

write_csv(
  diabete_age_sexe,
  file.path(
    processed_dir,
    "focus_diabete_age_sexe.csv"
  )
)

write_csv(
  diabete_social,
  file.path(
    processed_dir,
    "focus_diabete_social.csv"
  )
)

write_csv(
  diabete_ecarts_sociaux,
  file.path(
    processed_dir,
    "focus_diabete_ecarts_sociaux.csv"
  )
)

write_csv(
  diabete_residus_regions,
  file.path(
    processed_dir,
    "focus_diabete_residus_regions.csv"
  )
)





