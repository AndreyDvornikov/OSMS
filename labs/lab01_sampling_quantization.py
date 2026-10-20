import numpy as np
from matplotlib import pyplot as plt

# Переменные
time = np.linspace(0, 1, 500)
f = 10
pf2 = [2 * np.pi * f, 8 * np.pi * f]

# Аналоговый сигнал
yt = np.sin(pf2[0] * time) + np.sin(pf2[1] * time)

max_f = [pf2[0] / (2 * np.pi), pf2[1] / (2 * np.pi)]
D = 2.1 * max(max_f)
dyt = []
DT = []
Fx = []
amp_pos = []
freq_pos = []
for i in range(2):
    print("max_f:", max(max_f))
    print("Частота дискретизации:", D)
    
    DT.append(np.arange(0, 1, 1 / D))
    # Дискретный сигнал
    dyt.append(np.sin(pf2[0] * DT[i]) + np.sin(pf2[1] * DT[i]))
    
    # ППФ
    N = len(dyt[i])
    Fx.append(np.zeros(N, dtype=complex))
    for x in range(N):
        Fxi = 0
        for n in range(N):
            Fxi += dyt[i][n] * np.exp(-1j * 2 * np.pi * (x * (n / N)))
        Fx[i][x] = Fxi

    print("Размер Fx:", Fx[i].nbytes)

    # Нормировка и частоты
    half_N = N // 2 + 1
    amp_pos.append(np.abs(Fx[i][:half_N]) * 2 / N)
    freq_pos.append(np.arange(half_N) * D / N)
    BW = np.ptp(freq_pos[i][np.abs(Fx[i][:half_N]) > 1e-6])
    print("Bandwidth:", BW)
    D = 4*D
    print("===================")

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))

# Cигнал во времени
ax1.plot(time, yt, 'r--', label="Аналоговый сигнал")
ax1.plot(DT[0], dyt[0], 'b.-', label="Дискретный сигнал (D = 2.1 * max_f)")
ax1.plot(DT[1], dyt[1], 'green', label="Дискретный сигнал (D = 8.4*max_f)")
ax1.set_xlabel("t (с)")
ax1.set_ylabel("A (В)")
ax1.legend()
ax1.grid(True)

# Cпектр
ax2.stem(freq_pos[0], amp_pos[0], linefmt='r-', markerfmt='ro', basefmt='k-', label="Спектр (D = 2.1 * max_f)")
ax2.set_xlabel("Частота (Гц)")
ax2.set_ylabel("Амплитуда (В)")
ax2.legend()
ax2.grid(True)
ax3.stem(freq_pos[1], amp_pos[1], linefmt='b-', markerfmt='ro', basefmt='k-', label="Спектр (D = 8.4 * max_f)")
ax3.set_xlabel("Частота (Гц)")
ax3.set_ylabel("Амплитуда (В)")
ax3.legend()
ax3.grid(True)

plt.tight_layout()
plt.show()

# Влияние разрядности АЦП
def quant(signal, bits):
    levels = 2 ** bits - 1
    lo = signal.min()
    hi = signal.max()
    norm = (signal - lo) / (hi - lo)
    q = np.round(norm * levels) / levels
    return q * (hi - lo) + lo


plt.figure()
for bits in [3, 4, 5, 6]:
    yq = quant(yt, bits)
    err = np.mean((yt - yq) ** 2)
    print("Разрядность", bits, "бит, ошибка:", err)
    Fq = np.fft.fft(yq)
    Fq_freq = np.fft.fftfreq(len(yq), d=1 / 500)
    plt.plot(Fq_freq[: len(yq) // 2], np.abs(Fq[: len(yq) // 2]), label=str(bits) + " бит")

F0 = np.fft.fft(yt)
F0_freq = np.fft.fftfreq(len(yt), d=1 / 500)
plt.plot(F0_freq[: len(yt) // 2], np.abs(F0[: len(yt) // 2]), "k--", label="без квант.")
plt.xlabel("f, Гц")
plt.ylabel("А, В")
plt.legend()
plt.show()
