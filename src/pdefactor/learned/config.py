"""Switches of the S-LEARNED layers (sessions/LEARNED/PLAN.md §2.1).

`run_loop(..., learned=None)` and `run_loop(..., learned=Learned())` are today's pipeline bit for bit
(tests/test_learned_off.py). Each field switches one layer; a layer only proposes candidates, rescales
intervals, sets global constants fitted offline, skips optional steps, or adds report flags. Labels
come from the deterministic evidence only.
"""
from __future__ import annotations

from dataclasses import dataclass

INTERVALS = ("off", "coef", "coef+weights")
HIGHK = ("off", "scan", "scan+net")
CONSTANTS = ("default", "sim-v2")
BUDGET = (False, True, "exact", "fast")  # LB profiles (learned/budget.py PROFILES)
VALIDATOR = (False, True, "downgrade")  # V1: off | report only | report + FIT-COMPATIBLE -> UNDECIDED on a flag


@dataclass(frozen=True)
class Learned:
    intervals: str = "off"          # L2c: "off" | "coef" | "coef+weights"
    highk: str = "off"              # H0/H1: "off" | "scan" | "scan+net"
    constants: str = "default"      # L2d: "default" | "sim-v2" (global calibrated constants file)
    budget: bool | str = False      # LB: False | True (= "exact") | "exact" | "fast" (learned/budget.py)
    prob_calibration: bool = False  # L2b: calibrated P(top) in the report (never a label)
    validator: bool | str = False   # V1: False | True (report only) | "downgrade" (a flagged FIT-COMPATIBLE
                                    # answer becomes UNDECIDED; never an upgrade; P7 user decision 2026-10-31)
    controller: bool = False        # C: targeted reruns under the honesty rule

    def __post_init__(self):
        if self.intervals not in INTERVALS:
            raise ValueError(f"intervals must be one of {INTERVALS}")
        if self.highk not in HIGHK:
            raise ValueError(f"highk must be one of {HIGHK}")
        if self.constants not in CONSTANTS:
            raise ValueError(f"constants must be one of {CONSTANTS}")
        if self.budget not in BUDGET:
            raise ValueError(f"budget must be one of {BUDGET}")
        if self.validator not in VALIDATOR:
            raise ValueError(f"validator must be one of {VALIDATOR}")

    @property
    def any(self):
        return self != OFF


OFF = Learned()


def active(learned):
    """The config to use: None means all layers off."""
    return OFF if learned is None else learned
