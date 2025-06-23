import numpy as np
import soundfile as sf
from scipy.signal import argrelextrema, savgol_filter
from scipy.interpolate import make_lsq_spline, BSpline

class LAVProcessor:
    def __init__(self,
                 sample_rate=44100,
                 smooth_method='savgol',
                 smooth_window=15,
                 smooth_poly=3,
                 ema_alpha=0.1,
                 spline_degree=3,
                 num_ctrl_points=8):
        self.sample_rate = sample_rate
        self.smooth_method = smooth_method
        self.smooth_window = smooth_window
        self.smooth_poly = smooth_poly
        self.ema_alpha = ema_alpha
        self.spline_degree = spline_degree
        self.num_ctrl_points = num_ctrl_points

    def smooth(self, signal):
        if self.smooth_method == 'ema':
            alpha = self.ema_alpha
            out = np.empty_like(signal)
            out[0] = signal[0]
            for i in range(1, len(signal)):
                out[i] = alpha * signal[i] + (1 - alpha) * out[i-1]
            return out
        elif self.smooth_method == 'savgol':
            return savgol_filter(signal, self.smooth_window, self.smooth_poly)
        else:
            raise ValueError(f"Unknown smoothing method: {self.smooth_method}")

    def find_turning_points(self, signal):
        maxima = argrelextrema(signal, np.greater)[0]
        minima = argrelextrema(signal, np.less)[0]
        return np.sort(np.concatenate(([0], maxima, minima, [len(signal)-1])))

    def segment_by_turns(self, signal, turning_points):
        return [signal[turning_points[i]:turning_points[i+1]+1] for i in range(len(turning_points)-1)]

    def fit_spline_to_segment(self, segment):
        length = len(segment)
        degree = min(self.spline_degree, max(1, length - 1))
        num_ctrl = min(self.num_ctrl_points, length)
        n_int = num_ctrl - degree + 1
        if n_int < 1:
            n_int = 1

        x = np.linspace(0, 1, length)
        knots = np.concatenate([
            np.zeros(degree),
            np.linspace(0, 1, n_int),
            np.ones(degree)
        ])

        try:
            spline = make_lsq_spline(x, segment, knots, degree)
            return spline.c, spline.t, degree, length
        except Exception:
            degree = 1
            return segment.astype(np.float32), np.array([0.0, 1.0], dtype=np.float32), degree, length

    def encode_from_array(self, signal, sr):
        if sr != self.sample_rate:
            raise ValueError(f"Expected sample rate {self.sample_rate}, got {sr}")
        smoothed = self.smooth(signal)
        turning_points = self.find_turning_points(smoothed)
        segments = self.segment_by_turns(smoothed, turning_points)

        vector_data = []
        for segment in segments:
            coeffs, knots, degree, length = self.fit_spline_to_segment(segment)
            vector_data.append((coeffs, knots, degree, length))
        return vector_data

    def decode_to_array(self, vector_data):
        output = []
        prev_end = None
        for coeffs, knots, degree, length in vector_data:
            try:
                spline = BSpline(knots, coeffs, degree, extrapolate=False)
                t_interp = np.linspace(0, 1, length)
                waveform = spline(t_interp)
                if prev_end is not None:
                    waveform[0] = float(prev_end)
                prev_end = waveform[-1]
                output.append(waveform)
            except Exception:
                continue
        return np.concatenate(output) if output else np.array([], dtype=np.float32)

    def save_lav(self, vector_data, path):
        with open(path, "wb") as f:
            f.write(np.int32(len(vector_data)).tobytes())
            for coeffs, knots, degree, length in vector_data:
                f.write(np.int32(len(coeffs)).tobytes())
                f.write(np.int32(len(knots)).tobytes())
                f.write(np.int32(degree).tobytes())
                f.write(np.int32(length).tobytes())
                f.write(np.asarray(coeffs, dtype=np.float32).tobytes())
                f.write(np.asarray(knots, dtype=np.float32).tobytes())

    def load_lav(self, path):
        vectors = []
        with open(path, "rb") as f:
            segment_count = int(np.frombuffer(f.read(4), dtype=np.int32)[0])
            for _ in range(segment_count):
                len_coeffs = int(np.frombuffer(f.read(4), dtype=np.int32)[0])
                len_knots = int(np.frombuffer(f.read(4), dtype=np.int32)[0])
                degree = int(np.frombuffer(f.read(4), dtype=np.int32)[0])
                length = int(np.frombuffer(f.read(4), dtype=np.int32)[0])
                coeffs = np.frombuffer(f.read(4 * len_coeffs), dtype=np.float32)
                knots = np.frombuffer(f.read(4 * len_knots), dtype=np.float32)
                vectors.append((coeffs, knots, degree, length))
        return vectors

    def fit_to_constant_grid(self, signal, grid_spacing_samples=2, degree=3):
        length = len(signal)
        if length < degree + 1:
            raise ValueError("Signal too short for specified spline degree.")

        # Fixed knot interval in samples
        num_knots = int(length / grid_spacing_samples) + degree * 2
        knot_positions = np.linspace(0, 1, num_knots - degree * 2)
        knots = np.concatenate([
            np.zeros(degree),
            knot_positions,
            np.ones(degree)
        ])

        x = np.linspace(0, 1, length)

        try:
            spline = make_lsq_spline(x, signal, knots, degree)
            coeffs = spline.c
            return [(coeffs, knots, degree, length)]
        except Exception as e:
            # Fall back to linear
            degree = 1
            knots = np.array([0.0, 1.0], dtype=np.float32)
            coeffs = signal.astype(np.float32)
            return [(coeffs, knots, degree, length)]