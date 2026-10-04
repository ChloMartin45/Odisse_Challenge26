# 03_prepare_region.R
# Agrégation des indicateurs territoriaux à l'échelle régionale


# Packages

library(tidyverse)


# Chemins


processed_dir <- "../data/processed"

dir.create(
  processed_dir,
  recursive = TRUE,
  showWarnings = FALSE
)


# Importation de la base communale


territoires <- read_csv(
  file.path(
    processed_dir,
    "territoires_communes.csv"
  ),
  show_col_types = FALSE
)


# Contrôle de la structure


glimpse(territoires)

territoires |>
  summarise(
    nb_lignes = n(),
    nb_communes = n_distinct(code_commune),
    nb_regions = n_distinct(region)
  ) |>
  print()


# Préparation des variables

territoires <- territoires |>
  mutate(
    population_totale = as.numeric(population_totale),
    apl = as.numeric(apl),
    fdep = as.numeric(fdep),
    fedi = as.numeric(fedi),
    
    # Harmonisation des noms de régions
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


# Fonction de moyenne pondérée


# Seules les communes disposant simultanément de l'indicateur
# et de la population 2023 sont utilisées dans le calcul.

moyenne_ponderee <- function(indicateur, population) {
  
  valide <-
    !is.na(indicateur) &
    !is.na(population)
  
  if (sum(valide) == 0) {
    return(NA_real_)
  }
  
  sum(
    indicateur[valide] *
      population[valide]
  ) /
    sum(
      population[valide]
    )
}


# Agrégation régionale


territoires_regions <- territoires |>
  group_by(
    code_region,
    region
  ) |>
  summarise(
    
    # Nombre de communes
    nb_communes =
      n_distinct(code_commune),
    
    # Population 2023 disponible
    population =
      sum(
        population_totale,
        na.rm = TRUE
      ),
    
    # FDep20 pondéré par la population
    fdep_pondere =
      moyenne_ponderee(
        fdep,
        population_totale
      ),
    
    # F-EDI pondéré par la population
    fedi_pondere =
      moyenne_ponderee(
        fedi,
        population_totale
      ),
    
    # APL pondéré par la population
    apl_pondere =
      moyenne_ponderee(
        apl,
        population_totale
      ),
    
    # Contrôles
    nb_apl_manquante =
      sum(is.na(apl)),
    
    nb_population_manquante =
      sum(is.na(population_totale)),
    
    nb_fdep_manquant =
      sum(is.na(fdep)),
    
    nb_fedi_manquant =
      sum(is.na(fedi)),
    
    .groups = "drop"
  )


# Contrôle du résultat régional


print(territoires_regions)


# Contrôle global


controle_regions <- territoires_regions |>
  summarise(
    nb_regions = n(),
    
    population_totale =
      sum(
        population,
        na.rm = TRUE
      ),
    
    apl_manquant =
      sum(
        is.na(apl_pondere)
      ),
    
    fdep_manquant =
      sum(
        is.na(fdep_pondere)
      ),
    
    fedi_manquant =
      sum(
        is.na(fedi_pondere)
      )
  )

print(controle_regions)


# Contrôle des régions

territoires_regions |>
  select(
    code_region,
    region,
    nb_communes,
    population
  ) |>
  arrange(region) |>
  print(n = 13)


# Contrôle des indicateurs


controle_indicateurs <- territoires_regions |>
  summarise(
    fdep_min =
      min(
        fdep_pondere,
        na.rm = TRUE
      ),
    
    fdep_max =
      max(
        fdep_pondere,
        na.rm = TRUE
      ),
    
    fedi_min =
      min(
        fedi_pondere,
        na.rm = TRUE
      ),
    
    fedi_max =
      max(
        fedi_pondere,
        na.rm = TRUE
      ),
    
    apl_min =
      min(
        apl_pondere,
        na.rm = TRUE
      ),
    
    apl_max =
      max(
        apl_pondere,
        na.rm = TRUE
      )
  )

print(controle_indicateurs)


# Vérification indépendante de l'APL régional

controle_apl <- territoires |>
  filter(
    !is.na(apl),
    !is.na(population_totale)
  ) |>
  group_by(region) |>
  summarise(
    apl_moyenne_simple =
      mean(apl),
    
    apl_moyenne_ponderee =
      weighted.mean(
        apl,
        population_totale
      ),
    
    .groups = "drop"
  ) |>
  arrange(region)

print(controle_apl, n = 13)


# Export


write_csv(
  territoires_regions,
  file.path(
    processed_dir,
    "territoires_regions.csv"
  )
)
