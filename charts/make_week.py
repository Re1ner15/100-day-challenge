#!/usr/bin/env python3
"""Render a week's dashboard + InBody comparison from data/week-NN.json.

Usage:  python3 make_week.py 1        # renders week-01.png (+ week-01-inbody.png if scan present)

Each data/week-NN.json holds the week's daily numbers and the InBody baseline/current.
Days with null kcal are treated as "not logged yet" and skipped. The InBody panel is
produced only once `inbody.current` is filled in (i.e. after that week's Monday scan).
"""
import json, sys, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
week = int(sys.argv[1]) if len(sys.argv) > 1 else 1
data = json.load(open(os.path.join(HERE, "data", f"week-{week:02d}.json")))

TDEE = data.get("tdee", 2700); KCAL_T = data.get("kcal_target", 1750); PROT_F = data.get("protein_floor", 160)
C_KCAL, C_PROT, C_CARB, C_FAT, C_ACT = "#3b82f6", "#10b981", "#f59e0b", "#8b5cf6", "#ef4444"
GRID, INK, MUT = "#e5e7eb", "#111827", "#6b7280"
plt.rcParams.update({"font.size": 11, "axes.edgecolor": GRID, "axes.linewidth": 1,
                     "text.color": INK, "axes.labelcolor": INK, "xtick.color": MUT, "ytick.color": MUT})

# ---- daily dashboard (only days with data) ----
d = [x for x in data["days"] if x.get("kcal") is not None]
labels_ = [x["day"] for x in d]
kcal = [x["kcal"] for x in d]; prot = [x["protein"] for x in d]
carb = [x["carbs"] for x in d]; fat = [x["fat"] for x in d]; act = [x["active"] for x in d]
x = np.arange(len(d))

def style(a):
    a.grid(axis="y", color=GRID, lw=1); a.set_axisbelow(True)
    for s in ("top", "right"): a.spines[s].set_visible(False)
    a.set_xticks(x); a.set_xticklabels(labels_, fontsize=9)

def vlabels(a, vals, dy=3):
    for xi, v in zip(x, vals):
        a.annotate(f"{v:.0f}", (xi, v), ha="center", va="bottom",
                   xytext=(0, dy), textcoords="offset points", fontsize=9, color=INK)

fig, ax = plt.subplots(2, 2, figsize=(11, 8.2))
fig.suptitle(data["label"], fontsize=16, fontweight="bold", y=0.98)

a = ax[0, 0]; a.bar(x, kcal, color=C_KCAL, width=0.6, zorder=3); vlabels(a, kcal)
a.axhline(TDEE, color=C_ACT, ls="--", lw=1.5); a.axhline(KCAL_T, color=MUT, ls=":", lw=1.5)
a.text(-0.4, TDEE+40, f"TDEE ~{TDEE}", ha="left", color=C_ACT, fontsize=9)
a.text(-0.4, KCAL_T+40, f"target ~{KCAL_T}", ha="left", color=MUT, fontsize=9)
a.set_title("Calories eaten vs TDEE", fontweight="bold", loc="left"); a.set_ylim(0, max(3000, max(kcal)+300)); style(a)

a = ax[0, 1]; a.bar(x, prot, color=C_PROT, width=0.6, zorder=3); vlabels(a, prot)
a.axhline(PROT_F, color=C_ACT, ls="--", lw=1.5); a.text(-0.4, PROT_F+4, f"floor {PROT_F} g", ha="left", color=C_ACT, fontsize=9)
a.set_title("Protein (g) — the muscle guardian", fontweight="bold", loc="left"); a.set_ylim(0, 190); style(a)

a = ax[1, 0]; w = 0.26
a.bar(x-w, prot, w, label="Protein", color=C_PROT, zorder=3)
a.bar(x, carb, w, label="Carbs", color=C_CARB, zorder=3)
a.bar(x+w, fat, w, label="Fat", color=C_FAT, zorder=3)
a.set_title("Macros per day (g)", fontweight="bold", loc="left")
a.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.02), fontsize=9)
a.set_ylim(0, 190); style(a)

