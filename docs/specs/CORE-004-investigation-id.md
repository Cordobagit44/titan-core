# CORE-004 — InvestigationId

## Objetivo

Introducir un identificador propio para las investigaciones.

## Reglas

- Cada investigación debe tener un `InvestigationId`.
- El identificador debe generarse automáticamente al crear la investigación.
- Dos investigaciones distintas nunca deben compartir el mismo identificador.
- El identificador debe ser inmutable.
