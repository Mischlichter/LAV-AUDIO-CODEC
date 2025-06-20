# LAV Audio Codec

A high-fidelity, temporally-precise audio format and toolkit for encoding and decoding audio as **Latent Audio Vectors** (`.lav`), plus a simple playback CLI.

## Overview

LAV transforms raw waveforms into sequences of dynamically-fitted B-spline segments, capturing the geometric structure of sound with perfect temporal integrity. It is ideal for:

- **Neural audio pipelines** (tokenizers, transformers, generative models)
- **Real-time streaming** (low-latency, chunk-based processing)
- **Compact storage** (binary `.lav` files storing spline parameters)
- **High-fidelity reconstruction** back to PCM audio

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
audio-lav/
├── LICENSE
├── README.md
├── requirements.txt
├── examples/
│   ├── audioINPUT/             # Place source .wav files here
│   ├── audioVECTOR/            # Encoded .lav outputs
│   └── audioOUTPUT/            # Decoded .wav outputs
└── src/
    └── lav/
        ├── __init__.py
        ├── LAV_module.py       # Core LAVProcessor class
        ├── encode.py           # CLI: `lav-encode`
        ├── decode.py           # CLI: `lav-decode`
        └── radio.py            # CLI: `lav-radio`
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
lav-radio --dir examples/audioVECTOR
```

- Lists all `.lav` files and plays the selected one at 44.1 kHz.

## Configuration

Adjust any default behavior via CLI flags or by instantiating `LAVProcessor` in code:

```python
from lav.LAV_module import LAVProcessor
proc = LAVProcessor(
    smooth_method='ema',
    smooth_window=21,
    smooth_poly=2,
    ema_alpha=0.2,
    spline_degree=4,
    num_ctrl_points=12
)
```

## Development & Contribution

- Add tests under a `tests/` directory.  
- Use `pytest` for testing.  
- Update `setup.py` / `pyproject.toml` and bump version before release.  
- Open issues or pull requests on GitHub.

---
