"""Step 1 (interpolation with probabilities): GP posterior samples, deep-ensemble ablation,
factor-wise EPGP prior, and the bridge to the core (run_core_on_samples)."""
from .gp import GPPosterior, fit_gp, smoother
from .core_bridge import bench_interpolator, factor_set_posterior, run_core_on_samples
