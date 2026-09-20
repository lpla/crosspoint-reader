#!/usr/bin/env python3
"""Replay Settings navigation using an isolated simulator SD card."""
import argparse
import json
import os
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("binary", type=Path)
parser.add_argument("output", type=Path)
parser.add_argument("--language", default="CAV")
parser.add_argument("--theme", type=int, default=1)
args = parser.parse_args()
output = args.output.resolve()
output.mkdir(parents=True, exist_ok=True)
sd = output / "sd"
(sd / ".crosspoint").mkdir(parents=True, exist_ok=True)
(sd / ".crosspoint/settings.json").write_text(json.dumps({"language": args.language, "uiTheme": args.theme}))
script = "1500:LEFT;2200:ENTER;3200:ENTER;4000:ENTER;4800:ENTER;6000:LEFT;7000:LEFT;8000:ENTER;10000:BACK;11500:BACK;12500:LEFT;13500:RIGHT;15500:QUIT"
schedule = [(5500,"system"),(6500,"language-selected"),(7500,"about-selected"),(9000,"about-open"),(10700,"about-return"),(13000,"language-again"),(14500,"tab-return")]
env = dict(os.environ, CROSSPOINT_SIM_SD=str(sd), CROSSPOINT_SIM_INPUT_SCRIPT=script,
           CROSSPOINT_SIM_SCREENSHOTS=";".join(f"{ms}:{output / (name + '.bmp')}" for ms,name in schedule))
with (output / "run.log").open("w") as log:
    subprocess.run([str(args.binary.resolve())], env=env, stdout=log, stderr=subprocess.STDOUT, timeout=25, check=True)
for _,name in schedule:
    subprocess.run(["sips","-s","format","png",str(output / (name + ".bmp")),"--out",str(output / (name + ".png"))], stdout=subprocess.DEVNULL, check=True)
(output / "scenario.json").write_text(json.dumps({"language":args.language,"theme":args.theme,"script":script,"screenshots":schedule},indent=2))
