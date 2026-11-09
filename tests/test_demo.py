"""The documented quick start must keep working."""
from pdefactor import demo


def test_demo_runs(capsys):
    demo.main(["transport_plus_diffusion", "--noise", "0.05"])
    out = capsys.readouterr().out
    assert "FIT-COMPATIBLE" in out and "recovered equation" in out


def test_demo_list(capsys):
    demo.main(["--list"])
    assert "heat" in capsys.readouterr().out
