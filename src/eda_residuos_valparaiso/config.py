from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, model_validator


class StudyConfig(BaseModel):
    name: str
    region_code: str
    province_code: str
    commune_code: str
    commune_name: str
    census_year: int = 2024
    projection_year: int = 2026
    commune_projection_2026: float | None = None


class PathsConfig(BaseModel):
    raw: Path
    interim: Path
    processed: Path
    outputs: Path
    sources: Path


class CensusColumnsConfig(BaseModel):
    block_id: str
    region_code: str
    province_code: str
    commune_code: str
    population: str
    households: str
    occupied_dwellings: str
    apartments: str


class SeasonalWasteConfig(BaseModel):
    total_waste_kg_per_person_day: float = Field(gt=0)
    organic_fraction: float = Field(ge=0, le=1)
    factor_source_id: str

    @property
    def organic_waste_kg_per_person_day(self) -> float:
        return self.total_waste_kg_per_person_day * self.organic_fraction


class WasteConfig(BaseModel):
    winter: SeasonalWasteConfig
    summer: SeasonalWasteConfig


class CaptureConfig(BaseModel):
    separation_efficiency: float = Field(ge=0, le=1)
    accepted_fraction: float = Field(ge=0, le=1)
    safety_margin: float = Field(ge=0)
    assumptions_status: str
    scenarios: dict[str, float]

    @model_validator(mode="after")
    def validate_scenarios(self) -> "CaptureConfig":
        if not self.scenarios:
            raise ValueError("Debe existir al menos un escenario de participación.")
        for name, value in self.scenarios.items():
            if not 0 <= value <= 1:
                raise ValueError(f"Participación inválida para {name}: {value}")
        return self


class BuildingDefaultsConfig(BaseModel):
    average_people_per_occupied_unit: float | None = Field(default=None, gt=0)
    occupancy_default_allowed: bool = False


class SpatialConfig(BaseModel):
    output_crs: str
    map_crs: str


class SyntheticDemoConfig(BaseModel):
    seed: int
    projected_population_2026: float = Field(gt=0)


class AppConfig(BaseModel):
    study: StudyConfig
    paths: PathsConfig
    census_columns: CensusColumnsConfig
    waste: WasteConfig
    capture: CaptureConfig
    building: BuildingDefaultsConfig
    spatial: SpatialConfig
    synthetic_demo: SyntheticDemoConfig

    @classmethod
    def from_yaml(cls, path: Path) -> "AppConfig":
        with path.open("r", encoding="utf-8") as handle:
            raw = yaml.safe_load(handle)
        return cls.model_validate(raw)

    def seasonal(self, season: Literal["winter", "summer"]) -> SeasonalWasteConfig:
        return getattr(self.waste, season)
