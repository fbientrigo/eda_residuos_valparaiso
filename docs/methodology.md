# Metodología

## Propósito

El pipeline estima la carga de residuos orgánicos residenciales que podría desviarse de disposición final y la capacidad nominal de compostaje asociada. El código implementa el método; no constituye el objeto central de la tesis.

## Jerarquía de datos

1. Observación territorial: Censo 2024 a nivel manzana-entidad.
2. Actualización temporal: proyección oficial comunal 2026, cuando esté disponible y verificada.
3. Generación de residuos: factores estacionales específicos de Viña del Mar provenientes de SUBDERE 2024.
4. Captura: escenarios explícitos de participación, eficiencia de separación y fracción aceptada.
5. Edificio: ocupación observada o administrativa; si no existe, una inferencia declarada.

## Proyección territorial 2026

Para cada manzana `i`:

`P_i,2026 = P_i,2024 * P_comuna,2026 / sum(P_i,2024)`

La suma de las manzanas proyectadas debe reproducir el total comunal objetivo dentro de tolerancia numérica. El resultado se etiqueta como estimación sintética, no como observación censal.

## Residuos orgánicos

Para estación `s`:

`Q_org = P * g_total,s * f_org,s`

`Q_capt = Q_org * p_participacion * eta_separacion * f_aceptada`

`C_nom = Q_capt * (1 + margen_seguridad)`

Unidades principales: personas y kg/día. Los resultados mensuales usan 30.44 días/mes y los anuales 365 días/año.

## Escenarios

Los escenarios conservador, esperado y alto modifican solamente la participación. Eficiencia de separación, fracción aceptada y margen de seguridad permanecen visibles en configuración para facilitar análisis de sensibilidad posterior.

## Edificios

Precedencia para estimar residentes:

1. `observed_residents` si existe;
2. `occupied_units * average_people_per_occupied_unit`;
3. error de validación si faltan ambos.

La manzana censal no se utiliza como sustituto silencioso de un edificio.

## Validación

- conservación del total poblacional proyectado;
- no negatividad de poblaciones y flujos;
- fracciones entre 0 y 1;
- comparación independiente invierno/verano;
- coherencia ordinal de escenarios;
- control comunal contra cifras municipales como capa separada.

## Incertidumbre

La mayor incertidumbre de dimensionamiento inicial suele provenir de participación real, separación correcta y ocupación del edificio. Estos parámetros deben transformarse en escenarios o mediciones piloto, no presentarse como hechos.
