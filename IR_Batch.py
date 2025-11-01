import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np
import os
from pathlib import Path
from datetime import datetime

# ==================== EINSTELLUNGEN ====================
INPUT_FOLDER = "IR_Daten"
OUTPUT_FOLDER = "IR_Output"

# OPTION 1: Gleiche Einstellungen für alle Dateien
DEFAULT_PROMINENCE = 0.05
DEFAULT_DISTANCE = 25

# OPTION 2: Individuelle Einstellungen pro Datei
# Format: "dateiname.csv": (prominence, distance)
CUSTOM_SETTINGS = {
    "11_BP_1_02.csv": (0.03, 15),    # Weniger Peaks
    # "12_BP_2_03.0.csv": (0.03, 10),    # Mehr Peaks
    # Weitere Dateien hier hinzufügen...
}
# =======================================================

# Output-Ordner erstellen
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Alle CSV-Dateien finden
csv_files = list(Path(INPUT_FOLDER).glob("*.csv"))

# Text-Datei für Zusammenfassung vorbereiten
summary_file = os.path.join(OUTPUT_FOLDER, "peak_summary.txt")
summary_lines = []

if len(csv_files) == 0:
    print(f"Keine CSV-Dateien in '{INPUT_FOLDER}' gefunden!")
else:
    print(f"{len(csv_files)} CSV-Datei(en) gefunden\n")
    
    for csv_file in csv_files:
        try:
            # Einstellungen für diese Datei ermitteln
            if csv_file.name in CUSTOM_SETTINGS:
                prominence, distance = CUSTOM_SETTINGS[csv_file.name]
                print(f"[Custom] {csv_file.name} (prom={prominence}, dist={distance})")
            else:
                prominence, distance = DEFAULT_PROMINENCE, DEFAULT_DISTANCE
                print(f"[Default] {csv_file.name} (prom={prominence}, dist={distance})")
            
            # CSV einlesen
            df = pd.read_csv(csv_file)
            wn, intensity = df.iloc[:, 0], df.iloc[:, 1]
            
            # Peak-Erkennung mit spezifischen Parametern
            peaks, props = find_peaks(-intensity, prominence=prominence, distance=distance)
            
            # Plot erstellen
            fig, ax = plt.subplots(figsize=(14, 6))
            ax.plot(wn, intensity, color="black", linewidth=1)
            
            # Peaks markieren und beschriften
            for i in peaks:
                ax.vlines(wn[i], ymin=1.0, ymax=intensity[i], color="black", linewidth=0.8)
                ax.text(wn[i], intensity[i] - 0.05, f"{wn[i]:.0f}",
                       rotation=90, va="top", ha="center", fontsize=8)
            
            # Formatierung
            ax.invert_xaxis()
            ax.set_xlabel("Wellenzahl / cm⁻¹", fontsize=11)
            ax.set_ylabel("Transmission / %", fontsize=11)
            ax.set_ylim(0, 1.05)
            ax.set_xlim(4000, 400)
            ax.set_title(csv_file.stem, fontsize=12, pad=10)
            plt.tight_layout()
            
            # PDF speichern
            output_path = os.path.join(OUTPUT_FOLDER, f"{csv_file.stem}.pdf")
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            # Peak-Liste erstellen
            peak_list = sorted(wn[peaks].round(0).astype(int), reverse=True)
            
            # Konsolenausgabe
            print(f"   -> {len(peaks)} Peaks gefunden")
            print(f"   -> {output_path}")
            print(f"   -> Peaks: {peak_list}\n")
            
            # In Zusammenfassung speichern
            summary_lines.append(f"{'='*70}\n")
            summary_lines.append(f"Datei: {csv_file.name}\n")
            summary_lines.append(f"Parameter: prominence={prominence}, distance={distance}\n")
            summary_lines.append(f"Anzahl Peaks: {len(peaks)}\n")
            summary_lines.append(f"\nPeaks (cm^-1):\n")
            summary_lines.append(f"{peak_list}\n\n")
            
        except Exception as e:
            print(f"FEHLER bei {csv_file.name}: {e}\n")
            summary_lines.append(f"{'='*70}\n")
            summary_lines.append(f"Datei: {csv_file.name}\n")
            summary_lines.append(f"FEHLER: {e}\n\n")
    
    # Zusammenfassung in Textdatei schreiben
    if summary_lines:
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("IR-SPEKTREN PEAK-ZUSAMMENFASSUNG\n")
            f.write(f"Generiert: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*70}\n\n")
            f.writelines(summary_lines)
        print(f"\nFertig! Alle PDFs sind in '{OUTPUT_FOLDER}/'")
        print(f"Peak-Zusammenfassung: {summary_file}")
    else:
        print(f"\nFertig! Alle PDFs sind in '{OUTPUT_FOLDER}/'")
        print("Keine Daten für Zusammenfassung vorhanden.")