# 0009. Store finishes as booleans

- **Status:** Accepted
- **Date:** 2026-11-01

## Context

A printing can exist in any combination of finishes: nonfoil, foil, and etched.
Scryfall lists them as an array, such as `["nonfoil", "foil"]`. When a copy is
added to the collection, the app must check: *is this finish valid for this printing?*

## Decision

Store three booleans on `printings`: `has_nonfoil`, `has_foil`, and `has_etched`,
each defaulting to `false`, so a finish is valid only when Scryfall says it exists.

## Alternatives considered

- **A string such as `"nonfoil,foil"`:** a single column, but every check means
  parsing text or a `LIKE` search.
- **A separate `printing_finishes` table:** fully normalized and open to new finishes,
  but a join for a small, rarely changing set of values.

## Consequences

- The validity check reads plainly (`printing.has_foil`) and filters simply in SQL.
- A new finish type means adding a column with a migration. That is rare, and a
  migration is cheap.
