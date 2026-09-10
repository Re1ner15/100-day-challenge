#!/usr/bin/env python3
"""Week 1 dashboard (Days 1-4, Mon 7 - Thu 10 Sep). Regenerate: python3 make_week1.py"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

days   = ["Mon\nPush", "Tue\nWalk", "Wed\nPull", "Thu\nCardio"]
kcal   = [2005, 1965, 2050, 1759]
protein= [156, 140, 145, 155]
carbs  = [103, 156, 156, 102]
fat    = [102, 79, 38, 78]
active = [540, 585, 1003, 199]          # logged active kcal (workouts + walks)

TDEE, KCAL_TARGET, PROT_FLOOR = 2700, 1750, 160

# palette (accessible, consistent)
C_KCAL, C_PROT, C_CARB, C_FAT, C_ACT = "#3b82f6", "#10b981", "#f59e0b", "#8b5cf6", "#ef4444"
GRID = "#e5e7eb"; INK = "#111827"; MUT = "#6b7280"
x = np.arange(len(days))

plt.rcParams.update({"font.size": 11, "axes.edgecolor": GRID, "axes.linewidth": 1,
                     "text.color": INK, "axes.labelcolor": INK,
                     "xtick.color": MUT, "ytick.color": MUT})

fig, ax = plt.subplots(2, 2, figsize=(11, 8.2))
fig.suptitle("100-Day Challenge — Week 1 (Mon 7 – Thu 10 Sep)", fontsize=16, fontweight="bold", y=0.98)

def style(a):
    a.grid(axis="y", color=GRID, lw=1); a.set_axisbelow(True)
    for s in ("top", "right"): a.spines[s].set_visible(False)
    a.set_xticks(x); a.set_xticklabels(days)

def labels(a, vals, fmt="{:.0f}", dy=3):
    for xi, v in zip(x, vals):
        a.annotate(fmt.format(v), (xi, v), ha="center", va="bottom",
                   xytext=(0, dy), textcoords="offset points", fontsize=9, color=INK)

# 1 — Calories vs TDEE
a = ax[0, 0]
a.bar(x, kcal, color=C_KCAL, width=0.6, zorder=3); labels(a, kcal)
a.axhline(TDEE, color=C_ACT, ls="--", lw=1.5, zorder=2)
a.axhline(KCAL_TARGET, color=MUT, ls=":", lw=1.5, zorder=2)
a.text(-0.4, TDEE+40, "TDEE ~2700", ha="left", color=C_ACT, fontsize=9)
a.text(-0.4, KCAL_TARGET+40, "target ~1750", ha="left", color=MUT, fontsize=9)
a.set_title("Calories eaten vs TDEE", fontweight="bold", loc="left")
a.set_ylim(0, 3000); style(a)

# 2 — Protein vs floor
a = ax[0, 1]
a.bar(x, protein, color=C_PROT, width=0.6, zorder=3); labels(a, protein)
a.axhline(PROT_FLOOR, color=C_ACT, ls="--", lw=1.5, zorder=2)
a.text(-0.4, PROT_FLOOR+4, "floor 160 g", ha="left", color=C_ACT, fontsize=9)
a.set_title("Protein (g)  —  the muscle guardian", fontweight="bold", loc="left")
a.set_ylim(0, 190); style(a)

# 3 — Macros grouped
a = ax[1, 0]; w = 0.26
a.bar(x-w, protein, w, label="Protein", color=C_PROT, zorder=3)
a.bar(x,   carbs,   w, label="Carbs",   color=C_CARB, zorder=3)
a.bar(x+w, fat,     w, label="Fat",     color=C_FAT,  zorder=3)
a.set_title("Macros per day (g)", fontweight="bold", loc="left")
a.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.02), fontsize=9)
a.set_ylim(0, 190); style(a)

# 4 — Active calories
a = ax[1, 1]
a.bar(x, active, color=C_ACT, width=0.6, zorder=3); labels(a, active)
a.set_title("Active calories burned (workouts + walks)", fontweight="bold", loc="left")
a.annotate("3 sessions\n(Pull+cardio+walk)", (2, 1003), ha="center", va="bottom",
           xytext=(0, 24), textcoords="offset points", fontsize=8, color=MUT)
a.set_ylim(0, 1250); style(a)

fig.tight_layout(rect=[0, 0.01, 1, 0.95])
fig.savefig("week-1.png", dpi=150, facecolor="white", bbox_inches="tight")
print("wrote week-1.png")
