import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from mpl_toolkits.axes_grid1 import make_axes_locatable


# Lee los datos como lo estabas haciendo
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

world = world[world.name != "Antarctica"] # esto elimina informacion irrelevante en este caso como el continente antartica. 

df_indicator = pd.read_csv('fertilizer_data.csv')
# Filtrar los valores nulos en la columna 'value'
df_indicator = df_indicator[df_indicator['value'].notnull()]

# Filtrar por categoría y rango de años
fertilizer_df = df_indicator[(df_indicator['indicator_name'] == 'Fertilizer consumption (kilograms per hectare of arable land)') & 
                             (df_indicator['year'].between(1990, 2021))].copy()


# rename code column and drop rows with empty cells 
fertilizer_df.rename({'country_code':'iso_a3'}, axis=1, inplace=True)
fertilizer_df = fertilizer_df [['iso_a3', 'value', 'year']].dropna()
# merge dataframes and filter columns
world_values = world.merge(fertilizer_df, how='inner', on='iso_a3', copy=True)
world_values = world_values[['name', 'iso_a3', 'year', 'geometry', 'value']]

        
# Ahora puedes utilizar el DataFrame cargado en tu script
# Título de la aplicación
st.title('Consumo de Fertilizantes por País y Año')

# Selector de país
selected_country = st.selectbox('Selecciona un país:', world_values['name'].unique())

# Selector de año
selected_year = st.selectbox('Selecciona un año:', world_values['year'].unique())

# Filtrar los datos según la selección del usuario
filtered_data = world_values[(world_values['name'] == selected_country) & (world_values['year'] == selected_year)]

# Mostrar la cantidad de fertilizante consumido
if not filtered_data.empty:
    st.write(f"El consumo de fertilizante en {selected_country} en el año {selected_year} fue de {filtered_data['value'].iloc[0]}")
else:
    st.write("No hay datos disponibles para el país y año seleccionados.")


# Crear una figura y ejes
fig, ax = plt.subplots(1, figsize=(16, 8), facecolor='lightblue')

# Dibujar el mapa mundial en gris
world_map = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world_map.plot(ax=ax, color='darkgrey')

# Dibujar el mapa de valores de fertilizantes por país, usando una escala de colores de amarillo a rojo
# Líneas negras remarcando países
filtered_data.plot(column='value', ax=ax, cmap='YlOrRd', edgecolors='black')

# Configurar color bar
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="3%", pad=0.05)
vmax = filtered_data['value'].max()
mappable = plt.cm.ScalarMappable(cmap='YlOrRd', norm=plt.Normalize(vmin=0, vmax=vmax))
cbar = fig.colorbar(mappable, cax=cax)
cbar.set_ticks(range(0, int(vmax), int(vmax / 10)))
cbar.ax.tick_params(labelsize=10)

# Título del mapa
ax.set_title(f'Uso de fertilizantes por país ({selected_year})', fontsize=16)

# Mostrar el mapa
st.pyplot(fig)