a = ax[1, 1]; a.bar(x, act, color=C_ACT, width=0.6, zorder=3); vlabels(a, act)
a.set_title("Active calories burned (workouts + walks)", fontweight="bold", loc="left")
a.set_ylim(0, max(1250, max(act)+150)); style(a)

fig.tight_layout(rect=[0, 0.01, 1, 0.95])
out = os.path.join(HERE, f"week-{week:02d}.png")
fig.savefig(out, dpi=150, facecolor="white", bbox_inches="tight"); print("wrote", out)

# ---- InBody: baseline -> EXPECTED (pre-scan prediction) vs ACTUAL (post-scan) ----
ib = data.get("inbody", {})
base, exp, cur = ib.get("baseline"), ib.get("expected"), ib.get("current")
metrics = [("Weight (kg)", "weight"), ("Muscle SMM (kg)", "smm"),
           ("Fat mass (kg)", "fat"), ("Body fat %", "pbf"), ("Visceral", "visceral")]
if base and (exp or cur):
    names = [m[0] for m in metrics]
    y = np.arange(len(names))[::-1]
    d_exp = [round(exp[k] - base[k], 1) for _, k in metrics] if exp else None
    d_cur = [round(cur[k] - base[k], 1) for _, k in metrics] if cur else None
    fig2, a2 = plt.subplots(figsize=(9.5, 5))
    h = 0.36
    if d_exp and d_cur:
        a2.barh(y+h/1.6, d_exp, h, color="#93c5fd", zorder=3, label="Expected Δ")
        a2.barh(y-h/1.6, d_cur, h, color="#2563eb", zorder=3, label="Actual Δ")
        for yi, de, dc, (_, k) in zip(y, d_exp, d_cur, metrics):
            a2.annotate(f"exp {exp[k]}", (de, yi+h/1.6), va="center", ha="left" if de>=0 else "right",
                        xytext=(5 if de>=0 else -5,0), textcoords="offset points", fontsize=8, color=MUT)
            a2.annotate(f"act {cur[k]}", (dc, yi-h/1.6), va="center", ha="left" if dc>=0 else "right",
                        xytext=(5 if dc>=0 else -5,0), textcoords="offset points", fontsize=8, color=INK)
        a2.legend(frameon=False, loc="lower right", fontsize=9)
        title = f"InBody: Expected vs Actual — {base['date']} → {cur['date']}"
        allv = d_exp + d_cur
    else:
        dd = d_cur or d_exp; who = "Actual" if d_cur else "Expected (prediction)"
        src = cur or exp
        colors = ["#10b981" if (k != "smm" and v <= 0) or (k == "smm" and v >= -0.4) else "#ef4444"
                  for (_, k), v in zip(metrics, dd)]
        a2.barh(y, dd, 0.6, color=colors, zorder=3)
        for yi, dv, (_, k) in zip(y, dd, metrics):
            a2.annotate(f"{base[k]} → {src[k]} ({'+' if dv>0 else ''}{dv})", (dv, yi),
                        va="center", ha="left" if dv>=0 else "right",
                        xytext=(6 if dv>=0 else -6,0), textcoords="offset points", fontsize=9, color=INK)
        title = f"InBody {who} — from {base['date']}"; allv = dd
    a2.axvline(0, color=INK, lw=1)
    a2.set_yticks(y); a2.set_yticklabels(names, fontsize=11)
    a2.set_title(title, fontsize=13, fontweight="bold", loc="left")
    a2.grid(axis="x", color=GRID, lw=1); a2.set_axisbelow(True)
    for s in ("top", "right", "left"): a2.spines[s].set_visible(False)
    pad = max(1.0, max(abs(v) for v in allv) * 2.2)
    a2.set_xlim(-pad, pad)
    fig2.tight_layout()
    out2 = os.path.join(HERE, f"week-{week:02d}-inbody.png")
    fig2.savefig(out2, dpi=150, facecolor="white", bbox_inches="tight"); print("wrote", out2)
else:
    print("inbody expected/current not set — skipping comparison chart")
