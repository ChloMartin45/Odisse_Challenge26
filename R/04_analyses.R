# 04_analysis.R
# Analyse des relations entre inégalités, accessibilité et santé


# Packages


library(tidyverse)
library(FactoMineR)
library(sf)
library(giscoR)


# Chemins


processed_dir <- "../data/processed"

dir.create(
  processed_dir,
  recursive = TRUE,
  showWarnings = FALSE
)


# Importation des données


territoires <- read_csv(
  file.path(
    processed_dir,
    "territoires_regions.csv"
  ),
  show_col_types = FALSE
)

sante <- read_csv(
  file.path(
    processed_dir,
    "sante_regions.csv"
  ),
  show_col_types = FALSE
)

diabete <- read_csv(
  file.path(
    processed_dir,
    "diabete_regions.csv"
  ),
  show_col_types = FALSE
)


# Harmonisation des noms de régions


sante <- sante |>
  mutate(
    region = `Nouvelles régions`,
    
    region = recode(
      region,
      
      "Ile-de-France" =
        "Île-de-France",
      
      "Auvergne et Rhône-Alpes" =
        "Auvergne-Rhône-Alpes",
      
      "Bourgogne et Franche-Comté" =
        "Bourgogne-Franche-Comté",
      
      "Nouvelle Aquitaine" =
        "Nouvelle-Aquitaine"
    )
  )


diabete <- diabete |>
  mutate(
    region = `Nouvelles régions`,
    
    region = recode(
      region,
      
      "Ile-de-France" =
        "Île-de-France",
      
      "Auvergne et Rhône-Alpes" =
        "Auvergne-Rhône-Alpes",
      
      "Bourgogne et Franche-Comté" =
        "Bourgogne-Franche-Comté",
      
      "Nouvelle Aquitaine" =
        "Nouvelle-Aquitaine"
    )
  )



# Préparation des indicateurs sanitaires


# Santé générale


sante_analyse <- sante |>
  select(
    region,
    Indicateur,
    Estimation
  ) |>
  pivot_wider(
    names_from = Indicateur,
    values_from = Estimation
  ) |>
  rename(
    sante_percue =
      `Santé perçue bonne ou très bonne`,
    
    limitation_activite =
      `Limitation d'activité`
  )



# Diabète déclaré


diabete_analyse <- diabete |>
  select(
    region,
    Estimation
  ) |>
  rename(
    diabete_declare = Estimation
  )


# Construction de la base analytique régionale


analyse_regions <- territoires |>
  left_join(
    sante_analyse,
    by = "region"
  ) |>
  left_join(
    diabete_analyse,
    by = "region"
  ) |>
  select(
    code_region,
    region,
    population,
    
    fdep_pondere,
    fedi_pondere,
    apl_pondere,
    
    sante_percue,
    limitation_activite,
    diabete_declare
  )


# Contrôle de la base analytique


controle_analyse <- analyse_regions |>
  summarise(
    nb_regions = n(),
    
    nb_regions_uniques =
      n_distinct(region),
    
    nb_valeurs_manquantes =
      sum(
        is.na(fdep_pondere) |
          is.na(fedi_pondere) |
          is.na(apl_pondere) |
          is.na(sante_percue) |
          is.na(limitation_activite) |
          is.na(diabete_declare)
      )
  )

print(controle_analyse)


# Vérification des doublons
analyse_regions |>
  count(region) |>
  filter(n > 1) |>
  print()


# Affichage des 13 régions
analyse_regions |>
  arrange(region) |>
  print(n = 13)


# Sécurisation
stopifnot(
  nrow(analyse_regions) == 13,
  n_distinct(analyse_regions$region) == 13,
  sum(is.na(analyse_regions)) == 0
)


# Analyse des relations territoriales


# Analyses exploratoires sur 13 régions métropolitaines.
#
# Ces relations décrivent des associations territoriales.
# Elles ne permettent pas d'établir de relation causale.


# Fonction de corrélation


calcul_correlation <- function(x, y) {
  
  valide <-
    !is.na(x) &
    !is.na(y)
  
  test <- cor.test(
    x[valide],
    y[valide],
    method = "pearson"
  )
  
  tibble(
    correlation =
      unname(test$estimate),
    
    p_value =
      test$p.value
  )
}


# FDep20 et santé


