from __future__ import annotations

import math

import pandas as pd


def project_blocks_to_commune_total(
    frame: pd.DataFrame,
    target_population: float,
    census_population_column: str = "population_2024",
) -> pd.DataFrame:
    if target_population < 0:
        raise ValueError("La población objetivo no puede ser negativa.")
    observed_total = float(frame[census_population_column].sum())
    if observed_total <= 0:
        raise ValueError("La población censal comunal debe ser mayor que cero.")

    result = frame.copy()
    result["population_target_year"] = (
        result[census_population_column].astype(float) * target_population / observed_total
    )
    result["population_reference_year"] = 2026
    result["population_estimation_method"] = "synthetic_commune_projection_from_census_2024"
    result["population_is_observed"] = False

    if not math.isclose(
        float(result["population_target_year"].sum()),
        float(target_population),
        rel_tol=1e-9,
        abs_tol=1e-6,
    ):
        raise AssertionError("La proyección por manzana no conserva el total comunal.")
    return result


def mark_observed_2024(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    result["population_target_year"] = result["population_2024"].astype(float)
    result["population_reference_year"] = 2024
    result["population_estimation_method"] = "observed_census_2024"
    result["population_is_observed"] = True
    return result
