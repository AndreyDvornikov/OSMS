import matplotlib.pyplot as plt
import numpy as np

BS_Ptx = 46  # dBm
num_sectors = 3
UE_Ptx = 24  # dBm
BS_Gain = 21  # dBi
UE_Gain = 0  # dBi
PenetrationM = 15  # dB
IM = 1  # dB
propagation_model_macro = "COST 231 Hata"
propagation_model_micro_femto = "UMiNLOS"
freq_band = 1.8  # GHz
bandwidth_UL = 10  # MHz
bandwidth_DL = 20  # MHz
duplex_mode = "FDD"
BS_Noise_Figure = 2.4  # dB
UE_Noise_Figure = 6.0  # dB
SINR_req_DL = 2  # dB
SINR_req_UL = 4  # dB
BS_mimo_antennas = 2
MIMO_Gain = 3  # dB
area_total = 100  # sq km
area_micro_femto = 4  # sq km
has_feeders = True
feeder_loss = 2  # dB
MSU_loss = 0.4  # dB
Jumper_loss = 0.5  # dB
hBS = 50
hms = 5

N0 = -174 + 10 * np.log10(bandwidth_UL * 1e6)
RxSensBS = N0 + BS_Noise_Figure + SINR_req_UL
MAPL_UL = (
    UE_Ptx
    + UE_Gain
    + BS_Gain
    + MIMO_Gain
    - feeder_loss
    - MSU_loss
    - Jumper_loss
    - RxSensBS
    - PenetrationM
    - IM
)

print("MAPL_UL:", MAPL_UL)

N0_Dl = -174 + 10 * np.log10(bandwidth_DL * 1e6)
RxSensUE = N0_Dl + UE_Noise_Figure + SINR_req_DL
MAPL_DL = (
    BS_Ptx
    + BS_Gain
    + UE_Gain
    + MIMO_Gain
    - feeder_loss
    - MSU_loss
    - Jumper_loss
    - RxSensUE
    - PenetrationM
    - IM
)

print("MAPL_DL:", MAPL_DL)

d = np.linspace(0.1, 20, 100)  # km
A = 46.3
B = 33.9

a = 3.2 * (np.log10(11.75 * hms)) ** 2 - 4.97
s = np.where(
    d < 1,
    (47.88 + 13.9 * np.log10(freq_band * 1000) - 13.9 * np.log10(hBS))
    / np.log10(50),
    44.9 - 6.55 * np.log10(hBS),
)
Lclutter = 0

dh = 15
w = 20
b = 40
phi = 90
f_MHz = freq_band * 1000

L0 = 32.44 + 20 * np.log10(f_MHz) + 20 * np.log10(d)
if 0 <= phi < 35:
    ori_loss = -10 + 0.354 * phi
elif 35 <= phi < 55:
    ori_loss = 2.5 + 0.075 * phi
else:
    ori_loss = 4.0 - 0.114 * phi
L2 = (
    -16.9
    - 10 * np.log10(w)
    + 10 * np.log10(f_MHz)
    + 20 * np.log10(dh - hms)
    + ori_loss
)
L1_1 = -18 * np.log10(1 + hBS - dh) if hBS > dh else 0
if hBS > dh:
    ka = 54.0
    kd = 18.0
else:
    kd = 18 - 15 * ((hBS - dh) / dh)
    ka = (
        54 - 0.8 * (hBS - dh)
        if np.all(d > 0.5)
        else (54 - 0.8 * (hBS - dh) * (d / 0.5))
    )
kf = -4 + 0.7 * (f_MHz / 925 - 1)
L1 = L1_1 + ka + kd * np.log10(d) + kf * np.log10(f_MHz) - 9 * np.log10(b)

PLd_UMiNLOS = 26 * np.log10(freq_band) + 22.7 + 36.7 * np.log10(d * 1000)
PLd_Hata = (
    A
    + B * np.log10(freq_band * 1000)
    - 13.82 * np.log10(hBS)
    - a
    + s * np.log10(d)
    + Lclutter
)
PLd_WI = np.where(L1 + L2 > 0, L0 + L1 + L2, L0)

plt.figure(figsize=(8, 5))
plt.plot(d, PLd_WI, label="COST 231 Walfisch-Ikegami", color="orange", linewidth=2)
plt.plot(d, PLd_Hata, label="COST 231 Hata", color="b", linewidth=2)
plt.plot(d, PLd_UMiNLOS, label="UMiNLOS", color="g", linewidth=2)
plt.axhline(
    y=MAPL_UL,
    color="r",
    linestyle="--",
    label=f"MAPL = {MAPL_UL:.1f} дБ",
)

plt.title("Зависимость потерь сигнала от расстояния")
plt.xlabel("Расстояние d, км")
plt.ylabel("Потери PL(d), дБ")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.show()

R_UL = np.interp(MAPL_UL, PLd_Hata, d)
R_DL = np.interp(MAPL_DL, PLd_Hata, d)
R_cell = min(R_UL, R_DL)
S_site = 1.95 * (R_cell**2)
N_sites = int(np.ceil(area_total / S_site))

print(f"R_UL: {R_UL:.3f} км")
print(f"R_DL: {R_DL:.3f} км")
print(f"R_cell: {R_cell:.3f} км")
print(f"S_site: {S_site:.3f} кв. км")
print(f"N_sites: {N_sites}")
