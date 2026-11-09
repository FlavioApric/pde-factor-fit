"""Baselines for the benchmark: PySINDy (PDE-FIND, Weak, Ensemble, SBR) and PyDMD BOP-DMD.

Each takes gridded u[t, x] and returns a BaselineResult with the recovered operator symbol and
its sympy factors. None of them returns components, weights or a contract label.
"""
from .common import BaselineResult, factor_symbol, structure_of
from .dmd import bopdmd
from .sindy import ensemble_sindy, pdefind, sbr_sindy, weak_sindy

BASELINES = {
    "pdefind": pdefind,
    "weak_sindy": weak_sindy,
    "ensemble_sindy": ensemble_sindy,
    "sbr_sindy": sbr_sindy,
    "bopdmd": bopdmd,
}

__all__ = ["BASELINES", "BaselineResult", "factor_symbol", "structure_of",
           "pdefind", "weak_sindy", "ensemble_sindy", "sbr_sindy", "bopdmd"]
