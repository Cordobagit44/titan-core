# Coding Standard

1. TITAN Core depends only on the Python standard library.
2. Public code is fully typed.
3. `Any` is not used in domain code without a documented exception.
4. Domain concepts are explicit classes, not untyped dictionaries.
5. Value objects and domain events are immutable.
6. Domain state changes through explicit methods.
7. Event names use past tense.
8. Generic modules such as `utils.py`, `helpers.py`, and `misc.py` are prohibited.
9. Abstractions are introduced only after concrete duplication or multiple proven uses.
10. Tests describe behavior and protect architectural boundaries.
