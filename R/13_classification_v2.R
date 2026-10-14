# Packages
library(tidyverse)

# Chemins
processed_dir <- "../data/processed"

# Importation
analyse_regions_v2 <- read_csv(
  file.path(processed_dir, "analyse_regions_v2.csv"),
  col_types = cols(
    code_region = col_character(),
    .default = col_guess()
  )
)

# Indicateurs candidats à la classification
variables_candidates <- c(
  "part_pop_60_79",
  "fdep_pondere",
  "fedi_pondere",
  "diabete_declare",
  "limitation_activite",
  "sante_percue",
  "activite_reguliere",
  "sedentarite_elevee",
  "tabagisme_quotidien",
  "apl_pondere",
  "ald_sans_medecin_traitant"
)

# Contrôle des variables
stopifnot(
  nrow(analyse_regions_v2) == 13,
  !anyNA(analyse_regions_v2[, variables_candidates])
)

# Matrice de corrélation
matrice_v2 <- analyse_regions_v2 %>%
  select(all_of(variables_candidates)) %>%
  cor(method = "pearson")

round(matrice_v2, 2)

# Scénario de référence :
# variables actives de la V1 historique,
# recalculées avec la méthode commune aux scénarios V2.
# Ne remplace pas la classification V1 déployée.

variables_v1 <- c(
  "fdep_pondere",
  "fedi_pondere",
  "apl_pondere",
  "diabete_declare",
  "limitation_activite",
  "sante_percue"
)

# Scénario V2A : cinq dimensions territoriales
variables_v2a <- c(
  "fdep_pondere",
  "part_pop_60_79",
  "diabete_declare",
  "activite_reguliere",
  "tabagisme_quotidien",
  "apl_pondere"
)

# Scénario V2B : sédentarité à la place du tabagisme
variables_v2b <- c(
  "fdep_pondere",
  "part_pop_60_79",
  "diabete_declare",
  "activite_reguliere",
  "sedentarite_elevee",
  "apl_pondere"
)

# Contrôle des variables
stopifnot(
  all(variables_v1 %in% names(analyse_regions_v2)),
  all(variables_v2a %in% names(analyse_regions_v2)),
  all(variables_v2b %in% names(analyse_regions_v2))
)

# Packages
library(FactoMineR)
library(tidyverse)

# Fonction de classification
calculer_hcpc <- function(donnees, variables) {
  
  # Tableau contenant uniquement les variables actives
  donnees_acp <- donnees %>%
    select(all_of(variables))
  
  # Noms des régions comme identifiants
  donnees_acp <- as.data.frame(donnees_acp)
  rownames(donnees_acp) <- donnees$region
  
  # ACP sur variables standardisées
  acp <- PCA(
    donnees_acp,
    scale.unit = TRUE,
    ncp = min(
      ncol(donnees_acp),
      nrow(donnees_acp) - 1
    ),
    graph = FALSE
  )
  
  set.seed(2026)
  # Classification hiérarchique
  hcpc <- HCPC(
    acp,
    nb.clust = 4,
    consol = TRUE,
    graph = FALSE
  )
  
  # Récupération des groupes avec les noms des régions
  clusters_resultats <- hcpc$data.clust %>%
    as.data.frame() %>%
    tibble::rownames_to_column("region") %>%
    transmute(
      region,
      cluster = as.character(clust)
    )
  
  # Association sécurisée aux codes régionaux
  resultats <- donnees %>%
    select(code_region, region) %>%
    left_join(
      clusters_resultats,
      by = "region",
      relationship = "one-to-one"
    )
  
  stopifnot(
    nrow(resultats) == nrow(donnees),
    !anyNA(resultats$cluster)
  )
  
  return(resultats)

}

# Classification des trois scénarios
clusters_v1 <- calculer_hcpc(
  analyse_regions_v2,
  variables_v1
)

clusters_v2a <- calculer_hcpc(
  analyse_regions_v2,
  variables_v2a
)

clusters_v2b <- calculer_hcpc(
  analyse_regions_v2,
  variables_v2b
)

