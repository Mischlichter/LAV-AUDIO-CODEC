#!/usr/bin/env python
# CLI: lav-radio
# Plays files from examples/audioVECTOR

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from module import LAVProcessor
import argparse
import sounddevice as sd

def main():
    EXAMPLES   = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "examples"))
    DEFAULT_DIR = os.path.join(EXAMPLES, "audioVECTOR")

    parser = argparse.ArgumentParser(description="Play LAV files interactively")
    parser.add_argument("--dir", default=DEFAULT_DIR, help="Folder of .lav files")
    args = parser.parse_args()

    files = [f for f in os.listdir(args.dir) if f.lower().endswith(".lav")]
    for i,f in enumerate(files):
        print(f"{i}: {f}")
    idx  = int(input("Select file index: "))
    path = os.path.join(args.dir, files[idx])

    proc = LAVProcessor()
    vecs = proc.load_lav(path)
    wave = proc.decode_to_array(vecs)
    sd.play(wave, proc.sample_rate)
    sd.wait()

if __name__ == "__main__":
    main()