correlations_fdep <- bind_rows(
  
  calcul_correlation(
    analyse_regions$fdep_pondere,
    analyse_regions$sante_percue
  ) |>
    mutate(
      indicateur =
        "Santé perçue bonne ou très bonne"
    ),
  
  calcul_correlation(
    analyse_regions$fdep_pondere,
    analyse_regions$limitation_activite
  ) |>
    mutate(
      indicateur =
        "Limitation d'activité"
    ),
  
  calcul_correlation(
    analyse_regions$fdep_pondere,
    analyse_regions$diabete_declare
  ) |>
    mutate(
      indicateur =
        "Diabète déclaré"
    )
) |>
  select(
    indicateur,
    correlation,
    p_value
  )

print(correlations_fdep)


# APL et santé


correlations_apl <- bind_rows(
  
  calcul_correlation(
    analyse_regions$apl_pondere,
    analyse_regions$sante_percue
  ) |>
    mutate(
      indicateur =
        "Santé perçue bonne ou très bonne"
    ),
  
  calcul_correlation(
    analyse_regions$apl_pondere,
    analyse_regions$limitation_activite
  ) |>
    mutate(
      indicateur =
        "Limitation d'activité"
    ),
  
  calcul_correlation(
    analyse_regions$apl_pondere,
    analyse_regions$diabete_declare
  ) |>
    mutate(
      indicateur =
        "Diabète déclaré"
    )
) |>
  select(
    indicateur,
    correlation,
    p_value
  )

print(correlations_apl)



# APL et santé après prise en compte du FDep


# L'objectif est d'examiner l'association entre l'APL
# et la santé une fois retirée leur relation linéaire
# avec le FDep20.


# Fonction d'analyse résiduelle


calcul_relation_residuelle <- function(
    donnees,
    variable_sante
) {
  
  formule_sante_fdep <- reformulate(
    "fdep_pondere",
    response = variable_sante
  )
  
  formule_complete <- reformulate(
    c(
      "fdep_pondere",
      "apl_pondere"
    ),
    response = variable_sante
  )
  
  
  modele_apl <- lm(
    apl_pondere ~ fdep_pondere,
    data = donnees
  )
  
  
  modele_sante <- lm(
    formule_sante_fdep,
    data = donnees
  )
  
  
  modele_complet <- lm(
    formule_complete,
    data = donnees
  )
  
  
  correlation_residuelle <- cor(
    resid(modele_apl),
    resid(modele_sante)
  )
  
  
  p_value_apl <- summary(
    modele_complet
  )$coefficients[
    "apl_pondere",
    "Pr(>|t|)"
  ]
  
  
  tibble(
    correlation_partielle_apl_fdep =
      correlation_residuelle,
    
    p_value_apl_apres_fdep =
      p_value_apl
  )
}



# Application aux trois indicateurs


correlations_residuelles <- bind_rows(
  
  calcul_relation_residuelle(
    analyse_regions,
    "sante_percue"
  ) |>
    mutate(
      indicateur =
        "Santé perçue bonne ou très bonne"
    ),
  
  calcul_relation_residuelle(
    analyse_regions,
    "limitation_activite"
  ) |>
    mutate(
      indicateur =
        "Limitation d'activité"
    ),
  
  calcul_relation_residuelle(
    analyse_regions,
    "diabete_declare"
  ) |>
    mutate(
      indicateur =
        "Diabète déclaré"
    )
) |>
  select(
    indicateur,
    correlation_partielle_apl_fdep,
    p_value_apl_apres_fdep
  )

print(correlations_residuelles)



# Table de synthèse des relations territoriales


relations_territoriales <- correlations_fdep |>
  
  rename(
    correlation_fdep =
      correlation,
    
    p_value_fdep =
      p_value
  ) |>
  
  left_join(
    correlations_apl |>
      rename(
        correlation_apl =
          correlation,
        
        p_value_apl =
          p_value
      ),
    by = "indicateur"
  ) |>
  
  left_join(
    correlations_residuelles,
    by = "indicateur"
  )


print(relations_territoriales)


# Standardisation des indicateurs


# Convention commune :
#
# valeur positive = situation relativement plus défavorable
# valeur négative = situation relativement plus favorable
#
# par rapport à la moyenne des 13 régions.