# Comparaison des classifications

comparaison_clusters <- clusters_v1 %>%
  rename(cluster_v1 = cluster) %>%
  left_join(
    clusters_v2a %>%
      select(code_region, cluster) %>%
      rename(cluster_v2a = cluster),
    by = "code_region"
  ) %>%
  left_join(
    clusters_v2b %>%
      select(code_region, cluster) %>%
      rename(cluster_v2b = cluster),
    by = "code_region"
  ) %>%
  arrange(region)

print(comparaison_clusters, n = 13)

# Taille des groupes par scénario

taille_clusters <- comparaison_clusters %>%
  pivot_longer(
    cols = starts_with("cluster_"),
    names_to = "scenario",
    values_to = "cluster"
  ) %>%
  count(scenario, cluster)

print(taille_clusters, n = Inf)

# Caractérisation des groupes V2A et V2B

caracteriser_clusters <- function(clusters, donnees, variables) {
  
  donnees %>%
    left_join(
      clusters %>%
        select(code_region, cluster),
      by = "code_region",
      relationship = "one-to-one"
    ) %>%
    group_by(cluster) %>%
    summarise(
      nb_regions = n(),
      across(
        all_of(variables),
        ~ mean(.x, na.rm = TRUE)
      ),
      .groups = "drop"
    ) %>%
    arrange(cluster)
}

# Profils V2A
profils_v2a <- caracteriser_clusters(
  clusters_v2a,
  analyse_regions_v2,
  variables_v2a
)

# Profils V2B
profils_v2b <- caracteriser_clusters(
  clusters_v2b,
  analyse_regions_v2,
  variables_v2b
)

print(profils_v2a, width = Inf)
print(profils_v2b, width = Inf)

# Caractérisation complémentaire des profils V2A
# avec des variables illustratives

variables_illustratives <- c(
  "fedi_pondere",
  "limitation_activite",
  "sante_percue",
  "sedentarite_elevee",
  "ald_sans_medecin_traitant"
)

profils_illustratifs_v2a <- analyse_regions_v2 %>%
  left_join(
    clusters_v2a %>%
      select(code_region, cluster),
    by = "code_region",
    relationship = "one-to-one"
  ) %>%
  group_by(cluster) %>%
  summarise(
    nb_regions = n(),
    across(
      all_of(variables_illustratives),
      ~ mean(.x, na.rm = TRUE)
    ),
    .groups = "drop"
  ) %>%
  arrange(cluster)

print(profils_illustratifs_v2a, width = Inf)

# Évaluation des classifications par silhouette

library(cluster)

calculer_silhouette <- function(donnees, variables, clusters) {
  
  # Standardisation des variables actives
  donnees_std <- scale(
    donnees %>%
      select(all_of(variables))
  )
  
  # Distance euclidienne
  distances <- dist(donnees_std)
  
  # Alignement des groupes sur les codes régionaux
  groupes <- clusters$cluster[
    match(donnees$code_region, clusters$code_region)
  ]
  
  stopifnot(!anyNA(groupes))
  
  # Calcul de la silhouette
  sil <- silhouette(
    as.integer(factor(groupes)),
    distances
  )
  
  tibble(
    silhouette_moyenne = mean(sil[, "sil_width"]),
    silhouette_min = min(sil[, "sil_width"]),
    nb_silhouettes_negatives = sum(sil[, "sil_width"] < 0)
  )
}

# Comparaison des scénarios
evaluation_clusters <- bind_rows(
  V1 = calculer_silhouette(
    analyse_regions_v2, variables_v1, clusters_v1
  ),
  V2A = calculer_silhouette(
    analyse_regions_v2, variables_v2a, clusters_v2a
  ),
  V2B = calculer_silhouette(
    analyse_regions_v2, variables_v2b, clusters_v2b
  ),
  .id = "scenario"
)

print(evaluation_clusters)

# Sensibilité au nombre de groupes - scénario V2B

