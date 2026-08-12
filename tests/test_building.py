import pytest

from eda_residuos_valparaiso.models.building import estimate_residents
from eda_residuos_valparaiso.schemas import BuildingInput


def test_observed_residents_take_precedence() -> None:
    building = BuildingInput(
        building_id="A",
        building_name="A",
        commune="Viña del Mar",
        total_units=100,
        occupied_units=90,
        average_people_per_occupied_unit=2.5,
        observed_residents=180,
        occupancy_data_method="observed",
    )
    residents, method = estimate_residents(building)
    assert residents == 180
    assert method == "observed_residents"


def test_units_times_average_is_fallback() -> None:
    building = BuildingInput(
        building_id="B",
        building_name="B",
        commune="Viña del Mar",
        total_units=100,
        occupied_units=80,
        average_people_per_occupied_unit=2.4,
        occupancy_data_method="administrative",
    )
    residents, method = estimate_residents(building)
    assert residents == pytest.approx(192)
    assert method == "occupied_units_x_average_people"


def test_missing_occupancy_is_actionable_error() -> None:
    building = BuildingInput(
        building_id="C",
        building_name="C",
        commune="Viña del Mar",
        total_units=100,
        occupancy_data_method="unknown",
    )
    with pytest.raises(ValueError, match="occupied_units"):
        estimate_residents(building)
