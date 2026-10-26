import numpy as np
import sounddevice as sd

note = {
    "D5": 587.33,
    "B4": 493.88,
    "G4": 392.00,
    "D4": 293.66,
}
sr = int(2 * max(note.values()))
# Нота, продолжительность, пауза
events = [
    (["D5", "B4", "G4"], 312.5, 104.2),
    (["D5", "B4", "G4"], 104.2, 0),
    (["D5", "B4", "G4"], 208.3, 0),
    (["B4", "G4", "D4"], 208.3, 0),
    (["G4", "B4", "D4"], 416.7, 0),
    (["B4", "G4", "D4"], 208.3, 0),
    (["D5", "B4", "G4"], 312.5, 104.2),
    (["D5", "B4", "G4"], 104.2, 0),
    (["D5", "B4", "G4"], 208.3, 0),
    (["B4", "G4", "D4"], 208.3, 0),
    (["G4", "B4", "D4"], 416.7, 200),
]

events = events * 2

f_max = max(note.values())

samples = 10 * sr
track = np.zeros(samples)
pos = 0

for notes_list, dur_ms, pause_ms in events:
    n_tone = int(sr * dur_ms / 1000)
    t = np.arange(n_tone) / sr

    wave = np.zeros(n_tone)
    for name in notes_list:
        freq = note[name]
        wave += (
            1.00 * np.sin(2 * np.pi * freq * t)
            + 0.60 * np.sin(4 * np.pi * freq * t)
            + 0.35 * np.sin(6 * np.pi * freq * t)
            + 0.20 * np.sin(8 * np.pi * freq * t)
        )
    wave /= len(notes_list)

    env = np.ones(n_tone)
    attack = min(int(sr * 0.02), n_tone)
    release = min(int(sr * 0.05), n_tone)
    env[:attack] = np.linspace(0, 1, attack)
    env[-release:] = np.linspace(1, 0, release)
    wave *= env

    track[pos : pos + n_tone] = wave
    pos += n_tone
    pos += int(sr * pause_ms / 1000)

track = track / np.max(np.abs(track)) * 0.8

sd.play(track, sr)
sd.wait()
