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

focus_diabete_age_sexe <- diabete_age_sexe |>
  mutate(
    classe_age = factor(
      `Classe d'âge`,
      levels = ordre_age
    ),
    
    ordre_age = match(
      as.character(`Classe d'âge`),
      ordre_age
    ),
    
    Sexe = factor(
      Sexe,
      levels = c(
        "Tous",
        "Femmes",
        "Hommes"
      )
    )
  ) |>
  arrange(
    ordre_age,
    Sexe
  ) |>
  select(
    sexe = Sexe,
    classe_age,
    ordre_age,
    estimation = Estimation,
    ic_inf,
    ic_sup,
    effectif_brut = Effectif.Brut
  )

print(
  focus_diabete_age_sexe,
  n = 18
)

controle_focus_age_sexe <- focus_diabete_age_sexe |>
  summarise(
    nb_observations = n(),
    nb_sexes = n_distinct(sexe),
    nb_classes_age = n_distinct(classe_age),
    nb_estimations_manquantes =
      sum(is.na(estimation))
  )

print(controle_focus_age_sexe)

# Calcul de l'écart hommes-femmes

ecart_diabete_sexe_age <- focus_diabete_age_sexe |>
  filter(
    sexe %in% c(
      "Hommes",
      "Femmes"
    )
  ) |>
  mutate(
    sexe = as.character(sexe),
    classe_age = as.character(classe_age)
  ) |>
  select(
    sexe,
    classe_age,
    estimation
  ) |>
  pivot_wider(
    names_from = sexe,
    values_from = estimation
  ) |>
  mutate(
    ordre_age = match(
      classe_age,
      ordre_age
    ),
    
    ecart_hommes_femmes =
      Hommes - Femmes
  ) |>
  arrange(
    ordre_age
  )

print(
  ecart_diabete_sexe_age,
  n = 6
)

# 2. Bonus territorial

# Modèle exploratoire FDep -> diabète

modele_fdep_diabete <- lm(
  diabete_declare ~ fdep_pondere,
  data = analyse_regions
)

# Résidus régionaux

diabete_residus_regions <- analyse_regions |>
  mutate(
    diabete_attendu =
      predict(
        modele_fdep_diabete
      ),
    
    residu_diabete =
      diabete_declare - diabete_attendu,
    
    position = case_when(
      residu_diabete > 0 ~
        "Au-dessus de la tendance",
      
      residu_diabete < 0 ~
        "En dessous de la tendance",
      
      TRUE ~
        "Proche de la tendance"
    ),
    
    importance_ecart =
      abs(residu_diabete)
  ) |>
  select(
    region,
    fdep_pondere,
    diabete_declare,
    diabete_attendu,
    residu_diabete,
    importance_ecart,
    position
  ) |>
  arrange(
    residu_diabete
  )

print(
  diabete_residus_regions,
  n = 13
)

# ============================================================
# Statistiques du modèle
# ============================================================

resume_modele_fdep <- summary(
  modele_fdep_diabete
)

stats_modele_fdep <- tibble(
  pente = coef(modele_fdep_diabete)[["fdep_pondere"]],
  constante = coef(modele_fdep_diabete)[["(Intercept)"]],
  r2 = resume_modele_fdep$r.squared,
  r2_ajuste = resume_modele_fdep$adj.r.squared,
  p_value_fdep = resume_modele_fdep$coefficients[
    "fdep_pondere",
    "Pr(>|t|)"
  ]
)

print(
  stats_modele_fdep
)

# ============================================================
# Test de sensibilité du modèle
# ============================================================

modele_sans_idf_bretagne <- lm(
  diabete_declare ~ fdep_pondere,
  data = analyse_regions |>
    filter(
      !region %in% c(
        "Île-de-France",
        "Bretagne"
      )
    )
)

resume_sans_idf_bretagne <- summary(
  modele_sans_idf_bretagne
)

sensibilite_modele <- tibble(
  scenario = c(
    "Toutes les régions",
    "Sans Île-de-France et Bretagne"
  ),
  
  pente = c(
    coef(modele_fdep_diabete)[["fdep_pondere"]],
    coef(modele_sans_idf_bretagne)[["fdep_pondere"]]
  ),
  
  r2 = c(
    resume_modele_fdep$r.squared,
    resume_sans_idf_bretagne$r.squared
  ),
  
  p_value = c(
    resume_modele_fdep$coefficients[
      "fdep_pondere",
      "Pr(>|t|)"
    ],
    resume_sans_idf_bretagne$coefficients[
      "fdep_pondere",
      "Pr(>|t|)"
    ]
  )
)

print(
  sensibilite_modele
)


# 5. Exports pour Dash

write_csv(
  focus_diabete_age_sexe,
  file.path(
    processed_dir,
    "focus_diabete_age_sexe.csv"
  )
)

write_csv(
  ecart_diabete_sexe_age,
  file.path(
    processed_dir,
    "focus_diabete_ecart_sexe_age.csv"
  )
)

write_csv(
  diabete_residus_regions,
  file.path(
    processed_dir,
    "focus_diabete_residus_regions.csv"
  )
)

write_csv(
  stats_modele_fdep,
  file.path(
    processed_dir,
    "focus_diabete_modele_fdep.csv"
  )
)




