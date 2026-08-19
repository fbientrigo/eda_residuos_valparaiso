# Fuentes de datos

## INE — Censo 2024

Fuente oficial para población, hogares, viviendas y cartografía a nivel manzana-entidad. Año de referencia: 2024. Publicación territorial: 2025.

El mapeo de columnas se mantiene configurable porque el código no debe adivinar nombres del diccionario oficial.

## INE — Estimaciones y proyecciones, base 2024

Fuente para actualizar el total comunal al año objetivo. La configuración deja el total comunal 2026 como `null` hasta verificar una tabla oficial con la desagregación requerida.

## SUBDERE 2024

Estudio de caracterización de residuos municipales. Para Viña del Mar se conservan como parámetros trazables:

| Temporada | Total kg/hab/día | Fracción orgánica | Orgánico derivado kg/hab/día |
|---|---:|---:|---:|
| Invierno | 0.78 | 0.4681 | 0.3651 |
| Verano | 1.18 | 0.4942 | 0.5832 |

## Totales municipales

Se mantienen como una fuente independiente para control de orden de magnitud. No deben convertirse automáticamente en una tasa residencial por habitante.

## Edificios

Preferencia: administración del edificio. Como alternativas pueden utilizarse antecedentes agregados de DOM/transparencia. La procedencia y método de ocupación deben acompañar cada caso.
