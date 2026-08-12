from __future__ import annotations

import pandas as pd

from ..config import AppConfig


def estimate_block_waste(frame: pd.DataFrame, config: AppConfig) -> pd.DataFrame:
    rows: list[pd.DataFrame] = []
    for season in ("winter", "summer"):
        factor = config.seasonal(season)
        organic_per_person = factor.organic_waste_kg_per_person_day
        for scenario, participation in config.capture.scenarios.items():
            part = frame.copy()
            part["season"] = season
            part["scenario"] = scenario
            part["participation_rate"] = participation
            part["total_waste_kg_per_person_day"] = factor.total_waste_kg_per_person_day
            part["organic_fraction"] = factor.organic_fraction
            part["organic_waste_kg_per_person_day"] = organic_per_person
            part["factor_source_id"] = factor.factor_source_id
            part["organic_generated_kg_day"] = part["population_target_year"] * organic_per_person
            part["organic_captured_kg_day"] = (
                part["organic_generated_kg_day"]
                * participation
                * config.capture.separation_efficiency
                * config.capture.accepted_fraction
            )
            part["recommended_nominal_capacity_kg_day"] = (
                part["organic_captured_kg_day"] * (1 + config.capture.safety_margin)
            )
            rows.append(part)

    result = pd.concat(rows, ignore_index=True)
    numeric = [
        "organic_generated_kg_day",
        "organic_captured_kg_day",
        "recommended_nominal_capacity_kg_day",
    ]
    if (result[numeric] < 0).any().any():
        raise ValueError("El modelo produjo un flujo de residuos negativo.")
    return result
