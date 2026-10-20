# Localization and UI regression evidence

The screenshots in this directory are framebuffer captures from a USB-connected
Xteink X4, not simulator output or photographs of the e-paper panel. The text is
synthetic test input; no saved password or private book appears in these images.
Pixel contents are unretouched.

## Controlled device comparison

Source: CrossPoint develop `e78f09fd1e2e1c9a7a9fb6cec28ee84cfdb53722`, official
translation baseline `7cd9d9bee5848db4d7dd1d3e7a7e195f99a41931`, and FreeInk SDK
`f9cc1beda45f4d2d3dade69fc444165727424f53`.

Both device builds have identical private diagnostic scaffolding and wording.
The baseline reverts only the cache-dialog and password-mask C++ fixes. This
isolates the two bugs; it is not a heap or performance comparison with release
firmware. The later small-font replacement is not in these device images.

Candidate QA binary SHA-256:
`d660e8c3d0205e80e354e0a34eed2225fc054908e299429b341bbd81e75ffa02`.
Baseline QA binary SHA-256:
`3b99faa45e08d8394068e1bb684b166f4b28beead1264d34328c64c65f78cf69`.

The full run produced 112 candidate and six baseline captures. Only selected
examples are published here. It covered EN/ES/CA/Valencian, Classic/Lyra/
RoundedRaff, targeted four-orientation layout stress, and real USB-injected
button routing. Non-portrait keyboard/settings states were forced layout
fixtures, not evidence of normal routes into those screens.

Cache Cancel/Back preserved disposable progress, including after a following
Confirm. Explicit Clear removed the disposable book cache but left unrelated
files intact. Original user data was isolated before these tests and restored
afterward. No touch-panel or optical inspection is claimed for this button-only
X4. Three repeated-transition heap checkpoints were stable; this does not prove
absence of all leaks or establish end-user performance.

Sync-ready and recovery screenshots use the production render methods in
selected initial states. They do not test real authentication or firmware writes.
Battery readings may differ between captures; they are not battery measurements.

## Source-method checks

With a full repository checkout containing the baseline commit, Python 3 and a
C++17 compiler with AddressSanitizer/UndefinedBehaviorSanitizer support:

```sh
python3 check-password-mask.py /path/to/crosspoint-reader
python3 check-cache-dismissal.py /path/to/crosspoint-reader
```

Each script extracts the actual method bodies from the historical baseline and
the working tree, then compiles them into a controlled harness in a temporary
directory. The expected baseline failures demonstrate the regression; a fixed
working tree must pass the corresponding check. Run both scripts only after both
fixes are present; each PR intentionally changes just one of the two paths.
These are source-level checks, not whole-firmware
sanitizer runs. The popup harness models outcomes; it is not a physical touch test.

The password check covers 336 combinations including ASCII, 2/3/4-byte code
points, valid cursor boundaries, hidden/visible/cursor states and text/URL modes.
The cache check covers eight Cancel/Back/outside-dismissal/subsequent-Confirm/
explicit-Clear/idle assertions.

`screenshots.json` records the exact SHA-256 of each published PNG. There are no
device backups, private books, credentials, raw serial logs or QA firmware here.

## Current-font simulator refresh

After the device run, upstream replaced the small UI font with Ubuntu. The
files prefixed `current-font-native-` are explicitly separate native simulator
captures, not additional X4 captures. Their source is develop
`471243b2df886cb3f18474954ceac41a90a2a273` plus the approved fixes and translation
baseline, using the same pinned SDK. The translation values match current
`chore/update-translations` plus the 16 proposed edits.

The fresh run completed 387 cases and 128 captures. Across 12,560 font-width
measurements, the 71 audited fixed-line call sites had no over-width result;
the recorded draw calls had no clip-boundary findings or invalid UTF-8.
This is not a proof about every possible dynamic string or every device panel.
`current-font-summary.json` records the source/binary identity and results.
