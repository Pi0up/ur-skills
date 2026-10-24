---
id: EVD-YYYY-NNN
type: evidence
title: "[Constat factuel synthétique de l'observation ou de la déclaration]"
language: fr
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
projects: [PRJ-YYYY-NNN]        # Obligatoire, au moins un projet rattaché
provenance: declared            # declared (propos participant) | observed (chercheur) | documented (source tierce)
authored_by: ai
reviewed_by: null
sensitive: false
source: SRC-YYYY-NNN            # Identifiant de la source nettoyée
locator: "p. 1, § 2"            # Repère précis de localisation
session_id: "SESS-01"           # Session d'entretien, de test ou vague de recueil
collected_at: YYYY-MM-DD        # Date complète (YYYY-MM-DD) ou partielle documentée (YYYY-MM, YYYY). Interdit: null
context: null                   # Dimensions de contexte ou null ("contexte non spécifié")
aliases: []
tags: []

# Bloc quantitatif optionnel (applicable si données métriques/sondages)
quant:
  sample_size: null             # n : effectif analysé
  population: null              # N : population totale ciblée
  metric: null                  # Indicateur mesuré
  value: null                   # Valeur ou taux constaté

links:
  from_study: STU-YYYY-NNN      # Étude parente obligatoire
  concerns: PAR-YYYY-NNN        # Participant concerné (ou null si étude quantitative anonymisée)
  illustrates: null             # Optionnel : nœud de parcours illustré (ex. JRN-2026-001#n-002)
---

## Résumé
[Résumé de deux à quatre phrases formulant le constat d'observation ou l'enseignement empirique, son intensité et ce qu'il révèle de l'expérience vécue.]

## Constat & Limites
- **Constat** : [Ce que l'observation ou le retour démontre concrètement. Pas de verbatim sans constat, pas de constat sans croisement de faits probants.]
- **Représentativité & Limites** : [Tendance générale vs avis isolé, taille de l'échantillon associé, limites méthodologiques.]

## Preuves (Verbatims ou Mesures)
> "[Première citation textuelle exacte mot à mot, vérifiable mécaniquement dans la source SRC]" (locator)

> "[Seconde citation ou élément probant concordant croisé confirmant le constat]" (locator)

## Contexte de recueil
- **Moment / Déclencheur** : [À quel moment de la session, de l'interaction ou du protocole ce retour intervient.]
- **Question ou Tâche posée** : [Tâche demandée, question ouverte posée ou déclencheur comportemental.]
