import os
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from windrose import WindroseAxes
from matplotlib import cm

# Crear carpeta para guardar figuras
os.makedirs("figuras", exist_ok=True)

# Cargar archivo .nc (ajusta la ruta si es necesario)
ds = xr.open_dataset("datos_era5_capinota/viento_capinota_2024.nc")
tiempos = pd.to_datetime(ds['valid_time'].values)
u = ds['u100'].values
v = ds['v100'].values

# Calcular velocidad y dirección del viento
velocidad = np.sqrt(u**2 + v**2)
direccion = (270 - np.rad2deg(np.arctan2(v, u))) % 360

# Crear DataFrame con las variables relevantes
df = pd.DataFrame({
    'tiempo': tiempos,
    'velocidad': velocidad.flatten(),
    'direccion': direccion.flatten()
}).dropna()

# Función para graficar rosas de viento con colores modernos
def graficar_rosa(df, titulo, archivo):
    ax = WindroseAxes.from_ax()
    ax.bar(df['direccion'], df['velocidad'],
           bins = [0.0, 0.8, 1.6, 2.4, 3.2, 4.0, 4.8, 5.6, 6.4, 7.2, 8.0],  # rangos personalizados como en tu imagen
           normed=True, opening=0.8, edgecolor='white', cmap=cm.plasma)
    ax.set_legend(title="Velocidad [m/s]")  # leyenda clara con unidades
    ax.set_title(titulo, fontsize=14)
    plt.savefig(f"figuras/{archivo}", dpi=300)
    plt.close()

# Rosa anual
graficar_rosa(df, "Rosa de Vientos - Capinota 2024", "rosa_anual_2024.png")

# Estaciones del año
estaciones = {
    'verano': ((12, 21), (3, 20)),
    'otoño': ((3, 21), (6, 20)),
    'invierno': ((6, 21), (9, 22)),
    'primavera': ((9, 23), (12, 20))
}

# Filtrar y graficar por estación
for est, ((mes_ini, dia_ini), (mes_fin, dia_fin)) in estaciones.items():
    if mes_ini < mes_fin:
        df_est = df[
            ((df['tiempo'].dt.month > mes_ini) | ((df['tiempo'].dt.month == mes_ini) & (df['tiempo'].dt.day >= dia_ini))) &
            ((df['tiempo'].dt.month < mes_fin) | ((df['tiempo'].dt.month == mes_fin) & (df['tiempo'].dt.day <= dia_fin)))
        ]
    else:  # verano (dic-mar)
        df_est = df[
            (df['tiempo'].dt.month >= mes_ini) | (df['tiempo'].dt.month <= mes_fin)
        ]
    graficar_rosa(df_est, f"Rosa de Vientos - {est.capitalize()} 2024", f"rosa_{est}_2024.png")

print("✅ Rosas de viento generadas en la carpeta 'figuras'")
