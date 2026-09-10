# Weekly Ritual (repeat for all 14 weeks + final 2 days)

Every week runs as a **prediction → verification loop**: we predict the InBody result from the week's numbers *before* the scan, then check it against the actual scan. The gap self-calibrates the TDEE.

## During the week (daily)
Log **facts only** as they happen — nutrition + macros, walks, workouts (weights × reps + EASY/GOOD/HARD/MAX), sleep. (See [`nutrition.md`](./nutrition.md), [`logs/activity-log.md`](./logs/activity-log.md), workout files.)

## Sunday night — compute EXPECTED
Once the full week is logged, predict the Monday scan from the week's totals:

- **Fat mass Δ** = − (week's total deficit ÷ 7,700 kcal/kg). e.g. avg 800 kcal/day × 7 = 5,600 → ≈ −0.7 kg fat.
- **SMM (muscle)** = **hold** (flat) if protein averaged ≥ ~150 g. Drop only expected if protein was low or deficit extreme.
- **Weight Δ** = fat Δ ± water noise (carb/sodium/alcohol swings can mask fat loss by ±1 kg — flag high-carb/drinking weeks).
- **PBF %** = derived from new fat ÷ new weight.
- **Visceral** = tracks fat, usually the fastest early mover.

Write these into `charts/data/week-NN.json` → `inbody.expected` (+ a one-line `expected_basis`).

## Monday — record ACTUAL + compare
1. Add the scan to `inbody.current` in the JSON.
2. `python3 charts/make_week.py NN` → regenerates `week-NN.png` (daily dashboard) + `week-NN-inbody.png` (Expected vs Actual).
3. Update `logs/week-NN-summary.md` with the verdict:
   - **Actual fat loss ≈ expected + SMM held** → 🎯 system working. Keep TDEE, proceed with progression.
   - **Actual fat loss > expected** → TDEE is higher than 2,700 (or under-logged). Nudge the TDEE up.
   - **Actual < expected** → TDEE lower, or water masking (recheck next week), or intake under-counted.
   - **SMM dropping** → deficit too aggressive → raise calories/protein.

## Files per week
| File | Role |
|------|------|
| `charts/data/week-NN.json` | the week's daily numbers + inbody baseline/expected/current |
| `charts/make_week.py` | renders `week-NN.png` + `week-NN-inbody.png` from the JSON |
| `logs/week-NN-summary.md` | dashboard embed + table + expected/actual verdict |

Baseline for **each** week = the *previous* Monday's scan (Week 1 baseline = Mon 7 Sep).
