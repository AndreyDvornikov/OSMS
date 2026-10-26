from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
from scipy.io import wavfile

ROOT = Path(__file__).resolve().parents[1]
s_rate, samples = wavfile.read(ROOT / "data" / "audio" / "input.wav")
samples = samples + 6000

#sd.play(samples, s_rate)
#sd.wait()
output_path = ROOT / "outputs" / "audio" / "offset.wav"
output_path.parent.mkdir(parents=True, exist_ok=True)
wavfile.write(output_path, s_rate, samples)
