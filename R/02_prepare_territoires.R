# 02_prepare_territoires.R
# Construction de la base communale des indicateurs territoriaux

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


# Importation des données


# FDep20

fdep <- read.csv(
  file.path(
    raw_dir,
    "indice-de-defavorisation-sociale-fdep-par-commune.csv"
  ),
  header = TRUE,
  sep = ","
) |>
  mutate(
    Code.commune = str_pad(
      as.character(Code.commune),
      width = 5,
      side = "left",
      pad = "0"
    )
  )


# Contrôle rapide
glimpse(fdep)


# F-EDI

fedi <- read.csv(
  file.path(
    raw_dir,
    "french-european-deprivation-index-f-edi-2021-par-commune.csv"
  ),
  header = TRUE,
  sep = ","
) |>
  mutate(
    Commune.Code = str_pad(
      as.character(Commune.Code),
      width = 5,
      side = "left",
      pad = "0"
    )
  )


# 3.3 APL médecins généralistes - 2023

apl <- read_excel(
  file.path(
    raw_dir,
    "apl.xlsx"
  ),
  sheet = "Data",
  skip = 4
) |>
  rename(
    code_commune = codgeo,
    commune = libgeo,
    annee = an,
    apl = apl_mg_hmep
  ) |>
  mutate(
    code_commune = str_pad(
      as.character(code_commune),
      width = 5,
      side = "left",
      pad = "0"
    ),
    commune = as.character(commune),
    annee = as.integer(annee),
    apl = as.numeric(apl)
  ) |>
  filter(
    annee == 2023,
    !is.na(apl)
  )


# Contrôle : une seule valeur APL par commune
controle_doublons_apl <- apl |>
  count(code_commune) |>
  filter(n > 1)

print(controle_doublons_apl)


# Population communale 2023

population_2023 <- read_delim(
  file.path(
    raw_dir,
    "donnees_communes.csv"
  ),
  delim = ";",
  col_types = cols(
    COM = col_character(),
    .default = col_guess()
  ),
  show_col_types = FALSE
) |>
  rename(
    code_commune = COM,
    commune = Commune,
    population_totale = PTOT
  ) |>
  mutate(
    code_commune = str_pad(
      code_commune,
      width = 5,
      side = "left",
      pad = "0"
    ),
    commune = as.character(commune),
    population_totale = as.numeric(population_totale)
  )


# Contrôle : une seule population par commune
controle_doublons_population <- population_2023 |>
  count(code_commune) |>
  filter(n > 1)

print(controle_doublons_population)


# Contrôle de la couverture FDep / F-EDI

fdep |>
  summarise(
    nb_communes_fdep = n_distinct(Code.commune)
  ) |>
  print()


fedi |>
  summarise(
    nb_communes_fedi = n_distinct(Commune.Code)
  ) |>
  print()


# Communes présentes dans FDep mais absentes de F-EDI
controle_absentes_fedi <- fdep |>
  anti_join(
    fedi,
    by = c("Code.commune" = "Commune.Code")
  ) |>
  summarise(
    nb_absentes_fedi = n_distinct(Code.commune)
  )

print(controle_absentes_fedi)


# Communes présentes dans F-EDI mais absentes de FDep
controle_absentes_fdep <- fedi |>
  anti_join(
    fdep,
    by = c("Commune.Code" = "Code.commune")
  ) |>
  summarise(
    nb_absentes_fdep = n_distinct(Commune.Code)
  )

print(controle_absentes_fdep)


# Jointure FDep20 + F-EDI

territoires <- fdep |>
  inner_join(
    fedi,
    by = c("Code.commune" = "Commune.Code")
  )


territoires |>
  summarise(
    nb_communes_apres_jointure = n_distinct(Code.commune)
  ) |>
  print()


# Sélection et harmonisation des variables

territoires <- territoires |>
  transmute(
    
    # Identifiant communal
    code_commune = Code.commune,
    
    # Commune
    commune = Commune,
    
    # Département
    code_departement = Département.Code,
    departement = Département.x,
    
    # Région
    code_region = Région.Code.x,
    region = Région.x,
    
    # Population disponible dans la source FDep
    population_fdep_2020 = as.numeric(
      Nombre.d.habitants.de.la.commune
    ),
    
    # FDep20
    # Malgré son intitulé, cette variable correspond
    # au score continu FDep20.
    fdep = as.numeric(
      Indice.de.défavorisation.en.quintiles
    ),
    
    # F-EDI
    fedi = as.numeric(EDI),
    
    # Informations complémentaires F-EDI
    quintile_fedi = Quintile.natonal,
    millesime_fedi = Millésime.EDI
  )

