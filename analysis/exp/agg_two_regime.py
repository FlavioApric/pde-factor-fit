"""S-AGG-CLUSTER: domain grouping on transport (x < pi) | heat (x > pi), exact components as input."""
import time
import numpy as np
from sklearn.metrics import adjusted_rand_score as ari
from pdefactor.synthetic import case
from pdefactor import cluster as CL

tr, he = case("transport"), case("heat")
regions = [(tr, 0.0, np.pi), (he, np.pi, 2 * np.pi)]
for nt_w, nx_w, rel in [(2, 8, 1e-2), (2, 6, 1e-2), (2, 5, 1e-2)]:
    rects = CL.rectangles(2.0, 2 * np.pi, nt_w, nx_w)
    truth = CL.region_truth(rects, regions)
    t0 = time.time()
    wd = CL.window_features(rects, CL.exact_provider(regions), rel_noise=rel, S=6)
    print(f"== {nt_w}x{nx_w} noise {rel} reg={wd.reg:.2g} ({time.time()-t0:.0f}s) global k_eff={wd.glob.k_eff:.2f} DP P(k)={wd.glob.dp.p_k}")
    print("k posterior", {k: round(v, 3) for k, v in CL.k_posterior(wd.F, wd.reg).items()})
    np.set_printoptions(precision=2, suppress=True)
    print(wd.names); print(wd.F)
    print("global", wd.glob.summary())
    for m in ["gmm", "kmeans", "spectral", "agglomerative"]:
        for k in [None, "keff"]:
            lab = CL.cluster_windows(wd, m, k=k)
            print(m, k, "ARI", round(ari(truth, lab), 3), lab, "hole", CL.has_hole(rects, lab))
    # dominant balance on the glued field
    t = np.linspace(0, 2, 96); x = np.linspace(0, 2 * np.pi, 128, endpoint=False)
    TT, XX = np.meshgrid(t, x, indexing="ij")
    u = np.where(XX < np.pi, tr(TT, XX), he(TT, XX))
    u = u + rel * u.std() * np.random.default_rng(0).standard_normal(u.shape)
    lab = CL.dominant_balance_labels(u, t, x, rects)
    print("dominant balance ARI", round(ari(truth, lab), 3), lab, flush=True)
