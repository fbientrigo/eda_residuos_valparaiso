from __future__ import annotations

from pathlib import Path

import pandas as pd
import typer

from .acquisition.manual import manual_instructions
from .config import AppConfig
from .models.building import estimate_building
from .pipeline import run_synthetic
from .provenance import load_source_registry, resolved_manifest
from .schemas import BuildingInput

app = typer.Typer(help="EDA reproducible de residuos orgánicos residenciales en Valparaíso.")
sources_app = typer.Typer(help="Registro y validación de fuentes.")
app.add_typer(sources_app, name="sources")
DEFAULT_CONFIG = Path("configs/vina_del_mar.yaml")


def _config(path: Path) -> AppConfig:
    return AppConfig.from_yaml(path)


@sources_app.command("list")
def sources_list(config: Path = typer.Option(DEFAULT_CONFIG, "--config")) -> None:
    cfg = _config(config)
    for source in load_source_registry(cfg.paths.sources):
        typer.echo(f"{source.dataset_id:35} {source.acquisition_method:10} {source.title}")


@sources_app.command("validate")
def sources_validate(config: Path = typer.Option(DEFAULT_CONFIG, "--config")) -> None:
    cfg = _config(config)
    manifest = resolved_manifest(load_source_registry(cfg.paths.sources))
    typer.echo(manifest[["dataset_id", "acquisition_method", "processing_status"]].to_string(index=False))


@app.command("fetch")
def fetch(config: Path = typer.Option(DEFAULT_CONFIG, "--config")) -> None:
    cfg = _config(config)
    records = load_source_registry(cfg.paths.sources)
    automatic = [record for record in records if record.acquisition_method == "automatic"]
    if automatic:
        raise typer.BadParameter("Hay fuentes automáticas declaradas, pero falta su adaptador verificado.")
    typer.echo("No hay descargas automáticas habilitadas. Instrucciones de adquisición manual:\n")
    for record in records:
        if record.acquisition_method == "manual":
            typer.echo(manual_instructions(record))


@app.command("prepare")
def prepare(config: Path = typer.Option(DEFAULT_CONFIG, "--config")) -> None:
    cfg = _config(config)
    manifest = resolved_manifest(load_source_registry(cfg.paths.sources))
    census = manifest.loc[manifest["dataset_id"] == "census_2024_blocks"].iloc[0]
    if census["processing_status"] == "missing":
        raise typer.BadParameter(
            "Falta la base Censo 2024. Ejecute 'residuos-valpo fetch' para ver la ruta y fuente esperadas."
        )
    typer.echo("Fuente censal localizada. La siguiente etapa es mapear columnas oficiales en la configuración.")


@app.command("estimate-blocks")
def estimate_blocks(config: Path = typer.Option(DEFAULT_CONFIG, "--config")) -> None:
    cfg = _config(config)
    if cfg.study.commune_projection_2026 is None:
        raise typer.BadParameter(
            "study.commune_projection_2026 es null. Ingrese una proyección comunal oficial verificada. "
            "Para una demostración use 'residuos-valpo run-all'."
        )
    raise typer.BadParameter(
        "La estimación con datos oficiales requiere primero un archivo censal canónico preparado. "
        "El scaffold deja esta frontera explícita para no inferir columnas INE."
    )


@app.command("estimate-building")
def estimate_building_command(
    buildings: Path = typer.Option(Path("data/external/buildings.csv"), "--buildings"),
    config: Path = typer.Option(DEFAULT_CONFIG, "--config"),
) -> None:
    cfg = _config(config)
    if not buildings.exists():
        raise typer.BadParameter(
            f"No existe {buildings}. Copie data/external/buildings_template.csv y complete datos agregados."
        )
    frame = pd.read_csv(buildings)
    rows: list[dict[str, object]] = []
    for record in frame.to_dict(orient="records"):
        clean = {key: (None if pd.isna(value) else value) for key, value in record.items()}
        building = BuildingInput.model_validate(clean)
        rows.extend(item.model_dump() for item in estimate_building(building, cfg))
    output = cfg.paths.outputs / "tables/building_estimates.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output, index=False)
    typer.echo(f"Escrito: {output}")


@app.command("map")
def map_command(config: Path = typer.Option(DEFAULT_CONFIG, "--config")) -> None:
    cfg = _config(config)
    parquet = cfg.paths.outputs / "tables/block_estimates.parquet"
    if not parquet.exists():
        raise typer.BadParameter("No existen estimaciones territoriales. Ejecute run-all o estimate-blocks primero.")
    raise typer.BadParameter(
        "El remapeo independiente desde Parquet queda reservado para la etapa con datos oficiales; "
        "run-all ya genera los tres mapas del fixture sintético."
    )


@app.command("run-all")
def run_all(config: Path = typer.Option(DEFAULT_CONFIG, "--config")) -> None:
    outputs = run_synthetic(config)
    typer.echo("Demostración sintética completada. No representa datos observados de Viña del Mar.")
    for name, path in outputs.items():
        typer.echo(f"{name}: {path}")


if __name__ == "__main__":
    app()
