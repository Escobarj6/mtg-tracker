# 0001. Store color identity as a bitmask

- **Status:** Accepted
- **Date:** 2026-10-23

## Context

The app's core deck-building question is: *which cards fit this commander?* In
Commander, a card can go in a deck only if its color identity is a subset of the
commander's. That check runs constantly: browsing unused singles, building a deck,
validating a deck.

Scryfall provides color identity as a list of letters, such as `["G", "W"]`. SQL has
no list type, and a subset check on text is awkward to express in a query, which
pushes filtering out of the database and into Python.

## Decision

Store `oracle_cards.color_identity` as an integer bitmask, one bit per color:

| Color | W | U | B | R | G |
|-------|---|---|---|---|---|
| Bit   | 1 | 2 | 4 | 8 | 16 |

A green-white card is `1 + 16 = 17`; colorless is `0`. A card fits a commander when
it has no bits outside the commander's bits:

```sql
WHERE (color_identity & ~@commander_identity) = 0
```

`colors` stays a string (for example `"GW"`), because it is only displayed, never filtered.

## Alternatives considered

- **String (`"GW"`):** readable in the database, but the subset check needs string
  logic or loading candidates into Python.
- **Separate `card_colors` table:** fully normalized, but every check becomes a join
  plus grouping, which is heavy for a five-value set that never changes.

## Consequences

- The core filter is a single bitwise expression that the database evaluates directly.
- Raw values such as `17` are not human-readable. A small helper converts between
  letters and the bitmask; the import and the API use it, so users only see letters.
- Bitwise expressions can't use a normal index, so there is no index on the column.
  At collection scale (thousands of cards), a full check is effectively instant.
- Changing the format later would require a migration that converts every row, which
  is why it was decided before any data existed.
