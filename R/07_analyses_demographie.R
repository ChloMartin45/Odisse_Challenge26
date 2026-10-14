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

demographie_regions <- read_csv(
  file.path(processed_dir, "demographie_regions_2023.csv"),
  col_types = cols(
    code_region = col_character(),
    .default = col_guess()
  )
)

# Fusion des indicateurs
analyse_regions_v2 <- analyse_regions %>%
  left_join(
    demographie_regions %>%
      select(
        code_region,
        pop_18_79,
        starts_with("part_pop_")
      ),
    by = "code_region",
    relationship = "one-to-one"
  )

# Contrôle
controle_v2 <- analyse_regions_v2 %>%
  summarise(
    nb_regions = n(),
    nb_regions_uniques = n_distinct(code_region),
    nb_parts_manquantes = sum(is.na(part_pop_60_79))
  )

print(controle_v2)

stopifnot(
  controle_v2$nb_regions == 13,
  controle_v2$nb_regions_uniques == 13,
  controle_v2$nb_parts_manquantes == 0
)

# Analyse exploratoire :
# la structure par âge sert à contextualiser les écarts
# de santé entre régions.
# Les associations observées ne sont pas causales.
# Les indicateurs régionaux de santé ne sont pas
# standardisés sur l'âge.

# Comparaison démographie et santé
comparaison_age_sante <- analyse_regions_v2 %>%
  select(
    region,
    part_pop_60_79,
    diabete_declare,
    limitation_activite,
    sante_percue,
    fdep_pondere
  ) %>%
  arrange(desc(part_pop_60_79))

print(comparaison_age_sante, n = 13)


# Répartition régionale par classe d'âge

demographie_graphique <- demographie_regions %>%
  select(
    region,
    part_pop_60_79,
    part_pop_18_29,
    part_pop_30_39,
    part_pop_40_49,
    part_pop_50_59,
    part_pop_60_69,
    part_pop_70_79
  ) %>%
  pivot_longer(
    cols = matches("^part_pop_\\d{2}_\\d{2}$"),
    names_to = "classe_age",
    values_to = "proportion"
  ) %>%
  mutate(
    classe_age = factor(
      classe_age,
      levels = c(
        "part_pop_18_29",
        "part_pop_30_39",
        "part_pop_40_49",
        "part_pop_50_59",
        "part_pop_60_69",
        "part_pop_70_79"
      ),
      labels = c(
        "18–29 ans",
        "30–39 ans",
        "40–49 ans",
        "50–59 ans",
        "60–69 ans",
        "70–79 ans"
      )
    ),
    
    region = fct_reorder(
      region,
      part_pop_60_79
    )
  )

# Graphique

ggplot(
  demographie_graphique,
  aes(
    x = region,
    y = proportion,
    fill = classe_age
  )
) +
  geom_col(width = 0.75) +
  coord_flip() +
  scale_fill_viridis_d(
    option = "C",
    direction = -1
  ) +
  guides(
    fill = guide_legend(nrow = 1)
  ) +
  labs(
    title = "Des structures démographiques contrastées",
    subtitle = "Répartition des 18–79 ans par classe d'âge, en 2023",
    x = NULL,
    y = "Part de la population des 18–79 ans (%)",
    fill = "Classe d'âge",
    caption = "Source : Insee, recensement de la population 2023"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    legend.position = "bottom",
    panel.grid.major.y = element_blank()
  )


# Variabilité des classes d'âge entre régions

variabilite_age <- demographie_regions %>%
  select(starts_with("part_pop_"), -part_pop_60_79) %>%
  pivot_longer(
    cols = everything(),
    names_to = "classe_age",
    values_to = "proportion"
  ) %>%
  group_by(classe_age) %>%
  summarise(
    moyenne = mean(proportion),
    minimum = min(proportion),
    maximum = max(proportion),
    ecart_type = sd(proportion),
    amplitude = maximum - minimum,
    .groups = "drop"
  ) %>%
  arrange(desc(ecart_type))

print(variabilite_age)

# Relations entre les principaux indicateurs démographiques

correlations_demographie <- demographie_regions %>%
  select(
    part_pop_18_29,
    part_pop_70_79,
    part_pop_60_79
  ) %>%
  cor(method = "pearson")

round(correlations_demographie, 3)


