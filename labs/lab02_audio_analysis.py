from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
from scipy.io import wavfile

ROOT = Path(__file__).resolve().parents[1]

# Время начала и конца
start: float = 1.00
end: float = 1.05

# Читаю файл
s_rate, samples = wavfile.read(ROOT / "data" / "audio" / "input.wav")

print(samples)
# Стартовые и конечные сэмплы
s_start = int(start * s_rate)
s_end = int(end * s_rate)

# Длительность
duration = len(samples) / s_rate
# Считываю значения и время
channel = samples[s_start:s_end]
N = len(channel)
time = np.linspace(start, end, N)

# Если отрезок больше секунды - считаю через FFT,
# иначе ручное ДПФ.
use_fft: bool = (end - start) > 1.0

# ДПФ
Ak = []  # Амплитуды
Fs = []  # Частоты
Phases = []  # Фазы
FX = []  # Ряд
if use_fft:
    FX = np.fft.fft(channel)
    Ak = np.abs(FX)
    Fs = np.fft.fftfreq(N, d=1 / s_rate)
    Phases = np.angle(FX)
else:
    for k in range(N):  # Частоты
        X = 0
        for n in range(N):  # Отсчёты
            X += channel[n] * np.exp(-1j * 2 * np.pi * k * n / N)
        FX.append(X)
        Ak.append(np.abs(X))
        Fs.append((k * s_rate) / N)
        Phases.append(np.angle(X))


# Вывод первого графика
plt.figure()
plt.plot(time, channel)
plt.xlabel("t (с)", loc="right")
plt.ylabel("А (В)", loc="top")
ax = plt.gca()

ax.spines["bottom"].set_position(("data", 0))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.show()

A_db = 20 * np.log10(Ak)

fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(Fs[: N // 2], A_db[: N // 2])
ax1.set_xscale("log")
ax1.set_xlabel("f, Гц")
ax1.set_ylabel("А, В")
ax1.set_title("Амплитудный спектр")
ax2.plot(Fs[: N // 2], Phases[: N // 2])
ax2.set_xscale("log")
ax2.set_xlabel("f, Гц")
ax2.set_ylabel("Phi")
ax2.set_title("Фазовый спектр")
plt.show()


# Частота дискретизации по количеству отсчётов и длительности
Fs_calc = len(samples) / duration
print("Длительность:", duration, "с")
print("Отсчётов:", len(samples))
print("Fs (расчёт):", Fs_calc, "Гц")
print("Fs (из файла):", s_rate, "Гц")


# Прореживаю, оставляю каждый 10-й отсчёт
full = samples.mean(axis=1, dtype=np.float64) / 32768
y1 = full[::10]

try:
    sd.play(y1, s_rate / 10)
    sd.wait()
except Exception as e:
    print("Не воспроизвелось:", e)


# БПФ оригинала и прореженного сигнала
FX_full = np.fft.fft(full)
FX_dec = np.fft.fft(y1)
Fs_full = np.fft.fftfreq(len(full), d=1 / s_rate)
Fs_dec = np.fft.fftfreq(len(y1), d=10 / s_rate)

fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(Fs_full[: len(full) // 2], 20 * np.log10(np.abs(FX_full[: len(full) // 2])))
ax1.set_xlabel("f, Гц")
ax1.set_ylabel("А, дБ")
ax1.set_title("Спектр оригинала")
ax2.plot(Fs_dec[: len(y1) // 2], 20 * np.log10(np.abs(FX_dec[: len(y1) // 2])))
ax2.set_xlabel("f, Гц")
ax2.set_ylabel("А, дБ")
ax2.set_title("Спектр прореженного")
plt.show()
