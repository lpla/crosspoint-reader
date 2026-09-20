# Settings selection: simulator evidence

Baseline: `8c84ef3268fd56147ae1625e04f773f0f50b7720` (upstream develop).
Fix: `87b9f34b9647375b5e1eb32dd58261b68da099e4`.
Simulator: `6864807` with the same local static-mutex compatibility shim in both runs.
X4 portrait, Valencià; Lyra unless the path says after-round (RoundedRaff).

These are simulator screenshots, not physical e-paper validation. Original PNGs are lossless conversions from simulator BMPs. comparison.png only adds captions and scales those captures to logical size.

Reproduction: Settings → System, focus tab band, Up twice. The focused row is About. Before the fix it is unhighlighted near the bottom, though Confirm opens it. After the fix the viewport moves enough to show its highlight.

The replay script uses isolated SD directories and captures About opening, return, Language selection and return to the tab band. The firmware patch contains only SettingsActivity.cpp and SettingsActivity.h; this separate evidence branch is not intended to be merged.
