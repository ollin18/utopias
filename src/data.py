import numpy as np
import pandas as pd

# ======================
# Loading
# ======================

def load_summary(path: str = "data/utopias_summary.csv") -> pd.DataFrame:
    """Per-site table, sorted by unique visitors (descending)."""
    m = pd.read_csv(path)
    return m.sort_values("n_unique_visitors", ascending=False).reset_index(drop=True)


def load_items(path: str = "data/service_items.csv") -> pd.DataFrame:
    """Long catalog of facilities: one row per site and facility."""
    return pd.read_csv(path)


# ======================
# Rescaling
# ======================

def zscore(s) -> pd.Series:
    s = pd.Series(s, dtype=float)
    return (s - s.mean()) / s.std(ddof=0)


def minmax(s) -> pd.Series:
    s = pd.Series(s, dtype=float)
    rng = s.max() - s.min()
    return (s - s.min()) / rng if rng > 0 else s * 0


# ======================
# The three axes and the composite
# ======================

def build_axes(m: pd.DataFrame) -> pd.DataFrame:
    """Standardised service, transit and crime axes and the equal-weight composite.

    Services axis averages distinctiveness and facility count; transit is the
    standardised transit score alone (it already folds in routes, trips, metro,
    BRT and modes); crime averages density and violent share. The composite
    subtracts crime so higher always means better reach.
    """
    m = m.copy()
    m["services_z"] = (zscore(m["distinctiveness_index"]) + zscore(m["n_facilities"])) / 2
    m["transit_z"] = zscore(m["transit_score"])
    m["crime_z"] = (zscore(m["crime_per_km2"]) + zscore(m["violent_share"])) / 2
    m["composite_score"] = (m["services_z"] + m["transit_z"] - m["crime_z"]) / 3
    return m


def domain_counts(items: pd.DataFrame, sites) -> pd.DataFrame:
    """Distinct facility categories each site offers, by service domain."""
    tab = (items.groupby(["name", "domain"])["clean_category"].nunique()
           .unstack(fill_value=0))
    return tab.reindex(sites).fillna(0)
