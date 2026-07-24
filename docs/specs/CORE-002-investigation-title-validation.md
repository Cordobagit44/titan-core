# CORE-002 — Investigation Title Validation

## Objetivo

Evitar la creación de investigaciones con títulos inválidos.

## Reglas

- El título es obligatorio.
- Un título compuesto únicamente por espacios se considera vacío.
- Si el título es inválido, debe lanzarse una excepción.