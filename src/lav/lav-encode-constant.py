#!/usr/bin/env python
# CLI: lav-encode
# Encodes all .wav in examples/audioINPUT → examples/audioVECTOR

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

    parser = argparse.ArgumentParser(description="Encode WAV files to LAV")
    parser.add_argument("--in",    dest="indir",  default=default_in,  help="Input WAV directory")
    parser.add_argument("--out",   dest="outdir", default=default_out, help="Output LAV directory")
    parser.add_argument("--method",dest="method",choices=["savgol","ema"], default="savgol", help="Smoothing method")
    parser.add_argument("--degree",dest="degree",type=int, default=3, help="Spline degree")
    parser.add_argument("--ctrl",  dest="ctrl",  type=int, default=8, help="Control points per segment")
    parser.add_argument("--khz",   dest="khz",   type=float, default=22.05, help="Grid resolution in kHz (default: 22.05)")
    args = parser.parse_args()

    proc = LAVProcessor(
        smooth_method   = args.method,
        spline_degree   = args.degree,
        num_ctrl_points = args.ctrl
    )

    os.makedirs(args.outdir, exist_ok=True)
    for fname in os.listdir(args.indir):
        if not fname.lower().endswith(".wav"):
            continue
        inpath = os.path.join(args.indir, fname)
        sig, sr = sf.read(inpath)
        if sr != proc.sample_rate:
            raise ValueError(f"Expected sample rate {proc.sample_rate}, got {sr}")
        grid_spacing = int(proc.sample_rate / (args.khz * 1000))
        vecs = proc.fit_to_constant_grid(sig, grid_spacing_samples=grid_spacing, degree=args.degree)
        outname = fname.rsplit(".",1)[0] + ".lav"
        outpath = os.path.join(args.outdir, outname)
        proc.save_lav(vecs, outpath)
        print(f"Encoded {fname} → {outname}")

if __name__ == "__main__":
    main()