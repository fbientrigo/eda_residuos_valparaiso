from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator


class SourceRecord(BaseModel):
    dataset_id: str
    title: str
    institution: str
    source_url: str = ""
    publication_year: int | None = None
    reference_year: int | None = None
    geographic_resolution: str
    expected_format: str
    local_path: str
    acquisition_method: Literal["automatic", "manual", "synthetic", "derived"]
    license_note: str = ""
    notes: str = ""


class BuildingInput(BaseModel):
    building_id: str
    building_name: str
    commune: str
    address: str = ""
    total_units: int = Field(ge=0)
    occupied_units: int | None = Field(default=None, ge=0)
    average_people_per_occupied_unit: float | None = Field(default=None, gt=0)
    observed_residents: int | None = Field(default=None, ge=0)
    occupancy_data_method: str
    latitude: float | None = None
    longitude: float | None = None
    notes: str = ""

    @model_validator(mode="after")
    def validate_occupancy(self) -> "BuildingInput":
        if self.occupied_units is not None and self.occupied_units > self.total_units:
            raise ValueError("occupied_units no puede superar total_units")
        return self


class BuildingEstimate(BaseModel):
    building_id: str
    building_name: str
    estimated_residents: float
    population_estimation_method: str
    occupancy_data_method: str
    season: str
    scenario: str
    organic_generated_kg_day: float
    organic_captured_kg_day: float
    recommended_nominal_capacity_kg_day: float
    monthly_input_tonnes: float
    annual_input_tonnes: float
