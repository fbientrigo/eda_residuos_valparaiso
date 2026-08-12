from pathlib import Path

from eda_residuos_valparaiso.config import AppConfig
from eda_residuos_valparaiso.models.organic_waste import estimate_block_waste
from eda_residuos_valparaiso.models.population import project_blocks_to_commune_total
from eda_residuos_valparaiso.pipeline import synthetic_blocks

CONFIG = Path("configs/vina_del_mar.yaml")


def test_seasons_and_scenarios_are_independent() -> None:
    config = AppConfig.from_yaml(CONFIG)
    blocks = synthetic_blocks(config)
    projected = project_blocks_to_commune_total(blocks, 2800)
    result = estimate_block_waste(projected, config)
    assert set(result["season"]) == {"winter", "summer"}
    assert set(result["scenario"]) == {"conservative", "expected", "high"}
    summer = result[(result.season == "summer") & (result.scenario == "expected")]
    winter = result[(result.season == "winter") & (result.scenario == "expected")]
    assert summer["organic_generated_kg_day"].sum() > winter["organic_generated_kg_day"].sum()


def test_zero_population_produces_zero_waste() -> None:
    config = AppConfig.from_yaml(CONFIG)
    blocks = synthetic_blocks(config)
    projected = project_blocks_to_commune_total(blocks, 2800)
    result = estimate_block_waste(projected, config)
    zero = result[result.block_id == "SYN-005"]
    assert (zero["organic_generated_kg_day"] == 0).all()
    assert (zero["organic_captured_kg_day"] == 0).all()


def test_scenario_ordering() -> None:
    config = AppConfig.from_yaml(CONFIG)
    blocks = synthetic_blocks(config)
    projected = project_blocks_to_commune_total(blocks, 2800)
    result = estimate_block_waste(projected, config)
    totals = result[result.season == "summer"].groupby("scenario")["organic_captured_kg_day"].sum()
    assert totals["conservative"] < totals["expected"] < totals["high"]
