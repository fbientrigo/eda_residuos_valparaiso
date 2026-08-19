# EDA de residuos orgánicos — Valparaíso

Herramienta reproducible para una tesis de Ingeniería Industrial que estima generación de residuos orgánicos residenciales y capacidad preliminar de compostaje. Viña del Mar es el primer caso completo.

## Pregunta operacional

Dada una población observada o estimada, una época del año y un escenario de participación, ¿cuántos kg/día de residuos orgánicos podrían capturarse y qué capacidad nominal de compostaje sería necesaria?

## Escalas y significado

- **Comuna:** control de coherencia y contexto municipal.
- **Manzana censal:** unidad territorial fina del Censo 2024. No representa un edificio.
- **Edificio/condominio:** caso explícito con datos de ocupación propios o administrativos.

La población a nivel manzana del Censo 2024 es **observada**. Cualquier valor 2026 por manzana es una **estimación sintética** que preserva la distribución 2024 y ajusta el total a una proyección comunal oficial.

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Demostración sin datos externos

```bash
residuos-valpo run-all --config configs/vina_del_mar.yaml
pytest
```

`run-all` genera un fixture territorial sintético y dos edificios de ejemplo. Los resultados quedan explícitamente marcados como sintéticos.

## Datos oficiales

```bash
residuos-valpo sources list --config configs/vina_del_mar.yaml
residuos-valpo sources validate --config configs/vina_del_mar.yaml
residuos-valpo fetch --config configs/vina_del_mar.yaml
```

Las fuentes cuyo enlace directo no sea estable se registran como adquisición manual. El pipeline no hace scraping de portales interactivos.

## Comandos

```text
residuos-valpo sources list
residuos-valpo sources validate
residuos-valpo fetch
residuos-valpo prepare
residuos-valpo estimate-blocks
residuos-valpo estimate-building
residuos-valpo map
residuos-valpo run-all
```

Todos aceptan `--config configs/vina_del_mar.yaml`.

## Salidas

`run-all` produce tablas CSV/Parquet/Excel, figuras PNG, mapas HTML y un manifiesto de procedencia. Ver `docs/methodology.md` para ecuaciones y `docs/limitations.md` para restricciones.

## Principio de diseño

El código es un instrumento de investigación: las hipótesis científicas y operacionales se mantienen en configuración y documentos, no ocultas en funciones Python.
