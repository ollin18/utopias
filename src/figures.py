import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from scipy import stats

from stats import permutation_pearson, sig_stars

PALETTE = {
    "atzintli": "#4E79A7", "barco": "#F28E2B", "cuauhtlicalli": "#E15759",
    "la_cascada": "#76B7B2", "libertad": "#59A14F", "meyehualco": "#EDC948",
    "olini": "#B07AA1", "papalotl": "#FF9DA7", "quetzalcoatl": "#9C755F",
    "tecoloxtitlan": "#7F7F7F", "teotongo": "#D37295", "tezontli": "#A0CBE8",
    "ixtapalcalli": "#86BCB6",
}
ACCENT = "#7B4FA3"
RNG = np.random.default_rng(42)


def style():
    plt.rcParams.update({
        "figure.dpi": 120, "savefig.dpi": 300, "font.family": "DejaVu Sans",
        "axes.spines.top": False, "axes.spines.right": False,
        "font.size": 20, "axes.titlesize": 23, "axes.labelsize": 21,
        "xtick.labelsize": 19, "ytick.labelsize": 19, "legend.fontsize": 19,
        "lines.linewidth": 2.4, "lines.markersize": 9, "axes.titleweight": "bold",
    })


def label(name: str) -> str:
    return name.replace("_", " ").title()


def save(fig, name: str, outdir: str = "figs"):
    os.makedirs(outdir, exist_ok=True)
    fig.savefig(f"{outdir}/{name}.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def statbox(ax, text, loc="upper left"):
    x, ha = (0.03, "left") if "left" in loc else (0.97, "right")
    y, va = (0.97, "top") if "upper" in loc else (0.03, "bottom")
    ax.text(x, y, text, transform=ax.transAxes, ha=ha, va=va, fontsize=18,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="0.6", lw=1.1), zorder=20)


# ======================
# Panels
# ======================

def scatter_fit(m, x, y, xlabel, ylabel, name, logy=False, xerr=None,
                statloc="upper left", outdir="figs"):
    """Site scatter with a bootstrapped least-squares band; r matches the plotted values."""
    fig, ax = plt.subplots(figsize=(7.4, 6.2))
    d = m.dropna(subset=[x, y]).copy()
    yv = np.log10(d[y].clip(lower=1)) if logy else d[y]
    r, p = permutation_pearson(d[x], yv)
    for _, row in d.iterrows():
        yy = np.log10(max(row[y], 1)) if logy else row[y]
        c = PALETTE.get(row["utopia_name"], "gray")
        if xerr is not None and np.isfinite(row.get(xerr, np.nan)):
            ax.errorbar(row[x], yy, xerr=row[xerr], fmt="none", ecolor="0.6",
                        elinewidth=1.3, capsize=3, zorder=4)
        ax.scatter(row[x], yy, s=185, color=c, edgecolor="white", lw=1.3, zorder=5)
        ax.annotate(label(row["utopia_name"]), (row[x], yy), textcoords="offset points",
                    xytext=(7, 5), fontsize=15.5, color="#222222",
                    path_effects=[pe.withStroke(linewidth=2.6, foreground="white")])
    sl, ic, *_ = stats.linregress(d[x].astype(float), yv.astype(float))
    xs = np.linspace(d[x].min(), d[x].max(), 100)
    boots = []
    for _ in range(1000):
        idx = RNG.integers(0, len(d), len(d))
        s2, i2, *_ = stats.linregress(d[x].values[idx].astype(float), yv.values[idx].astype(float))
        boots.append(s2 * xs + i2)
    boots = np.array(boots)
    ax.fill_between(xs, np.percentile(boots, 2.5, 0), np.percentile(boots, 97.5, 0),
                    color=ACCENT, alpha=0.13, zorder=2)
    ax.plot(xs, sl * xs + ic, color=ACCENT, lw=2.6, zorder=3)
    statbox(ax, f"$r$ = {r:+.2f}{sig_stars(p)}\n$p$ = {p:.3f}", loc=statloc)
    if logy:
        lo_e, hi_e = int(np.floor(np.log10(max(d[y].min(), 1)))), int(np.ceil(np.log10(d[y].max())))
        ax.set_yticks(range(lo_e, hi_e + 1))
        ax.set_yticklabels([f"$10^{{{k}}}$" for k in range(lo_e, hi_e + 1)])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.18)
    save(fig, name, outdir)
    return r, p


