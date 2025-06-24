import cdsapi
import os
import time

# Medir tiempo de ejecución
inicio = time.time()

# Crear carpeta para guardar resultados
os.makedirs("datos_era5_capinota", exist_ok=True)

# Iniciar cliente de CDS
c = cdsapi.Client()

print("🚀 Enviando solicitud a Copernicus para ERA5 (Capinota, 2024)...")

# Definir parámetros
c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'format': 'netcdf',
        'variable': ['100m_u_component_of_wind', '100m_v_component_of_wind'],
        'year': '2024',
        'month': [f"{i:02d}" for i in range(1, 13)],
        'day': [f"{i:02d}" for i in range(1, 32)],
        'time': ['00:00', '06:00', '12:00', '18:00'],
        'area': [-17.60, -66.35, -17.75, -66.15],  # Zona precisa alrededor de Capinota [N, W, S, E]
    },
    'datos_era5_capinota/viento_capinota_2024.nc'
)

fin = time.time()
duracion = fin - inicio
minutos = int(duracion // 60)
segundos = int(duracion % 60)

print(f"\n✅ Descarga completa: 'viento_capinota_2024.nc'")
print(f"⏱️ Tiempo total: {minutos} min {segundos} s")