# Ajout indépendant de la population et de l'APL

territoires <- territoires |>
  left_join(
    population_2023 |>
      select(
        code_commune,
        population_totale
      ),
    by = "code_commune"
  ) |>
  left_join(
    apl |>
      select(
        code_commune,
        apl
      ),
    by = "code_commune"
  )



# Harmonisation de l'APL pour Paris, Lyon et Marseille


# L'APL 2023 est fournie au niveau de la commune-centre,
# tandis que FDep, F-EDI et la population distinguent les
# arrondissements municipaux.
#
# La valeur APL de la commune-centre est donc attribuée
# à chacun de ses arrondissements.

apl_paris <- apl |>
  filter(code_commune == "75056") |>
  pull(apl)

apl_lyon <- apl |>
  filter(code_commune == "69123") |>
  pull(apl)

apl_marseille <- apl |>
  filter(code_commune == "13055") |>
  pull(apl)


territoires <- territoires |>
  mutate(
    apl = case_when(
      str_detect(code_commune, "^751") ~ apl_paris,
      str_detect(code_commune, "^6938") ~ apl_lyon,
      str_detect(code_commune, "^132") ~ apl_marseille,
      TRUE ~ apl
    )
  )

# Contrôle des doublons après jointures

controle_doublons <- territoires |>
  summarise(
    nb_lignes = n(),
    nb_communes = n_distinct(code_commune)
  )

print(controle_doublons)


territoires |>
  count(code_commune) |>
  filter(n > 1) |>
  print()


# Contrôle des données manquantes après correction


controle_manquants_apres_correction <- territoires |>
  summarise(
    nb_communes = n_distinct(code_commune),
    
    nb_apl_manquante =
      sum(is.na(apl)),
    
    nb_population_manquante =
      sum(is.na(population_totale)),
    
    nb_fedi_manquante =
      sum(is.na(fedi)),
    
    nb_fdep_manquante =
      sum(is.na(fdep)),
    
    nb_region_manquante =
      sum(is.na(region)),
    
    nb_departement_manquant =
      sum(is.na(departement))
  )

print(controle_manquants_apres_correction)


# Identification des communes encore manquantes

territoires_manquants <- territoires |>
  filter(
    is.na(apl) |
      is.na(population_totale)
  ) |>
  select(
    code_commune,
    commune,
    departement,
    region,
    population_fdep_2020,
    apl,
    population_totale
  )


# Nombre de communes restantes
print(
  nrow(territoires_manquants)
)

# Les communes encore sans APL et sans population 2023 sont conservées
# dans la base. Elles représentent environ 0,12 % de la population
# couverte par FDep20 et seront exclues uniquement des agrégations
# nécessitant ces variables.


# Répartition par région
territoires_manquants |>
  count(
    region,
    sort = TRUE
  ) |>
  print()


# 12. Poids démographique des communes manquantes

controle_poids_manquants <- territoires |>
  summarise(
    population_fdep_2020_totale =
      sum(
        population_fdep_2020,
        na.rm = TRUE
      ),
    
    population_fdep_2020_manquants =
      sum(
        population_fdep_2020[
          is.na(apl) |
            is.na(population_totale)
        ],
        na.rm = TRUE
      )
  ) |>
  mutate(
    part_population_manquante =
      100 *
      population_fdep_2020_manquants /
      population_fdep_2020_totale
  )

print(controle_poids_manquants)


# Contrôle de la géographie

controle_geographie <- territoires |>
  summarise(
    nb_regions =
      n_distinct(region),
    
    nb_departements =
      n_distinct(departement)
  )

print(controle_geographie)

# 14. Statistiques descriptives

statistiques_territoires <- territoires |>
  summarise(
    
    apl_min =
      min(
        apl,
        na.rm = TRUE
      ),
    
    apl_q1 =
      quantile(
        apl,
        0.25,
        na.rm = TRUE
      ),
    
    apl_mediane =
      median(
        apl,
        na.rm = TRUE
      ),
    
    apl_moyenne =
      mean(
        apl,
        na.rm = TRUE
      ),
    
    apl_q3 =
      quantile(
        apl,
        0.75,
        na.rm = TRUE
      ),
    
    apl_max =
      max(
        apl,
        na.rm = TRUE
      ),
    
    population_2023_totale =
      sum(
        population_totale,
        na.rm = TRUE
      )
  )

print(statistiques_territoires)


# Export

write_csv(
  territoires,
  file.path(
    processed_dir,
    "territoires_communes.csv"
  )
)
