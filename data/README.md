# Datos

Los archivos oficiales grandes no se versionan.

## Censo 2024

Colocar la base territorial y la cartografía oficial bajo `data/raw/census_2024/`. Antes de ejecutar datos reales, revisar el diccionario de variables INE y mapear nombres en `configs/vina_del_mar.yaml`.

## Proyecciones 2026

Colocar la tabla oficial bajo `data/raw/projections/` y registrar el total comunal de Viña del Mar en `study.commune_projection_2026`. No usar una cifra estimada manualmente como si fuese oficial.

## Residuos

Los factores estacionales de Viña del Mar están declarados en configuración y referencian el estudio SUBDERE 2024. El PDF/anexos pueden conservarse localmente bajo `data/raw/waste/subdere_2024/`.

## Edificios

Copiar `data/external/buildings_template.csv` a `data/external/buildings.csv` y completar únicamente datos agregados.
