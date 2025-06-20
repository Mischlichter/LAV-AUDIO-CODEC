#!/usr/bin/env python
# CLI: lav-decode
# Decodes all .lav in examples/audioVECTOR → examples/audioOUTPUT

import os
import sys
import argparse
import soundfile as sf

# allow importing module.py from same folder
sys.path.insert(0, os.path.dirname(__file__))
from module import LAVProcessor

def main():
    examples = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "examples"))
    default_in  = os.path.join(examples, "audioVECTOR")
    default_out = os.path.join(examples, "audioOUTPUT")

    parser = argparse.ArgumentParser(description="Decode LAV files to WAV")
    parser.add_argument("--in",  dest="indir",  default=default_in,  help="Input LAV directory")
    parser.add_argument("--out", dest="outdir", default=default_out, help="Output WAV directory")
    args = parser.parse_args()

    proc = LAVProcessor()
    os.makedirs(args.outdir, exist_ok=True)
    for fname in os.listdir(args.indir):
        if not fname.lower().endswith(".lav"):
            continue
        inpath  = os.path.join(args.indir, fname)
        vecs    = proc.load_lav(inpath)
        wave    = proc.decode_to_array(vecs)
        outname = fname.rsplit(".",1)[0] + ".wav"
        outpath = os.path.join(args.outdir, outname)
        sf.write(outpath, wave, proc.sample_rate)
        print(f"Decoded {fname} → {outname}")

if __name__ == "__main__":
    main()