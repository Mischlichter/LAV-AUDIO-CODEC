![LAV Banner](https://github.com/Mischlichter/LAV-AUDIO-CODEC/raw/main/banner.png)

# LAV Audio Codec

A Near-Hi-Fi, temporally-precise audio format and toolkit for encoding and decoding audio as **Latent Audio Vectors** (`.lav`), plus a simple playback CLI.

## Overview

LAV transforms raw waveforms into sequences of dynamically-fitted B-spline segments, capturing the geometric structure of sound with perfect temporal integrity. It is ideal for:

- **Neural audio pipelines** (tokenizers, transformers, generative models)
- **Real-time streaming** (low-latency, chunk-based processing)
- **Compact storage** (binary `.lav` files storing spline parameters)
- **Near-Hi-Fi, reconstruction** back to PCM audio

## Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourname/audio-lav.git
   cd audio-lav
   ```

2. **Create & activate a virtual environment**  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # macOS/Linux
   .venv\Scripts\activate.bat     # Windows
   ```

3. **Install dependencies**  
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Directory Structure

```
LAV-AUDIO-CODEC/
├── LICENSE
├── LAV-CODEC-INFO.txt
├── README.md
├── requirements.txt
├── examples/
│   ├── audioINPUT/            # source .wav files
│   ├── audioVECTOR/           # encoded .lav files
│   └── audioOUTPUT/           # decoded .wav files
└── src/
    └── lav/
        ├── __init__.py
        ├── lav-encode.py          # CLI: lav-encode
        ├── lav-decode.py          # CLI: lav-decode
        ├── lav-player.py          # CLI: lav-radio
        └── module.py          # LAVProcessor core
```

## CLI Usage

### 1. Encode WAV → LAV

```bash
lav-encode \
  --in examples/audioINPUT \
  --out examples/audioVECTOR \
  --method savgol \
  --degree 3 \
  --ctrl 8
```

- `--in`: WAV input directory (default: `examples/audioINPUT`)  
- `--out`: LAV output directory (default: `examples/audioVECTOR`)  
- `--method`: smoothing method (`savgol` or `ema`)  
- `--degree`: maximum spline degree  
- `--ctrl`: maximum control points per segment  

### 2. Decode LAV → WAV

```bash
lav-decode \
  --in examples/audioVECTOR \
  --out examples/audioOUTPUT
```

- `--in`: LAV input directory (default: `examples/audioVECTOR`)  
- `--out`: WAV output directory (default: `examples/audioOUTPUT`)  

### 3. Interactive Playback

```bash
lav-player --dir examples/audioVECTOR
```

- Lists all `.lav` files and plays the selected one at 44.1 kHz.

## Configuration

Adjust any default behavior via CLI flags or by instantiating `LAVProcessor` in code:

```python
from lav.module import LAVProcessor
proc = LAVProcessor(
    smooth_method='ema',
    smooth_window=21,
    smooth_poly=2,
    ema_alpha=0.2,
    spline_degree=4,
    num_ctrl_points=12
)
```

### 4. Encode WAV → LAV (Fixed Knot Grid)

```bash
lav-encode-constant \
  --in examples/audioINPUT \
  --out examples/audioVECTOR \
  --hz 11025 \
  --method savgol \
  --degree 3 \
  --ctrl 8
```

- `--in`: WAV input directory  
- `--out`: Output `.lav` vector directory  
- `--hz`: Target evaluation grid frequency (e.g. `11025` for 1/4 of 44.1kHz)  
- `--method`: smoothing method (`savgol` or `ema`)  
- `--degree`: maximum spline degree  
- `--ctrl`: maximum control points per segment  

> This encoder outputs `.lav` files with **uniform temporal spacing between knot samples** – ideal for vector operations like crossfading or morphing.

## Configuration

Adjust any default behavior via CLI flags or by instantiating `LAVProcessor` in code:

```python
from lav.module import LAVProcessor
proc = LAVProcessor(
    smooth_method='ema',
    smooth_window=21,
    smooth_poly=2,
    ema_alpha=0.2,
    spline_degree=4,
    num_ctrl_points=12
)
```