evaluer_nombre_clusters <- function(k) {
  
  donnees_acp <- analyse_regions_v2 %>%
    select(all_of(variables_v2b)) %>%
    as.data.frame()
  
  rownames(donnees_acp) <- analyse_regions_v2$region
  
  acp <- PCA(
    donnees_acp,
    scale.unit = TRUE,
    ncp = min(
      ncol(donnees_acp),
      nrow(donnees_acp) - 1
    ),
    graph = FALSE
  )
  
  set.seed(2026)
  hcpc <- HCPC(
    acp,
    nb.clust = k,
    consol = TRUE,
    graph = FALSE
  )
  
  # Alignement des groupes
  groupes <- as.character(hcpc$data.clust$clust)
  
  noms_regions <- rownames(hcpc$data.clust)
  
  groupes <- groupes[
    match(analyse_regions_v2$region, noms_regions)
  ]
  
  stopifnot(!anyNA(groupes))
  
  # Silhouette
  distances <- dist(scale(donnees_acp))
  
  sil <- cluster::silhouette(
    as.integer(factor(groupes)),
    distances
  )
  
  tibble(
    nb_clusters = k,
    silhouette_moyenne = mean(sil[, "sil_width"]),
    nb_groupes_isoles = sum(table(groupes) == 1),
    nb_silhouettes_negatives =
      sum(sil[, "sil_width"] < 0)
  )
}

# Comparaison de 3, 4 et 5 groupes
comparaison_k <- purrr::map_dfr(
  3:5,
  evaluer_nombre_clusters
)

print(comparaison_k)

# Caractérisation complémentaire de la V2B

variables_illustratives_v2b <- c(
  "fedi_pondere",
  "limitation_activite",
  "sante_percue",
  "tabagisme_quotidien",
  "ald_sans_medecin_traitant"
)

profils_illustratifs_v2b <- analyse_regions_v2 %>%
  left_join(
    clusters_v2b %>%
      select(code_region, cluster),
    by = "code_region",
    relationship = "one-to-one"
  ) %>%
  group_by(cluster) %>%
  summarise(
    nb_regions = n(),
    across(
      all_of(variables_illustratives_v2b),
      ~ mean(.x, na.rm = TRUE)
    ),
    .groups = "drop"
  ) %>%
  arrange(cluster)

print(profils_illustratifs_v2b, width = Inf)

# Export des groupes régionaux V2B

# 1. Vérification de la composition des groupes
# Les noms des profils correspondent aux groupes
# identifiés et interprétés lors de l'analyse.

groupes_attendus <- list(
  "1" = c("11"),
  "2" = c("84", "53", "75", "76", "52", "93"),
  "3" = c("27", "24", "94", "28"),
  "4" = c("44", "32")
)

for (groupe in names(groupes_attendus)) {
  
  stopifnot(
    setequal(
      clusters_v2b$code_region[
        clusters_v2b$cluster == groupe
      ],
      groupes_attendus[[groupe]]
    )
  )
}

# 2. Attribution des intitulés aux groupes validés

carte_regions_v2 <- clusters_v2b %>%
  rename(
    cluster_v2 = cluster
  ) %>%
  mutate(
    profil = case_when(
      cluster_v2 == "1" ~
        "Métropole jeune et fortement sédentaire",
      
      cluster_v2 == "2" ~
        "Activité physique élevée et santé relativement favorable",
      
      cluster_v2 == "3" ~
        "Vieillissement et diabète plus fréquent",
      
      cluster_v2 == "4" ~
        "Défavorisation sociale et difficultés sanitaires"
    )
  ) %>%
  arrange(code_region)

# 3. Contrôles de qualité

stopifnot(
  nrow(carte_regions_v2) == 13,
  n_distinct(carte_regions_v2$code_region) == 13,
  !anyNA(carte_regions_v2$profil)
)

# 4. Affichage des résultats

print(carte_regions_v2, n = 13)

# 5. Export

write_csv(
  carte_regions_v2,
  file.path(
    processed_dir,
    "carte_regions_v2.csv"
  )
)

message("Classification V2B exportée avec succès.")
