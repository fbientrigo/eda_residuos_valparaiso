from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def write_figures(blocks: pd.DataFrame, output_dir: Path) -> None:
    figure_dir = output_dir / "figures"
    figure_dir.mkdir(parents=True, exist_ok=True)
    expected_summer = blocks[(blocks["season"] == "summer") & (blocks["scenario"] == "expected")]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(expected_summer["block_id"], expected_summer["organic_captured_kg_day"])
    ax.set_title("Residuos orgánicos capturados por manzana — verano, escenario esperado")
    ax.set_ylabel("kg/día")
    ax.set_xlabel("Manzana")
    fig.tight_layout()
    fig.savefig(figure_dir / "organic_waste_distribution.png", dpi=150)
    plt.close(fig)
    summary = blocks.groupby(["season", "scenario"], as_index=False)["organic_captured_kg_day"].sum()
    pivot = summary.pivot(index="scenario", columns="season", values="organic_captured_kg_day")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    pivot.plot(kind="bar", ax=ax)
    ax.set_title("Comparación de escenarios de captura")
    ax.set_ylabel("kg/día")
    ax.set_xlabel("Escenario")
    fig.tight_layout()
    fig.savefig(figure_dir / "scenario_comparison.png", dpi=150)
    plt.close(fig)
