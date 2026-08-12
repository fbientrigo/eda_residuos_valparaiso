from __future__ import annotations

import geopandas as gpd

from ..config import AppConfig
from .validation import validate_blocks


def canonicalize_census(frame: gpd.GeoDataFrame, config: AppConfig) -> gpd.GeoDataFrame:
    columns = config.census_columns
    rename = {
        columns.block_id: "block_id",
        columns.region_code: "region_code",
        columns.province_code: "province_code",
        columns.commune_code: "commune_code",
        columns.population: "population_2024",
        columns.households: "households_2024",
        columns.occupied_dwellings: "occupied_dwellings_2024",
        columns.apartments: "apartments_2024",
    }
    result = frame.rename(columns=rename).copy()
    result = result[result["commune_code"].astype(str) == config.study.commune_code].copy()
    validate_blocks(result)
    return result