analyse_regions <- analyse_regions |>
  mutate(
    
    # Défavorisation élevée = défavorable
    z_fdep =
      as.numeric(
        scale(fdep_pondere)
      ),
    
    # F-EDI élevé = défavorable
    z_fedi =
      as.numeric(
        scale(fedi_pondere)
      ),
    
    # APL élevée = meilleure accessibilité
    # -> inversion
    z_apl =
      as.numeric(
        scale(-apl_pondere)
      ),
    
    # Santé perçue élevée = favorable
    # -> inversion
    z_sante =
      as.numeric(
        scale(-sante_percue)
      ),
    
    # Limitation élevée = défavorable
    z_limitation =
      as.numeric(
        scale(limitation_activite)
      ),
    
    # Diabète élevé = défavorable
    z_diabete =
      as.numeric(
        scale(diabete_declare)
      )
  )



# Contrôle de la standardisation


controle_standardisation <- analyse_regions |>
  summarise(
    across(
      c(
        z_fdep,
        z_fedi,
        z_apl,
        z_sante,
        z_limitation,
        z_diabete
      ),
      list(
        moyenne = mean,
        ecart_type = sd
      )
    )
  )

print(controle_standardisation)


# Préparation de la classification


classification <- analyse_regions |>
  select(
    region,
    z_fdep,
    z_fedi,
    z_apl,
    z_sante,
    z_limitation,
    z_diabete
  )


classification_hcpc <- classification |>
  column_to_rownames(
    "region"
  )


# Classification HCPC à quatre groupes


# La classification est exploratoire :
# seulement 13 régions sont étudiées.

hcpc_4 <- HCPC(
  classification_hcpc,
  nb.clust = 4,
  consol = TRUE,
  graph = FALSE
)



# Association des régions aux clusters

clusters_regions <- hcpc_4$data.clust |>
  as.data.frame() |>
  rownames_to_column(
    "region"
  ) |>
  select(
    region,
    clust
  ) |>
  mutate(
    clust =
      as.integer(
        as.character(clust)
      )
  ) |>
  as_tibble()


print(
  clusters_regions |>
    arrange(
      clust,
      region
    ),
  n = 13
)


# Taille des clusters

controle_taille_clusters <- clusters_regions |>
  count(
    clust,
    name = "nb_regions"
  ) |>
  arrange(clust)

print(controle_taille_clusters)


# Construction de la table régionale


carte_regions <- analyse_regions |>
  left_join(
    clusters_regions,
    by = "region"
  )



# Profil moyen des clusters


profils_clusters <- carte_regions |>
  group_by(
    clust
  ) |>
  summarise(
    nb_regions = n(),
    
    across(
      c(
        z_fdep,
        z_fedi,
        z_apl,
        z_sante,
        z_limitation,
        z_diabete
      ),
      mean
    ),
    
    .groups = "drop"
  ) |>
  arrange(clust)


print(
  profils_clusters,
  n = 4
)


# Composition des clusters


composition_clusters <- carte_regions |>
  select(
    region,
    clust
  ) |>
  arrange(
    clust,
    region
  )


print(
  composition_clusters,
  n = 13
)


# Tests de sensibilité de la classification


# Ces tests servent uniquement à vérifier la stabilité
# générale de la typologie.
#
# Ils ne servent pas à choisir a posteriori
# la classification donnant le résultat le plus favorable.


tester_hcpc <- function(
    donnees,
    variables,
    nb_clusters
) {
  
  base_test <- donnees |>
    select(
      region,
      all_of(variables)
    ) |>
    column_to_rownames(
      "region"
    )
  
  resultat <- HCPC(
    base_test,
    nb.clust = nb_clusters,
    consol = TRUE,
    graph = FALSE
  )
  
  resultat$data.clust |>
    as.data.frame() |>
    rownames_to_column(
      "region"
    ) |>
    transmute(
      region,
      
      clust =
        as.integer(
          as.character(clust)
        )
    ) |>
    as_tibble()
}


# Référence


classification_reference <- clusters_regions |>
  rename(
    cluster_reference = clust
  )


# Trois clusters


clusters_3 <- tester_hcpc(
  donnees = analyse_regions,
  
  variables = c(
    "z_fdep",
    "z_fedi",
    "z_apl",
    "z_sante",
    "z_limitation",
    "z_diabete"
  ),
  
  nb_clusters = 3
) |>
  rename(
    cluster_3_groupes = clust
  )


# Quatre clusters sans F-EDI

