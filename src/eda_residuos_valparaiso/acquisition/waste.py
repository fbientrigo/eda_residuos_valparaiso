from __future__ import annotations

from ..config import AppConfig


def waste_factor_summary(config: AppConfig) -> dict[str, float]:
    return {
        "winter_organic_kg_person_day": config.waste.winter.organic_waste_kg_per_person_day,
        "summer_organic_kg_person_day": config.waste.summer.organic_waste_kg_per_person_day,
    }
