"""Utilities for tan page: exact map, table builder, highlighter and plot renderer.
This module is intentionally lightweight and importable from Streamlit pages.
"""

import math
from typing import List, Dict, Tuple


exact_map_tan: Dict[int, str] = {
    0: "0",
    15: "2-√3",
    30: "√3/3",
    45: "1",
    60: "√3",
    75: "2+√3",
    90: "undef",
    105: "-(2+√3)",
    120: "-√3",
    135: "-1",
    150: "-√3/3",
    165: "-(2-√3)",
    180: "0",
    195: "2-√3",
    210: "√3/3",
    225: "1",
    240: "√3",
    255: "2+√3",
    270: "undef",
    285: "-(2+√3)",
    300: "-√3",
    315: "-1",
    330: "-√3/3",
    345: "-(2-√3)",
    360: "0",
}


def build_tan_rows(
    step: int = 15, show_radians: bool = True, show_exact: bool = True
) -> Tuple[List[Dict], List[int]]:
    """Return (rows, angles) for the tan table.

    rows: list of dict suitable for pandas.DataFrame
    angles: list of angles used (0..360 step)
    """
    angles = list(range(0, 361, step))
    rows = []
    for deg in angles:
        rad = math.radians(deg)
        c = math.cos(rad)
        if abs(c) < 1e-12:
            tan_num = None
        else:
            tan_num = math.tan(rad)

        if show_exact and deg in exact_map_tan:
            tan_val = exact_map_tan[deg]
        else:
            tan_val = "undef" if tan_num is None else f"{tan_num:.6f}"

        row = {"deg(°)": deg}
        if show_radians:
            row["rad"] = f"{rad:.6f}"
        row["tan(θ)"] = tan_val
        rows.append(row)

    return rows, angles


def highlight_row_func(highlight_angle: int):
    """Return a function suitable for pandas Styler.apply to highlight a row."""
    import streamlit as st

    def _highlight_row(row):
        try:
            deg = int(row.get("deg(°)", -1))
        except Exception:
            return ["" for _ in row]
        try:
            theme_base = st.get_option("theme.base")
        except Exception:
            theme_base = "light"
        highlight_style = (
            "background-color: #fff2a8;"
            if theme_base != "dark"
            else "background-color: rgba(31,119,180,0.25);"
        )
        if deg == int(highlight_angle):
            return [highlight_style for _ in row]
        return ["" for _ in row]

    return _highlight_row


def render_slope_figure(
    highlight_angle: int,
    visual_scale: float = 1.0,
    figsize: Tuple[float, float] = (6, 3),
):
    """Create and return a matplotlib Figure showing y = tan(theta) * x scaled visually.

    Raises ImportError if matplotlib/numpy aren't available.
    """
    try:
        import numpy as np
        import matplotlib.pyplot as plt
    except Exception:
        raise

    fig, ax = plt.subplots(figsize=figsize)
    x_lim = (-2, 2)
    ax.axhline(0, color="#cccccc")
    ax.axvline(0, color="#cccccc")
    ax.set_xlim(x_lim)
    ax.set_ylim(-4, 4)
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    ha = math.radians(highlight_angle)
    try:
        m = math.tan(ha)
    except Exception:
        m = None

    if m is None or abs(math.cos(ha)) < 1e-12:
        ax.text(0, 0, "slope: undef", ha="center", va="center")
    else:
        xs = np.linspace(x_lim[0], x_lim[1], 400)
        ys = m * xs * visual_scale
        ys = np.clip(ys, -100, 100)
        ax.plot(xs, ys, color="#2ca02c", linewidth=2)
        ax.text(
            0.95 * x_lim[1],
            0.9 * ax.get_ylim()[1],
            f"slope = tan({highlight_angle}°) = {m:.3f}",
            ha="right",
        )
        run = 1.0 * visual_scale
        rise = m * visual_scale
        if abs(m) < 50:
            ax.plot([0, run, run], [0, 0, rise], color="#2ca02c", linewidth=2)
            ax.fill([0, run, run], [0, 0, rise], color="#2ca02c", alpha=0.08)

    return fig


__all__ = [
    "exact_map_tan",
    "build_tan_rows",
    "highlight_row_func",
    "render_slope_figure",
]