clusters_sans_fedi <- tester_hcpc(
  donnees = analyse_regions,
  
  variables = c(
    "z_fdep",
    "z_apl",
    "z_sante",
    "z_limitation",
    "z_diabete"
  ),
  
  nb_clusters = 4
) |>
  rename(
    cluster_sans_fedi = clust
  )


# Quatre clusters sans APL


clusters_sans_apl <- tester_hcpc(
  donnees = analyse_regions,
  
  variables = c(
    "z_fdep",
    "z_fedi",
    "z_sante",
    "z_limitation",
    "z_diabete"
  ),
  
  nb_clusters = 4
) |>
  rename(
    cluster_sans_apl = clust
  )


# Comparaison

comparaison_clusters <- classification_reference |>
  
  left_join(
    clusters_3,
    by = "region"
  ) |>
  
  left_join(
    clusters_sans_fedi,
    by = "region"
  ) |>
  
  left_join(
    clusters_sans_apl,
    by = "region"
  ) |>
  
  arrange(
    cluster_reference,
    region
  )


print(
  comparaison_clusters,
  n = 13
)


# Stabilité des paires de régions


calcul_stabilite_paires <- function(
    reference,
    alternative,
    nom_reference,
    nom_alternative
) {
  
  base <- reference |>
    select(
      region,
      cluster_ref = all_of(nom_reference)
    ) |>
    left_join(
      alternative |>
        select(
          region,
          cluster_alt = all_of(nom_alternative)
        ),
      by = "region"
    )
  
  paires <- expand_grid(
    region_1 = base$region,
    region_2 = base$region
  ) |>
    filter(
      region_1 < region_2
    ) |>
    
    left_join(
      base |>
        select(
          region_1 = region,
          cluster_ref_1 = cluster_ref,
          cluster_alt_1 = cluster_alt
        ),
      by = "region_1"
    ) |>
    
    left_join(
      base |>
        select(
          region_2 = region,
          cluster_ref_2 = cluster_ref,
          cluster_alt_2 = cluster_alt
        ),
      by = "region_2"
    ) |>
    
    mutate(
      ensemble_reference =
        cluster_ref_1 == cluster_ref_2,
      
      ensemble_alternative =
        cluster_alt_1 == cluster_alt_2,
      
      accord =
        ensemble_reference ==
        ensemble_alternative
    )
  
  tibble(
    taux_accord_paires =
      mean(
        paires$accord
      ) * 100
  )
}


stabilite_sans_fedi <- calcul_stabilite_paires(
  classification_reference,
  clusters_sans_fedi,
  "cluster_reference",
  "cluster_sans_fedi"
)


stabilite_sans_apl <- calcul_stabilite_paires(
  classification_reference,
  clusters_sans_apl,
  "cluster_reference",
  "cluster_sans_apl"
)


print(stabilite_sans_fedi)
print(stabilite_sans_apl)


# Noms définitifs des profils


# Les noms sont attribués après examen des valeurs moyennes
# standardisées de chacun des quatre groupes.

noms_clusters <- c(
  
  "1" =
    "Profil francilien atypique",
  
  "2" =
    "Profil sanitaire globalement favorable",
  
  "3" =
    "Profil territorial plus défavorisé et moins accessible",
  
  "4" =
    "Profil de santé plus fragile malgré une meilleure accessibilité"
)


carte_regions <- carte_regions |>
  mutate(
    profil =
      recode(
        as.character(clust),
        !!!noms_clusters
      )
  )


# Contrôle
carte_regions |>
  select(
    region,
    clust,
    profil
  ) |>
  arrange(
    clust,
    region
  ) |>
  print(n = 13)


# Table descriptive des profils


profils_clusters_final <- carte_regions |>
  group_by(
    clust,
    profil
  ) |>
  summarise(
    nb_regions = n(),
    
    z_fdep =
      mean(z_fdep),
    
    z_fedi =
      mean(z_fedi),
    
    z_apl =
      mean(z_apl),
    
    z_sante =
      mean(z_sante),
    
    z_limitation =
      mean(z_limitation),
    
    z_diabete =
      mean(z_diabete),
    
    .groups = "drop"
  ) |>
  arrange(clust)


print(
  profils_clusters_final,
  n = 4
)


# Préparation des données géographiques


# Géométrie NUTS 2

regions_sf <- gisco_get_nuts(
  year = "2024",
  nuts_level = 2,
  resolution = "20",
  country = "FR"
)


