# Font-browser UX checks

These are native simulator screenshots of the X4 layout, not photographs of a physical device. Catalog and font responses were replayed from the real published catalog/assets.

Before: upstream develop `ad53eb645f27b76c8c4594fafe58479932234bf2`, SDK `946e6ac3d7a9d590ba3224428e6183d55ac7917c`.

After: the local font-browser navigation candidate, diff SHA-256 `0f379aa3a3174f428521a3ea6b339a9ec2bc0ebccb720074e96b5ddcec0c3d5e`. Human X4 validation remains pending. These screenshots do not claim that the fix is merged or included in an RC.

## Scrolling

Open Settings > Reader > Manage Fonts, connect, choose All Fonts, then press Down eleven times from Download All.

- Before: the selected font is outside the displayed rows, so there is no highlight.
- After: the same input sequence scrolls the selected font into view.

The upstream failure also reproduces in full-reader ESP32-C3 QEMU with real guest navigation/layout and substituted board/transport boundaries.

## Installation acknowledgment

Install Alef, then press and release Confirm once on Font installed.

- Before: the same gesture opens the Delete confirmation. No second press was made.
- After: the font list stays open, with Alef marked Installed.

If reproducing the original behavior, cancel the unexpected Delete prompt; do not confirm it.

## Other checks

Held scrolling passed in four explicitly forced renderer orientations, using English, Spanish, Catalan and Valencian across Classic, Lyra and RoundedRaff themes. Catalogue Retry recovered after a forced initial error. Short Confirm, held Confirm and Back acknowledgments were checked. A failed font-file transfer followed by Retry recovered after the valid response was restored.

Font-update data loss (existing issue 2918) is a separate problem and is not fixed by this navigation candidate.
