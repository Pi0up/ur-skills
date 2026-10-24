# Instructions et règles du projet (AGENTS.md)

Ce fichier consigne les règles et instructions régissant le comportement des assistants et agents IA intervenant sur le projet **ur-skills**.

---

## 1. Mémorisation des consignes comportementales (Méta-règle)
- **Persistance automatique** : Dès que l'utilisateur précise ou ajuste une consigne sur la façon d'opérer (règles de code, style de réponse, méthodologie, conventions, contraintes), cette consigne doit être immédiatement consignée ou mise à jour dans ce fichier (`AGENTS.md`).
- **Confirmation** : Informer brièvement l'utilisateur de l'enregistrement de la nouvelle consigne dans les instructions du projet.

---

## 2. Modèle opératoire Humain–IA (Socle UR Spécification v0.5/v0.6)
- **L'humain décide, l'outil opère** : L'IA propose ; seul un humain approuve et valide.
- **Traçabilité stricte** :
  - Tout atome créé ou modifié par l'agent IA porte obligatoirement `authored_by: ai` (ou `mixed`) et le statut initial `status: to_review`.
  - Seul un humain peut renseigner `reviewed_by` (identifiant Git de l'évaluateur) et promouvoir un atome vers `status: approved`. L'IA ne promeut jamais elle-même le statut ou le niveau d'un atome.
- **Neutralité vis-à-vis des exceptions** : L'IA ne peut jamais être mentionnée dans `requested_by` ni dans `confirmed_by` pour une exception ou dérogation à une règle.
- **Vérification mécanique du verbatim** : Pour toute preuve textuelle (`EVD`), l'extrait cité doit correspondre mot à mot, caractère par caractère, au texte de la source (`SRC`) à l'emplacement (`locator`) désigné.
- **Anonymisation par défaut** : Aucun motif de données personnelles directement identifiantes (nom de famille, email, numéro de téléphone, adresse) ne doit entrer dans le dépôt. Les participants sont identifiés par un pseudonyme `PAR-YYYY-NNN`.
- **L'observé n'est pas le conçu** : Les designs, flux conçus ou prototypes ne sont jamais des preuves et n'entrent jamais comme `JRN` tant que leur usage réel n'a pas été observé ou testé sur le terrain.

---

## 3. Conventions de nommage et de langue
- **Structure en anglais** :
  - Tous les noms de dossiers (`schema/`, `templates/`, `skills/`, `ur_tools/`, `views/`, `indexes/`, etc.).
  - Tous les identifiants techniques (`PRJ-YYYY-NNN`, `EVD-YYYY-NNN`, nœuds `n-NNN`, clés de frontmatter, types, statuts, relations typées, vocabulaires contrôlés, messages techniques de script).
  - Noms de fichiers d'atomes : format strict `ID-slug.md` en minuscules avec tirets (ex. `INS-2026-014-technicians-skip-alerts.md`).
- **Contenu des livrables dans la langue de l'utilisateur** :
  - Le contenu textuel des atomes (titre, résumé, sections obligatoires) est rédigé dans la langue employée par l'utilisateur (ex. français si la demande est en français), avec le champ `language: fr` (ou code ISO 639-1 approprié).
  - Les étiquettes et badges restitués aux utilisateurs dans les vues sont traduits selon `schema/labels.<lang>.yaml`.

---

## 4. Gestion des commits et exécution des tests
- **Commits fréquents et granulaires** : Commiter les modifications par petits groupes logiques d'actions avec le format conventionnel : `type(scope): description` (types autorisés : `feat`, `fix`, `docs`, `refactor`, `schema`, `chore`).
- **Déclenchement des tests** : Ne pas lancer la suite de tests systématiquement après chaque petite modification. Les tests ne doivent être exécutés que dans les cas suivants :
  1. À la demande explicite de l'utilisateur.
  2. À l'achèvement complet d'une nouvelle feature ou skill.
  3. Avant de pousser (`git push`) du code vers le dépôt distant.

---

## 5. Règles méthodologiques pour l'extraction des preuves (Evidence)
- **Pas de verbatim sans constat, pas de constat sans croisement** : Un verbatim unitaire isolé est trop petit pour constituer une evidence autonome. Une evidence doit obligatoirement porter un constat explicite étayé par un faisceau de citations/faits concordants issus de la même session/source (au moins 2 éléments probants croisés).
- **Seuil de rejet des opinions nues** : Aucune déclaration d'opinion vague ou subjective sans lien direct avec un fait observable, un comportement ou un obstacle concret ne doit être retenue comme evidence.
- **Dates partielles documentées** : Les dates incomplètes documentées dans la source sont renseignées au format ISO 8601 partiel (`YYYY-MM` ou `YYYY`). La valeur `collected_at: null` est strictement interdite.
- **Rattachement obligatoire à un projet** : Le champ `projects` doit obligatoirement contenir au moins un identifiant de projet valide (`[PRJ-YYYY-NNN]`).
- **Sections obligatoires dès le profil starter** : Tout atome d'evidence doit obligatoirement comporter son `## Résumé` (2 à 4 phrases), son `## Constat & Limites`, ses `## Preuves` (verbatims croisés) et son `## Contexte de recueil`.
- **Rattachement d'étude obligatoire** : Tout atome d'evidence doit être rattaché à son étude parente via `from_study` pour éviter la prolifération d'atomes orphelins.
