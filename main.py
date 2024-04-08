import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
import folium
import folium.plugins as plugins


# Load the data
df_procesado = pd.read_csv('./data/hoteles_puerto_varas_prototipo_merge.csv')

st.set_page_config(layout="wide")
# Calcular centroide
centroide = df_procesado[['latitud', 'longitud']].mean()

# Create a map
st.title('Oferta turística en Puerto Varas')	

# Create a sidebar for filters
st.sidebar.title('Filtros')

# Filtro por tipo de alojamiento
categorias = st.sidebar.multiselect('Tipo de alojamiento', df_procesado['tipo'].unique())
if categorias:
    df_procesado = df_procesado[df_procesado['tipo'].isin(categorias)]
# Filter by score
score = st.sidebar.slider('Score', min_value=0.0, max_value=5.0, value=(0.0, 5.0))
df_procesado = df_procesado[(df_procesado['score'] >= score[0]) & (df_procesado['score'] <= score[1])]

# Filter by number of reviews
reviews = st.sidebar.slider('Número de Reviews', min_value=0, max_value=int(df_procesado['reviews'].max()), value=(0, int(df_procesado['reviews'].max())))
df_procesado = df_procesado[(df_procesado['reviews'] >= reviews[0]) & (df_procesado['reviews'] <= reviews[1])]

# Hacer mapa con Folium y marcar cada uno de los hoteles, que muestre el score y nombre cuando se pasa por arriba y con leyenda
m = folium.Map(location=[-41.320084,-72.980447], zoom_start=14)

# Add a marker for each hotel and diferent color for each category Excellent, Very Good, Average, Poor, Terrible
for i, row in df_procesado.iterrows():
    if row['categorias'] == 'Excellent':
        color = 'blue'
    elif row['categorias'] == 'Very Good':
        color = 'green'
    elif row['categorias'] == 'Average':
        color = 'orange'
    elif row['categorias'] == 'Poor':
        color = 'red'
    else:
        color = 'black'
    # Add the marker to the map
    # add legend
    folium.Marker([row['latitud'], row['longitud']], 
                  popup=row['nombre'],
                    icon=folium.Icon(color=color,
                                     icon='glyphicon glyphicon-home' if row['tipo'] == 'Alojamientos' else 'glyphicon glyphicon-cutlery'),
                    tooltip=f"""<b>{row['nombre']}</b><br><br>Score: {row['score']}
                    <br>Reviews: {row['reviews']}
                    <br>Categoria: {row['categorias']}
                    <br>Direccion: {row['localidad']}
                    """,
                    
                    
                  ).add_to(m)
    

    
col1, col2, col3 = st.columns([1, 1, 1])

st.markdown(f"# Mapa de {categorias[0]} en Puerto Varas" if categorias else "# Mapa de alojamientos y restaurantes en Puerto Varas")

# call to render Folium map in Streamlit with legend
st_data = st_folium(m, width=1500, height=800)

if categorias == ['Alojamientos']:
    nombre_grafico_torta = f'Proporción de categorías de evaluación de alojamientos'
elif categorias == ['Restaurantes']:
    nombre_grafico_torta = f'Proporción de categorías de evaluación de restaurantes'
else:
    nombre_grafico_torta = f'Proporción de categorías de evaluación de alojamientos y restaurantes'
     
# Hacer grafico de proporciones de categorias en consonancia con el mapa
# Define the color mapping
color_mapping = {'Excellent': 'blue',
                 'Very Good': 'green',
                 'Average': 'orange',
                 'Poor': 'red',
                 'Terrible': 'black'}

# Create the pie chart
fig = px.pie(df_procesado, names='categorias', title=nombre_grafico_torta, hole=0.5,
             color='categorias', color_discrete_map=color_mapping)

col1.plotly_chart(fig)




# Cuantos hoteles o restaurantes hay en total
col3.write(f'Número de hoteles o restaurantes: {len(df_procesado)}')


# Display the filtered dataframe
#col3.write(df_procesado)

# Agregar un mapa de calor de la cantidad de reviews


# Create a list of coordinates and reviews
data = df_procesado[['latitud', 'longitud', 'reviews']].values.tolist()

# Create a heatmap pero sin los marcadores
m = folium.Map(location=[-41.320084,-72.980447], zoom_start=14)

heatmap = plugins.HeatMap(data)

# Add the heatmap to the map
heatmap.add_to(m)

st.markdown("# Mapa de calor según concentración de reviews\n\nEste mapa muestra la concentración de reviews en Puerto Varas. Mientras más rojo, mayor concentración de reviews en esa zona.")
# Render the map
st_folium(m, width=1500, height=800)
