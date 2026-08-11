# Transparent PNG sleep-overlay QA assets

These files reproduce the transparent PNG follow-up to
[crosspoint-reader#2937](https://github.com/crosspoint-reader/crosspoint-reader/pull/2937).

## Files

- `source-anime-reader-transparent.png`: the original 1086x1448 RGBA overlay used for testing.
- `home-baseline-emulator.png`: the X4 simulator screen before sleeping.
- `fit-overlay-emulator.png`: the same overlay rendered with **Fit** placement (480x640).
- `crop-overlay-emulator.png`: the same overlay rendered with **Crop** placement (480x800).

The source artwork was AI-generated specifically as copyright-safe QA material. It is not based on an identified
character or published work. The screenshots are simulator evidence, not physical-device photographs.

## Reproduce

1. Download `source-anime-reader-transparent.png` and rename it to `sleep-overlay.png` in the SD-card root.
2. Set **Settings > Sleep Screen > Transparent**.
3. Select **Fit** or **Crop** under **Cover Mode**.
4. Return to Home or open a book, then put the device to sleep.

The same file can be placed in `/.sleep-overlay/` or `/sleep-overlay/` when testing random selection. A root
`sleep-overlay.bmp` deliberately takes priority over the PNG.

## Integrity

```text
016daa9bb8dae8f44a29705a74971adf2a3443d13ed16849cf24645da3a45317  source-anime-reader-transparent.png
44213883a5515c8b1147b10391a1b34ca24447d0d4076aed81e97ad6ef0afcd4  home-baseline-emulator.png
5c829d09d646e78cec96fa7203554312330684efcb16b15e352e4a8980fdf682  fit-overlay-emulator.png
9bed8945715b98c7c20b68becf1566462efdc8cac24ca0594338ddb81836cf23  crop-overlay-emulator.png
```
