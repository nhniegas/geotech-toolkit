"""Checks for logspiral_passive.py. Lengths in m, forces in kN per m of wall."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import logspiral_passive as lp  # noqa: E402


def critical(H, gamma, phi, delta, c, ca):
    """(theta, result at theta, iterations) of the critical wedge."""
    def force(theta):
        return lp.passive_force(theta, H, gamma, phi, delta, c, ca)["Pp"]

    theta, _, iterations = lp.minimise(force, 45.0 + phi / 2.0, [])
    return theta, lp.passive_force(theta, H, gamma, phi, delta, c, ca), iterations


def test_worked_example_of_the_user_guide():
    """README.txt section 4: H 6.1, gamma 17.9, phi 36, delta 20, c 24, ca 24."""
    theta, result, iterations = critical(6.1, 17.9, 36.0, 20.0, 24.0, 24.0)
    assert iterations > 0
    assert theta == pytest.approx(26.45932, abs=1e-4)
    assert result["Pp"] == pytest.approx(3398.05738, rel=1e-6)
    assert result["z"] == pytest.approx(2.30217, abs=1e-4)
    assert result["Kp_eff"] == pytest.approx(10.20347, rel=1e-5)
    assert result["Pp"] == pytest.approx(result["PPI"] + result["PPII"])


def test_smooth_wall_in_sand_gives_the_rankine_force():
    """delta = 0, c = 0: the spiral degenerates to the plane wedge,
    Pp = 0.5 gamma H^2 tan^2(45 + phi/2) = 0.5 x 18 x 25 x 3 = 675 kN/m."""
    _, result, iterations = critical(5.0, 18.0, 30.0, 0.0, 0.0, 0.0)
    assert iterations == 0
    assert result["Pp"] == pytest.approx(675.0, rel=1e-6)


def test_wall_friction_raises_the_passive_force():
    _, smooth, _ = critical(5.0, 18.0, 30.0, 0.0, 0.0, 0.0)
    _, rough, _ = critical(5.0, 18.0, 30.0, 20.0, 0.0, 0.0)
    assert rough["Pp"] > smooth["Pp"]


def test_spiral_sector_area_matches_the_closed_form():
    """A1 = (r1^2 - r0^2) / (4 tan phi) for r = r0 exp(theta tan phi)."""
    result = lp.passive_force(25.0, 6.0, 18.0, 32.0, 15.0, 10.0, 5.0)
    exact = (result["r1"] ** 2 - result["r0"] ** 2) / (4 * math.tan(math.radians(32.0)))
    assert result["A1"] == pytest.approx(exact, rel=1e-9)


def test_parabola_vertex():
    """f = (t - 2)^2 + 1 through t = 1, 2.5, 4: vertex at t = 2."""
    f = [(t - 2) ** 2 + 1 for t in (1.0, 2.5, 4.0)]
    assert lp.parabolic_min(1.0, 2.5, 4.0, *f) == pytest.approx(2.0)
