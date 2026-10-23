---
id: JRN-YYYY-NNN
type: journey
title: "[Titre du parcours observé]"
language: fr
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
projects: [PRJ-YYYY-NNN]
provenance: observed
authored_by: ai
reviewed_by: null
scale: journey
sensitive: false
aliases: []
tags: []
links:
  serves: [JOB-YYYY-NNN]
  part_of: []
---

## Résumé
[Résumé de deux à quatre phrases décrivant le parcours utilisateur observé, son point de départ et son issue.]

## Périmètre (Scope)
[Périmètre fonctionnel, temporel ou organisationnel du parcours.]

## Objectif utilisateur
[Ce que l'utilisateur cherche à accomplir à travers ce parcours.]

## Arbre des nœuds

### n-001 · Début du parcours
- kind: step
- parent: root
- actor: utilisateur
- state: initial
- applies_to: [JOB-YYYY-NNN]

### n-002 · Étape d'action observée
- kind: action
- parent: n-001
- actor: utilisateur
- state: en cours
- applies_to: [JOB-YYYY-NNN]

## Couche émotionnelle (Emotional)
- node: n-002
  state: "Incertitude quant à la validation de la saisie"
  provenance: inferred

## Couche des frictions (Friction)
- node: n-002
  level: "Moyen"
  description: "Manque de confirmation visuelle immédiate"
  provenance: inferred

## Couche des outils (Tools)
- node: n-002
  tools: ["Application mobile", "Bloc-notes papier"]
  provenance: inferred

## Couche des canaux (Channels)
- node: n-002
  channel: "Application smartphone"
  provenance: inferred
