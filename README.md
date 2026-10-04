# Geotech Toolkit

Geotechnical engineering calculations, run from the terminal. Split out of
[structural-design-toolkit](https://github.com/nhniegas/structural-design-toolkit),
with its history.

| Tool | What it does |
|---|---|
| `logspiral_passive.py` | Passive earth force on a vertical wall with a horizontal backfill by the logarithmic-spiral method (Terzaghi, Peck & Mesri, Art. 32): c-phi soil, wall friction and wall adhesion. Finds the critical wedge angle and reports Pp, its point of application and the equivalent Kp. |

## Running

Python 3.8 or newer, standard library only:

```powershell
python logspiral_passive.py
```

The program asks for the inputs one at a time; see the [user guide](README.txt).
A standalone `LogSpiralPassive.exe` (no Python needed) is attached to each
[GitHub Release](../../releases): push a tag such as `v1.0.0` to build one.

## Tests

```powershell
python -m pip install pytest
python -m pytest tests
```

`tests/test_logspiral_passive.py` checks the worked example of the user guide,
the Rankine limit (delta = 0, c = 0) and the closed-form spiral sector area.
GitHub Actions runs them on every push and pull request to `main`.

## Engineering use

These tools automate calculations; they do not replace engineering judgement.
Check the results independently before using them for design, and read the
limitations in the user guide.

## License

[MIT](LICENSE) © 2026 Nhel Harold Niegas. The software is provided as is, without warranty of any kind.
