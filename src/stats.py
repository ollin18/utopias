import numpy as np
import pandas as pd
from scipy import stats
from numpy.linalg import lstsq

# ======================
# Correlations with permutation p and bootstrap CI
# ======================

def permutation_pearson(x, y, n_perm: int = 10_000, seed: int = 20240711):
    """Pearson r with a two-sided permutation p-value.
    """
    x, y = np.asarray(x, float), np.asarray(y, float)
    mask = np.isfinite(x) & np.isfinite(y)
    x, y = x[mask], y[mask]
    if len(x) < 4:
        return np.nan, np.nan
    rng = np.random.default_rng(seed)
    r_obs, _ = stats.pearsonr(x, y)
    null = np.array([stats.pearsonr(rng.permutation(x), y)[0] for _ in range(n_perm)])
    return r_obs, (np.abs(null) >= np.abs(r_obs)).mean()


def bootstrap_r(x, y, n_boot: int = 5_000, ci: float = 0.95, seed: int = 20240712):
    """Pearson r with a bootstrap confidence interval."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    mask = np.isfinite(x) & np.isfinite(y)
    x, y = x[mask], y[mask]
    if len(x) < 4:
        return np.nan, np.nan, np.nan
    rng = np.random.default_rng(seed)
    obs, _ = stats.pearsonr(x, y)
    boots = []
    for _ in range(n_boot):
        idx = rng.integers(0, len(x), len(x))
        if np.std(x[idx]) == 0 or np.std(y[idx]) == 0:
            continue
        boots.append(stats.pearsonr(x[idx], y[idx])[0])
    lo = np.nanpercentile(boots, (1 - ci) / 2 * 100)
    hi = np.nanpercentile(boots, (1 - (1 - ci) / 2) * 100)
    return obs, lo, hi


def partial_pearson(x, y, z):
    """Partial Pearson correlation of x, y controlling for z (linear residuals)."""
    x, y, z = np.asarray(x, float), np.asarray(y, float), np.asarray(z, float)
    ex = x - np.polyval(np.polyfit(z, x, 1), z)
    ey = y - np.polyval(np.polyfit(z, y, 1), z)
    return stats.pearsonr(ex, ey)


def sig_stars(p) -> str:
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""


# ======================
# Reporting helpers
# ======================

def correlate(m: pd.DataFrame, x: str, y: str, logy: bool = False):
    """r, p and 95% CI for a single pair, log10-ing the outcome when skewed."""
    d = m.dropna(subset=[x, y])
    yv = np.log10(d[y].clip(lower=1)) if logy else d[y]
    r, p = permutation_pearson(d[x], yv)
    _, lo, hi = bootstrap_r(d[x], yv)
    return dict(r=round(float(r), 3), p=round(float(p), 3),
                ci=[round(float(lo), 3), round(float(hi), 3)], n=int(len(d)))


def correlation_table(m: pd.DataFrame, pairs) -> pd.DataFrame:
    """Build the headline correlation table from a list of (x, y, label, logy)."""
    rows = []
    for x, y, name, logy in pairs:
        s = correlate(m, x, y, logy=logy)
        rows.append(dict(pair=name, r=s["r"], p=s["p"],
                         ci_low=s["ci"][0], ci_high=s["ci"][1]))
    return pd.DataFrame(rows)


def standardized_regression(m: pd.DataFrame):
    """Standardised regression of log10 visitors on the three z-scored axes."""
    lv = np.log10(m["n_unique_visitors"])
    X = np.column_stack([stats.zscore(m[c]) for c in ["transit_z", "services_z", "crime_z"]])
    X = np.column_stack([np.ones(len(m)), X])
    y = stats.zscore(lv)
    beta, *_ = lstsq(X, y, rcond=None)
    yhat = X @ beta
    r2 = 1 - np.sum((y - yhat) ** 2) / np.sum((y - y.mean()) ** 2)
    return dict(transit=round(float(beta[1]), 3), services=round(float(beta[2]), 3),
                crime=round(float(beta[3]), 3), R2=round(float(r2), 3))


def partial_axes(m: pd.DataFrame) -> pd.DataFrame:
    """Zero-order and partial correlation of each axis with log10 visitors."""
    lv = np.log10(m["n_unique_visitors"])
    axes = ["transit_z", "services_z", "crime_z"]
    rows = []
    for axis in axes:
        ctrl = m[[a for a in axes if a != axis]].mean(axis=1)
        r0, p0 = stats.pearsonr(m[axis], lv)
        rp, pp = partial_pearson(m[axis].values, lv.values, ctrl.values)
        rows.append(dict(axis=axis.replace("_z", ""), r_zero=round(float(r0), 3),
                         p_zero=round(float(p0), 3), r_partial=round(float(rp), 3),
                         p_partial=round(float(pp), 3)))
    return pd.DataFrame(rows)
