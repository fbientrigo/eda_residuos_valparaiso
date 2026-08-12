from __future__ import annotations

from pathlib import Path

import folium
import geopandas as gpd


def _base_map(frame: gpd.GeoDataFrame) -> folium.Map:
    mapped = frame.to_crs("EPSG:4326")
    center = mapped.geometry.unary_union.centroid
    return folium.Map(location=[center.y, center.x], zoom_start=13, tiles="CartoDB positron")


def write_demographic_map(frame: gpd.GeoDataFrame, output_path: Path) -> None:
    unique = frame.drop_duplicates("block_id").to_crs("EPSG:4326").copy()
    m = _base_map(unique)
    folium.GeoJson(
        unique,
        tooltip=folium.GeoJsonTooltip(
            fields=[
                "block_id",
                "population_2024",
                "population_target_year",
                "population_reference_year",
                "population_estimation_method",
                "households_2024",
                "occupied_dwellings_2024",
                "apartments_2024",
            ],
            aliases=[
                "Manzana",
                "Población 2024",
                "Población usada",
                "Año población",
                "Método",
                "Hogares",
                "Viviendas ocupadas",
                "Departamentos",
            ],
        ),
    ).add_to(m)
    m.save(output_path)


def write_waste_map(frame: gpd.GeoDataFrame, season: str, output_path: Path) -> None:
    subset = frame[(frame["season"] == season) & (frame["scenario"] == "expected")].copy()
    subset = subset.to_crs("EPSG:4326")
    m = _base_map(subset)
    folium.Choropleth(
        geo_data=subset,
        data=subset,
        columns=["block_id", "organic_captured_kg_day"],
        key_on="feature.properties.block_id",
        fill_opacity=0.7,
        line_opacity=0.3,
        legend_name=f"Orgánicos capturados kg/día — {season}",
    ).add_to(m)
    folium.GeoJson(
        subset,
        tooltip=folium.GeoJsonTooltip(
            fields=[
                "block_id",
                "population_target_year",
                "population_reference_year",
                "population_estimation_method",
                "households_2024",
                "occupied_dwellings_2024",
                "apartments_2024",
                "organic_generated_kg_day",
                "organic_captured_kg_day",
                "recommended_nominal_capacity_kg_day",
            ]
        ),
    ).add_to(m)
    m.save(output_path)


def write_maps(frame: gpd.GeoDataFrame, output_dir: Path) -> None:
    map_dir = output_dir / "maps"
    map_dir.mkdir(parents=True, exist_ok=True)
    write_demographic_map(frame, map_dir / "demographic_map.html")
    write_waste_map(frame, "winter", map_dir / "organic_waste_winter.html")
    write_waste_map(frame, "summer", map_dir / "organic_waste_summer.html")
