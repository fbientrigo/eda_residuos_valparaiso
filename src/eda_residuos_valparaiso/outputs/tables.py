from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import pandas as pd


def dataframe_without_geometry(frame: pd.DataFrame) -> pd.DataFrame:
    result = pd.DataFrame(frame.copy())
    if "geometry" in result.columns:
        result["geometry_wkt"] = result["geometry"].astype(str)
        result = result.drop(columns="geometry")
    return result


def write_tables(
    blocks: gpd.GeoDataFrame,
    building_estimates: pd.DataFrame,
    provenance: pd.DataFrame,
    output_dir: Path,
) -> None:
    table_dir = output_dir / "tables"
    table_dir.mkdir(parents=True, exist_ok=True)
    blocks.to_parquet(table_dir / "block_estimates.parquet", index=False)
    flat_blocks = dataframe_without_geometry(blocks)
    building_estimates.to_csv(table_dir / "building_estimates.csv", index=False)
    commune_summary = (
        flat_blocks.groupby(["season", "scenario"], as_index=False)[
            [
                "organic_generated_kg_day",
                "organic_captured_kg_day",
                "recommended_nominal_capacity_kg_day",
            ]
        ]
        .sum()
        .rename(columns={"organic_generated_kg_day": "commune_organic_generated_kg_day"})
    )
    commune_summary.to_csv(table_dir / "commune_summary.csv", index=False)
    commune_summary.to_csv(table_dir / "scenario_summary.csv", index=False)
    metadata = pd.DataFrame(
        [
            {"key": "population_2024", "meaning": "observed census population"},
            {
                "key": "population_target_year",
                "meaning": "synthetic projection when reference year is 2026",
            },
        ]
    )
    with pd.ExcelWriter(table_dir / "block_estimates.xlsx", engine="openpyxl") as writer:
        metadata.to_excel(writer, sheet_name="metadata", index=False)
        provenance.to_excel(writer, sheet_name="source_provenance", index=False)
        demographic_cols = [
            "block_id",
            "population_2024",
            "households_2024",
            "occupied_dwellings_2024",
            "apartments_2024",
            "population_target_year",
            "population_reference_year",
            "population_estimation_method",
        ]
        flat_blocks[demographic_cols].drop_duplicates("block_id").to_excel(
            writer, sheet_name="block_demographics", index=False
        )
        flat_blocks.to_excel(writer, sheet_name="block_waste_estimates", index=False)
        commune_summary.to_excel(writer, sheet_name="scenarios", index=False)
        commune_summary.to_excel(writer, sheet_name="commune_summary", index=False)
