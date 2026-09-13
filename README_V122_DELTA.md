# SW BATTLECATS V122 DELTA

- Base: GitHub latest source + V121 DELTA
- Scope: Nintendo Switch Korean stage-detail data enrichment only
- Existing mobile/Nintendo enemy image UI from V121 is unchanged.
- Search whitespace-insensitive behavior is NOT included in this delta; it was requested after V122 work began and is pending separate execution approval.

## Changes
- Legend 112 stages: unlock progression metadata and area-final clear rewards added from Switch guide cross-checks.
- Weekday / guerrilla / XP / catfruit / frenzy / manic stages: verified schedule, reward, unlock and strategy fields added where source supports them.
- Future/Space story: only exact-name/sequence matches against Switch guide were enriched.
- World story: Japanese Switch first-story layout differs from the current Korean-project world-stage layout, so no Japanese data was copied into it.
- Unknown values remain blank.

## Regression protection
- Nintendo enemy_refs: unchanged (333 bindings)
- Nintendo recommended_cats: unchanged (26 bindings)
- Mobile data/UI files: unchanged
- V121 enemy image/card rendering: unchanged
