import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np

# CSV einlesen
df = pd.read_csv("11_BP_1_02.0.csv")
wn, intensity = df.iloc[:, 0], df.iloc[:, 1]

# Peak-Erkennung mit höherer Prominence (nur wichtige Peaks)
peaks, props = find_peaks(-intensity, prominence=0.03, distance=2)

# Plot
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(wn, intensity, color="black", linewidth=1)

# Alle Peaks mit Sticks markieren
for i in peaks:
    ax.vlines(wn[i], ymin=1.0, ymax=intensity[i], color="black", linewidth=0.8)
    ax.text(wn[i], intensity[i] - 0.05, f"{wn[i]:.0f}",
            rotation=90, va="top", ha="center", fontsize=8)

ax.invert_xaxis()
ax.set_xlabel("Wellenzahl / cm⁻¹", fontsize=11)
ax.set_ylabel("Transmission / %", fontsize=11)
ax.set_ylim(0, 1.05)
ax.set_xlim(4000, 400)
plt.tight_layout()
plt.savefig("IR_peaks.pdf", dpi=300, bbox_inches='tight')


print(f"Anzahl Peaks: {len(peaks)}")
print("Peaks (cm⁻¹):")
print(sorted(wn[peaks].round(0), reverse=True))