regions_france <- regions_sf |>
  filter(
    CNTR_CODE == "FR"
  )


# Correspondance avec les 13 régions


correspondance_regions <- tribble(
  ~NUTS_ID, ~region,
  
  "FR10", "Île-de-France",
  
  "FRB0", "Centre-Val de Loire",
  
  "FRC1", "Bourgogne-Franche-Comté",
  "FRC2", "Bourgogne-Franche-Comté",
  
  "FRD1", "Normandie",
  "FRD2", "Normandie",
  
  "FRE1", "Hauts-de-France",
  "FRE2", "Hauts-de-France",
  
  "FRF1", "Grand Est",
  "FRF2", "Grand Est",
  "FRF3", "Grand Est",
  
  "FRG0", "Pays de la Loire",
  
  "FRH0", "Bretagne",
  
  "FRI1", "Nouvelle-Aquitaine",
  "FRI2", "Nouvelle-Aquitaine",
  "FRI3", "Nouvelle-Aquitaine",
  
  "FRJ1", "Occitanie",
  "FRJ2", "Occitanie",
  
  "FRK1", "Auvergne-Rhône-Alpes",
  "FRK2", "Auvergne-Rhône-Alpes",
  
  "FRL0", "Provence-Alpes-Côte d'Azur",
  
  "FRM0", "Corse"
)


# Reconstruction des 13 régions

regions_13_sf <- regions_france |>
  inner_join(
    correspondance_regions,
    by = "NUTS_ID"
  ) |>
  group_by(
    region
  ) |>
  summarise(
    geometry =
      st_union(geometry),
    
    .groups = "drop"
  )


# Contrôle
stopifnot(
  nrow(regions_13_sf) == 13
)


# Association des profils

carte_hcpc <- regions_13_sf |>
  left_join(
    carte_regions |>
      select(
        region,
        clust,
        profil
      ),
    by = "region"
  )


# Contrôle
stopifnot(
  sum(is.na(carte_hcpc$clust)) == 0,
  sum(is.na(carte_hcpc$profil)) == 0
)


# Contours départementaux


departements_sf <- gisco_get_nuts(
  year = "2024",
  nuts_level = 3,
  resolution = "20",
  country = "FR"
)


departements_france <- departements_sf |>
  filter(
    CNTR_CODE == "FR"
  )


# Préparation des exports


carte_hcpc_data <- carte_regions |>
  select(
    code_region,
    region,
    population,
    
    clust,
    profil,
    
    fdep_pondere,
    fedi_pondere,
    apl_pondere,
    
    sante_percue,
    limitation_activite,
    diabete_declare,
    
    z_fdep,
    z_fedi,
    z_apl,
    z_sante,
    z_limitation,
    z_diabete
  )


# Contrôles finaux

controle_final <- tibble(
  
  nb_regions_analyse =
    nrow(analyse_regions),
  
  nb_regions_hcpc =
    nrow(carte_hcpc_data),
  
  nb_profils =
    n_distinct(
      carte_hcpc_data$clust
    ),
  
  nb_valeurs_manquantes =
    sum(
      is.na(carte_hcpc_data)
    )
)


print(controle_final)


stopifnot(
  controle_final$nb_regions_analyse == 13,
  controle_final$nb_regions_hcpc == 13,
  controle_final$nb_profils == 4,
  controle_final$nb_valeurs_manquantes == 0
)


# 26. Exports pour l'application Dash


# Relations territoriales


write_csv(
  relations_territoriales,
  file.path(
    processed_dir,
    "relations_territoriales.csv"
  )
)


# Base analytique régionale


write_csv(
  analyse_regions,
  file.path(
    processed_dir,
    "analyse_regions.csv"
  )
)


# Profils territoriaux


write_csv(
  carte_hcpc_data,
  file.path(
    processed_dir,
    "carte_regions_hcpc.csv"
  )
)


# Résumé moyen des profils


write_csv(
  profils_clusters_final,
  file.path(
    processed_dir,
    "profils_clusters.csv"
  )
)


# Carte régionale


st_write(
  carte_hcpc,
  file.path(
    processed_dir,
    "regions_hcpc.geojson"
  ),
  delete_dsn = TRUE,
  quiet = TRUE
)


# Contours départementaux


st_write(
  departements_france,
  file.path(
    processed_dir,
    "departements.geojson"
  ),
  delete_dsn = TRUE,
  quiet = TRUE
)
