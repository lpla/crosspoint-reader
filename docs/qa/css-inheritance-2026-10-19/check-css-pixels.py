from pathlib import Path
import json
import sys
import numpy as np
from PIL import Image

out = Path(__file__).resolve().parent
name, expected = sys.argv[1], sys.argv[2] == 'fixed'
image = np.asarray(Image.open(out / name).convert('L'))[:700] < 128
ys = np.where(image.any(axis=1))[0]
groups = np.split(ys, np.where(np.diff(ys) > 5)[0] + 1)
assert len(groups) == 5, [(int(g[0]), int(g[-1])) for g in groups]
lines = []
for group in groups:
    line = image[group[0]:group[-1] + 1]
    xs = np.where(line.any(axis=0))[0]
    lines.append(line[:, xs[0]:xs[-1] + 1])
emphasis = np.array_equal(lines[0], lines[1])
regular = np.array_equal(lines[2], lines[3])
assert emphasis == expected and regular, (emphasis, regular)
result = dict(image=name, emphasis_matches_reference=emphasis,
              regular_matches_reference=regular, fixed_expected=expected)
(out / (Path(name).stem + '-pixels.json')).write_text(json.dumps(result, indent=2))
print(json.dumps(result))
