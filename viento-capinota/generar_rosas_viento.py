
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# === CONFIGURACIÓN ===
netcdf_file = "viento_capinota_2024.nc"  # Reemplaza si tu archivo tiene otro nombre
output_dir = "rosas_viento_colores_vivos"
os.makedirs(output_dir, exist_ok=True)

# === 1. CARGAR DATOS ===
ds = xr.open_dataset(netcdf_file)
u10 = ds['u10'].values[:, 0, 0]
v10 = ds['v10'].values[:, 0, 0]
time = pd.to_datetime(ds['valid_time'].values)

# === 2. CALCULAR VELOCIDAD Y DIRECCIÓN ===
speed = np.sqrt(u10**2 + v10**2)
direction = (np.degrees(np.arctan2(-u10, -v10)) + 360) % 360

df = pd.DataFrame({
    'date': time,
    'speed': speed,
    'direction': direction
})

# === 3. CLASIFICACIONES ===
speed_bins = [0, 2, 4, 6, 8, 10, 12, 20]
speed_labels = ['0-2', '2-4', '4-6', '6-8', '8-10', '10-12', '12+']
df['speed_range'] = pd.cut(df['speed'], bins=speed_bins, labels=speed_labels, right=False)
direction_bins = np.arange(0, 361, 30)
df['dir_bin'] = pd.cut(df['direction'], bins=direction_bins, include_lowest=True)

def get_season(month):
    if month in [12, 1, 2]:
        return 'Verano'
    elif month in [3, 4, 5]:
        return 'Otoño'
    elif month in [6, 7, 8]:
        return 'Invierno'
    else:
        return 'Primavera'

df['season'] = df['date'].dt.month.map(get_season)

# === 4. ROSA DE VIENTOS CON COLORES VIVOS ===
bright_colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0']
seasons = ['Verano', 'Otoño', 'Invierno', 'Primavera', 'Todo el año']

for season in seasons:
    df_season = df.copy() if season == 'Todo el año' else df[df['season'] == season]
    table = df_season.groupby(['dir_bin', 'speed_range']).size().unstack(fill_value=0)
    angles = np.radians(direction_bins[:-1] + 15)
    width = np.radians(30)
    bottom = np.zeros(len(angles))

    fig = plt.figure(figsize=(7, 7))
    ax = plt.subplot(111, polar=True)

    for i, label in enumerate(speed_labels):
        values = table[label].reindex(pd.IntervalIndex.from_breaks(direction_bins, closed='left'), fill_value=0).values
        ax.bar(angles, values, width=width, bottom=bottom, color=bright_colors[i], edgecolor='black', label=label)
        bottom += values

    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_title(f'Rosa de Vientos - {season} (Capinota)', fontsize=14)
    ax.legend(title="Velocidad [m/s]", loc='lower left', bbox_to_anchor=(1.05, 0.1))
    plt.tight_layout()
    plt.savefig(f"{output_dir}/rosa_vientos_{season.lower().replace(' ', '_')}.png", dpi=300)
    plt.close()

print("✅ Rosas de viento generadas en la carpeta:", output_dir)
