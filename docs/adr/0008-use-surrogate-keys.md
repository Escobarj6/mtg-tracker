# 0008. Use surrogate keys, with Scryfall IDs as unique columns

- **Status:** Accepted
- **Date:** 2026-10-23

## Context

Card data comes from Scryfall, which assigns UUIDs to cards (`oracle_id`), printings
(`id`), and sets. Tables need primary keys, and foreign keys will reference them
constantly.

## Decision

Every table has its own integer primary key, `id`, assigned by the database.
Scryfall's IDs are stored as ordinary columns (`scryfall_id`, `scryfall_oracle_id`)
with a unique index.

## Alternatives considered

- **Scryfall UUIDs as primary keys (natural keys):** no extra column, but the
  database's identity would depend on an outside system's choices, and every foreign
  key would carry a 36-character string instead of an integer.

## Consequences

- Joins and foreign keys use compact integers.
- The schema stays independent of Scryfall; data from other sources fits without
  changing keys.
- Unique indexes on Scryfall IDs prevent duplicate imports and make lookups by
  Scryfall ID fast, which the import depends on.
- Imports must translate Scryfall IDs to internal IDs when linking rows.
