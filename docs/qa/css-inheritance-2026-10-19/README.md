# Explicit CSS font inheritance: X4 checks

Candidate: `01575d066`, based on upstream develop `2c09b8ce8`.
Pinned FreeInk SDK: `084fdfb24b16e890844ca5cb44951694ba8d6c56`.

## Reproduce

1. Put `css-inheritance.epub` on the SD card and enable embedded book styles.
2. Open its first chapter. The first two lines should both be bold and italic;
   the next two should both be regular. The first line of each pair is the
   reference; the second uses explicit CSS inheritance.
3. Turn to the second chapter, then back. Reopen the book to check the cached
   path. The long second chapter also exercises partial layout/resume.

The fixture is original generated text and contains no third-party book or art.
`make-css-fixture.py` regenerates it. It deliberately has no navigation table;
the unnamed chapter footer is not the regression being tested.

## Before and after

`before.png` is an X4 framebuffer capture from integration `53329f8f`, whose
relevant CSS parser/chapter parser source matched current develop. It loses the
inherited emphasis while the explicit reference stays correct.

`after.png` is from the standalone default build of this candidate, not the
integration or the private QA controller. Its cache was removed first, and
serial logs confirmed a fresh CSS parse and completed first-page render.
The screenshot command was sent after the passive observation interval.
Both emphasis lines match pixel-for-pixel after normalizing their positions;
the regular lines match before and after. See `check-css-pixels.py`:

```sh
python3 check-css-pixels.py before.png broken
python3 check-css-pixels.py after.png fixed
```

The checker needs Pillow and NumPy. These are framebuffer captures from the
physical X4, not photographs, simulator captures or optical panel calibration.

## Validation

- 30 CSS parser tests and 103 chapter parser tests passed.
- Formatting, diff check and final `pio run -e default` passed.
- Four independent read-only reviews covered the unchanged candidate.
- Standalone default image SHA256:
  `4722a1ea6549a60d13bc3a017b0b54f247e8d834233010c0874603114ac29095`.
- At 10 seconds the standalone synthetic-book run reported 127144 B free,
  68676 B minimum free and 114676 B largest allocation, with no observed panic
  or allocation failure. This is one functional run, not a speed benchmark.
- The current integration plus candidate also passed cold/warm fixture checks,
  paired emphasis/regular pixel comparisons and two chapters of a private real
  EPUB. That integration had the private USB QA controller: its heap values
  are not measurements of vanilla firmware.
- CSS cache version 18 was rebuilt as 19. Completed/partial section readbacks
  carried 64/218; reopening the partial cache resumed its build.

The enums retain their byte-sized storage and the change adds no allocation.
Explicit inherited emphasis can produce more distinct styles in some books;
it is not a claim of reduced heap use. Old CSS/page caches rebuild once.
Reading progress and book metadata formats do not change. Other devices and
human optical inspection are not covered by these automated USB checks.
