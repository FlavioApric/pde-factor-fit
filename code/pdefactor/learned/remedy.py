"""Offline remedy ordering for the controller C (PHASE4_ML_PLAN.md, C).

Within one diagnosis the controller tries remedies in an order. The order is learned *offline* as
the empirical success rate of each remedy on failure-injected simulations (an offline
contextual-bandit estimate, no online exploration). Success counts only when the remedy turns a
wrong output into the right one without adding a false factor on the null set; a remedy that only
changes the likelihood is not in the table at all (honesty rule).

The rate is a Beta(1, 1) posterior mean, and the ordering uses its lower credible bound so that a
remedy seen twice with two successes does not jump ahead of one seen 200 times at 80 %. Remedies
never tried keep the controller's fixed default order after the tried ones' ties.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

import numpy as np

from . import PRIOR_TAG


@dataclass
class RemedyTable:
    default: dict  # diagnosis -> list of remedies in the deterministic fixed order (layer off)
    level: float = 0.10
    tag: str = PRIOR_TAG
    _n: dict = field(default_factory=lambda: defaultdict(int))
    _k: dict = field(default_factory=lambda: defaultdict(int))
    _cost: dict = field(default_factory=lambda: defaultdict(float))

    def record(self, diagnosis, remedy, success, cost=0.0):
        key = (diagnosis, remedy)
        self._n[key] += 1
        self._k[key] += int(bool(success))
        self._cost[key] += float(cost)

    def fit(self, rows):
        """rows: iterable of (diagnosis, remedy, success[, cost])."""
        for r in rows:
            self.record(*r)
        return self

    def rate(self, diagnosis, remedy):
        """(posterior mean, lower bound at `level`) of the success probability."""
        from scipy.stats import beta

        n, k = self._n[(diagnosis, remedy)], self._k[(diagnosis, remedy)]
        a, b = 1 + k, 1 + n - k
        return a / (a + b), float(beta.ppf(self.level, a, b))

    def order(self, diagnosis, per_cost=False):
        """Remedies for `diagnosis`, best first. Off (nothing recorded) = the default order."""
        rems = list(self.default.get(diagnosis, []))
        if not any(self._n[(diagnosis, r)] for r in rems):
            return rems

        costs = [self._cost[(diagnosis, r)] / self._n[(diagnosis, r)] for r in rems
                 if self._n[(diagnosis, r)] and self._cost[(diagnosis, r)] > 0]
        mean_cost = float(np.mean(costs)) if costs else 1.0  # remedies without a recorded cost

        def score(item):
            i, r = item
            n = self._n[(diagnosis, r)]
            if n == 0:
                return (1, 0.0, i)  # untried: after tried ones, in default order
            lb = self.rate(diagnosis, r)[1]
            if per_cost:
                c = self._cost[(diagnosis, r)] / n
                lb /= c if c > 0 else mean_cost
            return (0, -lb, i)

        return [r for _, r in sorted(enumerate(rems), key=score)]
