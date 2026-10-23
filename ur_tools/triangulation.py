"""Triangulation and Confidence Calculation Engine.
Implements Section 6 (validation level), Section 10 (triangulation) and Section 11 (ordinal confidence).
"""

from __future__ import annotations

from typing import Any, Dict, List, Set


def compute_confidence_band(
    provenance: str,
    evidence_items: List[Dict[str, Any]],
    has_unresolved_contradictions: bool = False,
) -> tuple[str, str, str]:
    """Compute ordinal confidence band for an Insight or Recommendation.
    Returns: (band_id, badge, label_fr)
    Bands: low (●○○), medium (●●○), high (●●●), very_high (●●●).
    """
    if provenance == "rule":
        return ("very_high", "●●●", "Très élevée (Règle formelle)")

    if not evidence_items:
        return ("low", "●○○", "Faible (Aucune preuve directe)")

    # Group evidence by independent sessions
    sessions: Set[str] = set()
    families: Set[str] = set()
    axes: Set[str] = set()
    has_inferred_only = True

    for evd in evidence_items:
        prov = evd.get("provenance", "inferred")
        if prov != "inferred":
            has_inferred_only = False
        sid = evd.get("session_id")
        if sid:
            sessions.add(sid)
        else:
            sessions.add(evd.get("id", "unknown"))

        fam = evd.get("method_family")
        if fam:
            families.add(fam)
        axis = evd.get("method_axis")
        if axis:
            axes.add(axis)

    distinct_sessions = len(sessions)
    distinct_families = len(families)
    distinct_axes = len(axes)

    if has_inferred_only or distinct_sessions <= 1:
        return ("low", "●○○", "Faible (Preuve unique ou support inféré)")

    # High: at least 3 independent evidence from 2 families or axes, no unresolved contradiction
    if distinct_sessions >= 3 and (distinct_families >= 2 or distinct_axes >= 2) and not has_unresolved_contradictions:
        return ("high", "●●●", "Élevée (Triangulée sans contradiction)")

    # Medium: at least 2 independent evidence from one family or axis, or converging with contradiction
    if distinct_sessions >= 2:
        return ("medium", "●●○", "Moyenne (Corroborée sur 1 famille/axe ou tension ouverte)")

    return ("low", "●○○", "Faible")


def compute_validation_level(
    provenance: str,
    linked_participants: List[str],
    linked_sessions: List[str],
    has_quant_confirmation: bool = False,
) -> tuple[str, str, str]:
    """Compute validation level for a Job or Persona (Section 6).
    Returns: (level_id, badge, label_fr)
    """
    distinct_participants = len(set(linked_participants))
    distinct_sessions = len(set(linked_sessions))

    # Observed condition: observed qualitatively in >= 3 distinct participants, across >= 2 sessions
    is_observed = distinct_participants >= 3 and distinct_sessions >= 2

    if is_observed and has_quant_confirmation:
        return ("quant_validated", "●●●", "Corroboré")
    elif is_observed:
        return ("observed", "●●○", "Observé")
    elif provenance in ("declared", "documented") or distinct_participants >= 1:
        return ("sensed", "●○○", "Indice")
    else:
        return ("hypothesis", "●○○", "Indice (Hypothèse)")
