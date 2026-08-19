from pathlib import Path

import pytest
import yaml

pyarrow = pytest.importorskip("pyarrow")

from eda_residuos_valparaiso.pipeline import run_synthetic


def test_synthetic_run_all_produces_expected_outputs(tmp_path: Path) -> None:
    source = Path("configs/vina_del_mar.yaml")
    raw = yaml.safe_load(source.read_text(encoding="utf-8"))
    raw["paths"]["outputs"] = str(tmp_path / "outputs")
    raw["paths"]["sources"] = str(Path("configs/sources.yaml").resolve())
    config = tmp_path / "config.yaml"
    config.write_text(yaml.safe_dump(raw, allow_unicode=True), encoding="utf-8")
    outputs = run_synthetic(config)
    assert outputs["blocks_parquet"].exists()
    assert outputs["blocks_excel"].exists()
    assert outputs["buildings"].exists()
    assert outputs["demographic_map"].exists()
    assert (tmp_path / "outputs/maps/organic_waste_winter.html").exists()
    assert (tmp_path / "outputs/maps/organic_waste_summer.html").exists()
    assert (tmp_path / "outputs/figures/scenario_comparison.png").exists()
    assert (tmp_path / "outputs/provenance_manifest.csv").exists()
