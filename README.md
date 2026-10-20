# Localized confirmation screenshots

Evidence for CrossPoint PR4097. Keep this branch: the PR links to its images.
It is an evidence-only branch, not a firmware branch to merge.

These are unedited simulator captures of the production ConfirmationActivity,
using original test filenames. They are not photographs or an end-to-end file
deletion test. No file was deleted and no sleep cover was replaced. Separate
physical X4 validation was reported by the author; these images document only
the simulator component fixture.

## Capture inputs

- Firmware base: ad24aea85c1f9b1a4b2b2e0719ec0dd39020a6b4.
- SDK: f9cc1beda45f4d2d3dade69fc444165727424f53.
- candidate.patch.gz reproduces the production-source changes used for capture:
  the confirmation fix, public ES/CA/Valencian translation coverage and compact
  warning messages. The font-registry change subsequently merged into develop
  is not part of these captures.
- l10n-context-fixture.py is the simulator-only pre-build fixture. It invokes
  the real dialog renderer with long subjects. It does not enter the destructive
  file-operation callbacks and is not included in firmware builds.
- manifest.json preserves the original capture source-diff hash, selected case
  descriptors and pixel hashes, plus the published PNG and fixture file hashes.
- The three selected frames come from a 288-case matrix: four languages, three
  themes, four orientations and six warning/confirmation cases.

## Reproduce

In a separate clean firmware worktree at the base above, initialize the pinned
SDK recursively and apply the patch:

```sh
gzip -dc /path/to/this-evidence/candidate.patch.gz | git apply
```

Configure the macOS native simulator
following its sample, including current SDK compatibility and the archive-tool
fix from simulator PR46. Add this hook under the simulator's extra_scripts:

```ini
pre:/path/to/this-evidence/l10n-context-fixture.py
```

Build the simulator, then run it with a disposable SD directory and these
capture times (in milliseconds). The fixture starts at three seconds:

```sh
CROSSPOINT_CONTEXT_FIXTURE=1 \
CROSSPOINT_SIM_SD=/tmp/confirmation-fixture-sd \
CROSSPOINT_SIM_SCREENSHOTS='62130:/tmp/es-delete.bmp;72530:/tmp/es-sleep.bmp;84530:/tmp/va-landscape.bmp' \
CROSSPOINT_SIM_INPUT_SCRIPT='86000:QUIT' \
.pio/build/simulator/program
```

The portrait images are Spanish deletion (Classic) and sleep-cover confirmation
(RoundedRaff). The landscape image is Valencian sleep-cover confirmation (Lyra).
The host captured at 2x logical resolution; the published PNGs preserve those
pixels without cropping, rescaling or text overlays.
