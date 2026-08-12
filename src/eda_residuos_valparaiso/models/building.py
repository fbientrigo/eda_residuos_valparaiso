from __future__ import annotations

from ..config import AppConfig
from ..schemas import BuildingEstimate, BuildingInput


def estimate_residents(building: BuildingInput) -> tuple[float, str]:
    if building.observed_residents is not None:
        return float(building.observed_residents), "observed_residents"
    if building.occupied_units is not None and building.average_people_per_occupied_unit is not None:
        return (
            float(building.occupied_units * building.average_people_per_occupied_unit),
            "occupied_units_x_average_people",
        )
    raise ValueError(
        f"{building.building_id}: faltan residentes observados o la combinación "
        "occupied_units + average_people_per_occupied_unit."
    )


def estimate_building(building: BuildingInput, config: AppConfig) -> list[BuildingEstimate]:
    residents, population_method = estimate_residents(building)
    estimates: list[BuildingEstimate] = []
    for season in ("winter", "summer"):
        factor = config.seasonal(season)
        generated = residents * factor.organic_waste_kg_per_person_day
        for scenario, participation in config.capture.scenarios.items():
            captured = (
                generated
                * participation
                * config.capture.separation_efficiency
                * config.capture.accepted_fraction
            )
            capacity = captured * (1 + config.capture.safety_margin)
            estimates.append(
                BuildingEstimate(
                    building_id=building.building_id,
                    building_name=building.building_name,
                    estimated_residents=residents,
                    population_estimation_method=population_method,
                    occupancy_data_method=building.occupancy_data_method,
                    season=season,
                    scenario=scenario,
                    organic_generated_kg_day=generated,
                    organic_captured_kg_day=captured,
                    recommended_nominal_capacity_kg_day=capacity,
                    monthly_input_tonnes=captured * 30.44 / 1000,
                    annual_input_tonnes=captured * 365 / 1000,
                )
            )
    return estimates
