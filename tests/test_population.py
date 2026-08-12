import math

import pandas as pd

from eda_residuos_valparaiso.models.population import project_blocks_to_commune_total


def test_projected_blocks_sum_to_target() -> None:
    frame = pd.DataFrame({"population_2024": [100, 200, 0, 300]})
    result = project_blocks_to_commune_total(frame, 720)
    assert math.isclose(result["population_target_year"].sum(), 720.0)
    assert result.loc[2, "population_target_year"] == 0
