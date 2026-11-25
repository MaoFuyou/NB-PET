"""Run an NB-PET-inspired metric demonstration using only generated toy arrays."""

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nbpet_demo import legacy_threshold_demo, score_top_positive


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=ROOT / "configs" / "synthetic_evaluation.json",
        help="JSON with toy grid size and the indices for generated responses and reference",
    )
    parser.add_argument("--json", action="store_true", help="emit the toy scores as JSON")
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    size = config["grid_size"]
    positive = config["positive_response_indices"]
    start, stop = config["reference_interval"]
    if type(size) is not int or size < 1:
        parser.error("grid_size must be a positive integer")
    if any(type(index) is not int or not 0 <= index < size for index in positive):
        parser.error("positive_response_indices must lie inside the toy grid")
    if type(start) is not int or type(stop) is not int or not 0 <= start <= stop <= size:
        parser.error("reference_interval must be a valid half-open interval")

    positive = set(positive)
    scores = [float(index in positive) for index in range(size)]
    reference = [start <= index < stop for index in range(size)]
    kwargs = {"top_fraction": config["top_fraction"]}
    threshold, legacy = legacy_threshold_demo(scores, reference, **kwargs)
    corrected = score_top_positive(scores, reference, **kwargs)

    if args.json:
        output = {
            "synthetic": True,
            "legacy_threshold": threshold,
            "legacy_threshold_demo": asdict(legacy),
            "positive_budget": asdict(corrected),
        }
        print(json.dumps(output, indent=2))
        return

    print("Synthetic evaluation only — no model or patient data.")
    print(f"Toy grid: {size} pixels; positive scores: {len(positive)}; reference: {legacy.n_reference}")
    print(
        f"Threshold rule (H >= {threshold:g}): selected {legacy.n_selected}/{size}; "
        f"Hit={legacy.hit}; Recall={legacy.region_recall}"
    )
    print(
        f"Positive-only rule (budget {corrected.budget}): selected {corrected.n_selected}/{size}; "
        f"Hit={corrected.hit}; Recall={corrected.region_recall}"
    )
    print("Hit and Recall are undefined (None / null) when the reference is empty.")


if __name__ == "__main__":
    main()
