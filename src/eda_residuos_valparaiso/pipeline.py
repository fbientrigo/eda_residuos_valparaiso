from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import box

from .config import AppConfig
from .models.building import estimate_building
from .models.organic_waste import estimate_block_waste
from .models.population import project_blocks_to_commune_total
from .outputs.figures import write_figures
from .outputs.maps import write_maps
from .outputs.tables import write_tables
from .provenance import load_source_registry, resolved_manifest
from .schemas import BuildingInput


def synthetic_blocks(config: AppConfig) -> gpd.GeoDataFrame:
    populations = [380, 520, 210, 460, 0, 300, 430, 260]
    households = [130, 190, 80, 160, 0, 110, 165, 95]
    occupied = [125, 182, 75, 154, 0, 105, 158, 90]
    apartments = [110, 170, 8, 120, 0, 15, 145, 20]
    rows: list[dict[str, object]] = []
    lon0, lat0 = -71.57, -33.04
    width, height = 0.01, 0.008
    for index, population in enumerate(populations):
        col, row = index % 4, index // 4
        xmin = lon0 + col * width
        ymin = lat0 + row * height
        rows.append(
            {
                "block_id": f"SYN-{index + 1:03d}",
                "region_code": config.study.region_code,
                "province_code": config.study.province_code,
                "commune_code": config.study.commune_code,
                "population_2024": population,
                "households_2024": households[index],
                "occupied_dwellings_2024": occupied[index],
                "apartments_2024": apartments[index],
                "geometry": box(xmin, ymin, xmin + width * 0.8, ymin + height * 0.8),
            }
        )
    return gpd.GeoDataFrame(rows, geometry="geometry", crs="EPSG:4326")


def synthetic_buildings() -> list[BuildingInput]:
    return [
        BuildingInput(
            building_id="SYN-BLD-001",
            building_name="Edificio sintético A",
            commune="Viña del Mar",
            total_units=100,
            occupied_units=90,
            average_people_per_occupied_unit=2.4,
            occupancy_data_method="synthetic",
            latitude=-33.02,
            longitude=-71.55,
            notes="Fixture sintético: ocupación inferida desde unidades.",
        ),
        BuildingInput(
            building_id="SYN-BLD-002",
            building_name="Edificio sintético B",
            commune="Viña del Mar",
            total_units=60,
            occupied_units=55,
            observed_residents=132,
            occupancy_data_method="synthetic",
            latitude=-33.03,
            longitude=-71.54,
            notes="Fixture sintético: precedencia por residentes observados.",
        ),
    ]


def run_synthetic(config_path: Path) -> dict[str, Path]:
    config = AppConfig.from_yaml(config_path)
    output_dir = config.paths.outputs
    output_dir.mkdir(parents=True, exist_ok=True)
    blocks = synthetic_blocks(config)
    projected = project_blocks_to_commune_total(
        blocks,
        target_population=config.synthetic_demo.projected_population_2026,
    )
    estimated = estimate_block_waste(projected, config)
    estimated = gpd.GeoDataFrame(estimated, geometry="geometry", crs=blocks.crs)
    building_rows: list[dict[str, object]] = []
    for building in synthetic_buildings():
        building_rows.extend(item.model_dump() for item in estimate_building(building, config))
    buildings = pd.DataFrame(building_rows)
    provenance = resolved_manifest(load_source_registry(config.paths.sources))
    synthetic_row = pd.DataFrame(
        [
            {
                "dataset_id": "synthetic_census_fixture",
                "title": "Fixture territorial sintético",
                "institution": "Proyecto de tesis",
                "source_url": "",
                "publication_year": 2026,
                "reference_year": 2024,
                "geographic_resolution": "manzana sintética",
                "expected_format": "GeoDataFrame",
                "local_path": "generated in memory",
                "acquisition_method": "synthetic",
                "license_note": "Solo demostración",
                "notes": "No usar como evidencia empírica.",
                "acquired_at": "",
                "checksum": "",
                "processing_status": "synthetic",
            }
        ]
    )
    provenance = pd.concat([provenance, synthetic_row], ignore_index=True)
    provenance.to_csv(output_dir / "provenance_manifest.csv", index=False)
    write_tables(estimated, buildings, provenance, output_dir)
    write_figures(estimated, output_dir)
    write_maps(estimated, output_dir)
    return {
        "outputs": output_dir,
        "blocks_parquet": output_dir / "tables/block_estimates.parquet",
        "blocks_excel": output_dir / "tables/block_estimates.xlsx",
        "buildings": output_dir / "tables/building_estimates.csv",
        "demographic_map": output_dir / "maps/demographic_map.html",
    }
