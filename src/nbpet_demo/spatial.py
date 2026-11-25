"""Small reference scorer for synthetic examples, with no external dependencies."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from math import isfinite
from typing import Sequence


@dataclass(frozen=True)
class SpatialScore:
    n_grid: int
    budget: int
    n_selected: int
    n_reference: int
    n_overlap: int
    selected_fraction: float
    hit: int | None
    region_recall: float | None


def _selection_budget(n_grid: int, top_fraction: float) -> int:
    try:
        ratio = Decimal(str(top_fraction))
    except InvalidOperation as exc:
        raise ValueError("top_fraction must be a number in (0, 1]") from exc
    if not ratio.is_finite() or not 0 < ratio <= 1:
        raise ValueError("top_fraction must be a number in (0, 1]")
    return int(Decimal(n_grid) * ratio)


def _validate(scores: Sequence[float], reference: Sequence[bool]) -> None:
    if not scores or len(scores) != len(reference):
        raise ValueError("scores and reference must describe the same non-empty grid")


def _summarize(
    selected: Sequence[int], reference: Sequence[bool], budget: int
) -> SpatialScore:
    n_reference = sum(bool(value) for value in reference)
    n_overlap = sum(bool(reference[index]) for index in selected)
    return SpatialScore(
        n_grid=len(reference),
        budget=budget,
        n_selected=len(selected),
        n_reference=n_reference,
        n_overlap=n_overlap,
        selected_fraction=len(selected) / len(reference),
        hit=int(n_overlap > 0) if n_reference else None,
        region_recall=n_overlap / n_reference if n_reference else None,
    )


def score_top_positive(
    scores: Sequence[float], reference: Sequence[bool], *, top_fraction: float = 0.02
) -> SpatialScore:
    """Score at most floor(top_fraction * N) finite, strictly positive responses.

    The toy example uses ascending flattened index to resolve equal scores.
    This makes the example deterministic but does not reproduce the paper's
    seeded tie-breaking policy. Empty references yield no Hit/Recall.
    """
    _validate(scores, reference)
    budget = _selection_budget(len(scores), top_fraction)
    candidates = [
        index for index, value in enumerate(scores) if isfinite(value) and value > 0
    ]
    candidates.sort(key=lambda index: (-scores[index], index))
    return _summarize(candidates[:budget], reference, budget)


def legacy_threshold_demo(
    scores: Sequence[float], reference: Sequence[bool], *, top_fraction: float = 0.02
) -> tuple[float, SpatialScore]:
    """Illustrate tie inflation for a finite synthetic grid, not replay legacy code."""
    _validate(scores, reference)
    if not all(isfinite(value) for value in scores):
        raise ValueError("the legacy illustration accepts only finite synthetic scores")
    budget = max(1, _selection_budget(len(scores), top_fraction))
    threshold = sorted(scores, reverse=True)[budget - 1]
    selected = [index for index, value in enumerate(scores) if value >= threshold]
    return threshold, _summarize(selected, reference, budget)
