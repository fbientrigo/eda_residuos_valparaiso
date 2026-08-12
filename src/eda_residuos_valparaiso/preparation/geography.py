from __future__ import annotations

import geopandas as gpd


def ensure_map_crs(frame: gpd.GeoDataFrame, map_crs: str) -> gpd.GeoDataFrame:
    if frame.crs is None:
        raise ValueError("La cartografía no tiene CRS definido.")
    return frame.to_crs(map_crs)
