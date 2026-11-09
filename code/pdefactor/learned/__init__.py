"""Phase 4 learned layers (analysis/PHASE4_ML_PLAN.md). Every layer here is optional and off by
default: its output is a proposal (scored afterwards by the exact evidence), a calibration fitted
offline on a declared simulator prior (tagged PRIOR_TAG), or a flag. None changes a label.

- expsum:     generic damped exponential sums (training data for L0; PDE-agnostic by R2-T6).
- expseeds:   L0, learned pole-set proposals for the per-bin order comparison (needs torch).
- calibrate:  L2b/L2c, isotonic and monotone recalibration, loss-derived thresholds, conformal.
- validator:  V1, multi-label failure-mode combiner on V0 statistics, risk control, OOD gate.
- remedy:     offline remedy ordering for the controller C.
"""

PRIOR_TAG = "prior: sim-v1"