def barh_sites(values, xlabel, name, order=None, logx=False, fmt="{:.0f}", outdir="figs"):
    s = values.dropna()
    s = s.sort_values() if order is None else s.reindex(order)
    fig, ax = plt.subplots(figsize=(7.4, 6.6))
    ax.barh(range(len(s)), s.values, color=[PALETTE.get(n, "gray") for n in s.index],
            edgecolor="white", lw=0.8)
    ax.set_yticks(range(len(s)))
    ax.set_yticklabels([label(n) for n in s.index])
    if logx:
        ax.set_xscale("log")
    for i, v in enumerate(s.values):
        ax.text(v, i, "  " + fmt.format(v), va="center", ha="left", fontsize=12.5)
    ax.set_xlabel(xlabel)
    ax.grid(axis="x", alpha=0.18)
    save(fig, name, outdir)


def corr_heatmap(m, predictors, outcomes, name, logy_cols=(), outdir="figs"):
    """Grid of Pearson r between predictor columns and visit outcomes, starred by p."""
    pk, pl = zip(*predictors)
    ok, ol = zip(*outcomes)
    R = np.full((len(pk), len(ok)), np.nan)
    star = np.empty_like(R, dtype=object)
    for i, xc in enumerate(pk):
        for j, yc in enumerate(ok):
            yv = np.log10(m[yc].clip(lower=1)) if yc in logy_cols else m[yc]
            r, p = permutation_pearson(m[xc], yv)
            R[i, j], star[i, j] = r, sig_stars(p)
    fig, ax = plt.subplots(figsize=(1.35 * len(ok) + 3, 0.62 * len(pk) + 2))
    im = ax.imshow(R, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
    ax.set_xticks(range(len(ok)))
    ax.set_xticklabels(ol, rotation=40, ha="right", fontsize=15)
    ax.set_yticks(range(len(pk)))
    ax.set_yticklabels(pl, fontsize=15)
    for i in range(len(pk)):
        for j in range(len(ok)):
            ax.text(j, i, f"{R[i, j]:+.2f}{star[i, j]}", ha="center", va="center",
                    fontsize=12.5, color="black" if abs(R[i, j]) < 0.6 else "white")
    fig.colorbar(im, ax=ax, fraction=0.026, pad=0.02).set_label("Pearson $r$", fontsize=16)
    save(fig, name, outdir)


def typology_plot(m, name, outdir="figs"):
    """Transit against distinctiveness, sized by visitors, coloured by the four types."""
    tcol = {"Flagship destinations": "#B07AA1", "Connected neighborhood hubs": "#4E79A7",
            "Under-connected attractions": "#F28E2B", "Neighborhood spaces": "#59A14F"}
    fig, ax = plt.subplots(figsize=(8.6, 7.4))
    xm, ym = m["transit_score"].median(), m["distinctiveness_index"].median()
    ax.axvline(xm, color="0.7", ls="--", lw=1.4)
    ax.axhline(ym, color="0.7", ls="--", lw=1.4)
    for _, r in m.iterrows():
        c = tcol.get(str(r.get("typology", "")), "gray")
        sz = 120 + 900 * np.sqrt(r["n_unique_visitors"] / m["n_unique_visitors"].max())
        ax.scatter(r["transit_score"], r["distinctiveness_index"], s=sz, color=c,
                   edgecolor="white", lw=1.4, alpha=0.9, zorder=5)
        ax.annotate(label(r["utopia_name"]), (r["transit_score"], r["distinctiveness_index"]),
                    textcoords="offset points", xytext=(7, 5), fontsize=13, color="#222222",
                    path_effects=[pe.withStroke(linewidth=2.6, foreground="white")])
    ax.set_xlabel("Transit accessibility score")
    ax.set_ylabel("Service distinctiveness index")
    ax.grid(alpha=0.18)
    save(fig, name, outdir)
