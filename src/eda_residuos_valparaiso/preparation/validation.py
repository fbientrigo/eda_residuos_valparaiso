from __future__ import annotations

import pandas as pd


REQUIRED_BLOCK_COLUMNS = {
    "block_id",
    "region_code",
    "province_code",
    "commune_code",
    "population_2024",
    "households_2024",
    "occupied_dwellings_2024",
    "apartments_2024",
}


def validate_blocks(frame: pd.DataFrame) -> None:
    missing = REQUIRED_BLOCK_COLUMNS - set(frame.columns)
    if missing:
        raise ValueError(f"Faltan columnas canónicas: {sorted(missing)}")
    numeric = [
        "population_2024",
        "households_2024",
        "occupied_dwellings_2024",
        "apartments_2024",
    ]
    if (frame[numeric] < 0).any().any():
        raise ValueError("No se permiten conteos demográficos negativos.")
