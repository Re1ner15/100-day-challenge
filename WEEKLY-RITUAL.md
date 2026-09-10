# Weekly Ritual (repeat for all 14 weeks + final 2 days)

Every week runs as a **target → execute → verify loop**: on Monday we set a *target* for next Monday's scan (from the plan), chase it all week, then check the actual scan against it. The target is motivation; the gap self-calibrates the TDEE.

## Monday (START of week) — set the PREDICTION (your target)
Predict *next* Monday's scan from the **plan**, so there's a number to chase all week:

- **Fat mass Δ** = − (planned weekly deficit ÷ 7,700 kcal/kg). Plan = ~1,750 kcal intake vs TDEE ~2,700 ≈ **950/day → ~6,650/wk → ≈ −0.85 kg fat**.
- **SMM (muscle)** = **hold** (flat) — the reward for hitting ~160 g protein daily.
- **Weight Δ** = fat Δ ± water noise (carb/sodium/alcohol swings can mask ±1 kg — expect noise on high-carb/drinking weeks).
- **PBF %** = new fat ÷ new weight. **Visceral** = tracks fat (fastest early mover).

Write into `charts/data/week-NN.json` → `inbody.expected` (+ one-line `expected_basis`). **This is the number to beat — hit your plan, hit the prediction.**

## During the week (daily)
Log **facts only** — nutrition + macros, walks, workouts (weights × reps + EASY/GOOD/HARD/MAX), sleep. Every day, you can see how you're tracking against Monday's target.

## Next Monday — record ACTUAL + compare + re-predict
1. Add the scan to `inbody.current` in the JSON.
2. `python3 charts/make_week.py NN` → regenerates `week-NN.png` + `week-NN-inbody.png` (Expected vs Actual).
3. Set the **new week's** prediction (start of the next week's loop).
4. Update `logs/week-NN-summary.md` with the verdict:
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
