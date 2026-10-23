# ur-skills — User Research Knowledge Repository Skills

[![Socle UR Spec](https://img.shields.io/badge/spec-v0.5.0-blue)](docs/spec/socle-ur-spec-v0.5.md)
[![Python](https://img.shields.io/badge/python-3.9+-green.svg)](pyproject.toml)

Suite de skills compagnons et moteur de validation pour bases de connaissances de recherche utilisateur (User Research), conforme à la spécification normative **`socle-ur-spec v0.5`**.

---

## 🎯 Philosophie & Principes directeurs

1. **Le Markdown est la source de vérité** : Graphes, indexes et vues sont dérivés et recalculables.
2. **L'observé n'est pas le conçu** : Les designs ou userflows sont des hypothèses ; ils n'entrent comme parcours (`JRN`) qu'une fois leur usage réel observé sur le terrain.
3. **Le calculé n'est jamais saisi** : Niveaux de validation, scores, badges de confiance et tables de couverture sont calculés par script.
4. **L'humain décide, l'outil opère** : L'IA propose (`authored_by: ai`, `status: to_review`) ; seul un humain approuve (`reviewed_by`).
5. **Anonymisation stricte** : Zéro donnée personnelle directement identifiante (PII).

---

## 📦 Les 7 Skills Compagnons

Alignés sur le modèle opérationnel et les **5 gestes du chercheur** (Section 20 de la spec) :

| Skill | Geste / Rôle | Mission |
| :--- | :--- | :--- |
| **`ur-orchestrator`** | Orchestrateur | Pilote le cycle de vie, les profils (`starter`, `standard`, `strict`) et le rituel hebdomadaire du *steward*. |
| **`ur-capture`** | **Geste 1 : Capture** | Ingestion de notes et transcriptions, extraction des sources (`SRC`), pseudonymisation (`PAR`) et preuves atomiques (`EVD`). |
| **`ur-check`** | **Geste 2 : Check** | Linter normatif des 29 règles, audit des liens rompus et vérification mécanique mot à mot du verbatim. |
| **`ur-link`** | **Geste 3 : Link** | Relations typées, calcul de triangulation, bandes de confiance et arbitrage des contradictions via le contexte. |
| **`ur-approve`** | **Geste 4 : Approve** | Évaluation de la *Definition of Done* (3 questions), traçabilité de révision et double validation d'exceptions. |
| **`ur-ask`** | **Geste 5 : Ask** | Interrogation de la base, réponses étayées avec badges de confiance (●○○, ●●○, ●●●) et exploration de la *gap map*. |
| **`ur-journey`** | Parcours & Couches | Modélisation d'arbres de parcours observés (`JRN`, nœuds `n-NNN`), gestion des couches et export Mermaid. |

---

## 🛠️ Outillage CLI (`ur_tools`)

Le package Python `ur_tools` fournit la boîte à outils exécutable par les skills ou en ligne de commande :

```bash
# Initialiser l'arborescence normative
ur-tools init

# Allouer le prochain identifiant séquentiel sans collision
ur-tools allocate-id --prefix INS --title "Les techniciens ignorent les alertes"

# Valider la base contre les 29 règles
ur-tools validate
ur-tools validate --profile strict

# Vérifier mécaniquement une preuve contre son texte source
ur-tools check-verbatim --evidence knowledge/evidence/EVD-2026-001.md

# Générer les 5 vues obligatoires (gap-map, to-review, what-changed, etc.)
ur-tools generate-views
```

---

## 📂 Structure du Répertoire

```
/sources/              # SRC- sources nettoyées + pointeurs d'originaux
/knowledge/
  projects/            # PRJ- contexte projet
  studies/             # STU- études et questions de recherche
  insights/            # INS- constats étayés par des preuves
  evidence/            # EVD- verbatims et observations concrètes
  participants/        # PAR- participants pseudonymisés
  methods/             # MET- référentiel des méthodes employées
  jobs/                # JOB- rôles, activités et contextes
  personas/            # PER- archétypes comportementaux
  journeys/            # JRN- parcours observés arborescents mono-fichiers
  recommendations/     # REC- recommandations fondées sur des règles ou déduites
  decisions/           # DEC- décisions d'équipe tracées
  glossary/            # GLO- définitions des concepts et modèles
/guides/               # GDE- guides d'application par approche méthodologique
/templates/            # Gabarits de démarrage (proto-templates et atomes)
/schema/               # Schémas, profils, vocabulaires et dimensions
/views/                # Vues obligatoires générées pour les humains
/skills/               # Définitions des 7 companion skills
/ur_tools/             # Moteur de validation et scripts CLI
```

---

## 📜 Licence
GNU General Public License v3.0 (GPLv3) — Vincent Perrier-perrery
