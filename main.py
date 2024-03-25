import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
import folium


# Load the data
df_procesado = pd.read_csv('./data/hoteles_puerto_varas_prototipo.csv', index_col=0)


# Calcular centroide
centroide = df_procesado[['latitud', 'longitud']].mean()

# Create a map
st.title('Oferta turística en Puerto Varas')	

# Create a sidebar for filters
st.sidebar.title('Filtros')

# Filter by score
score = st.sidebar.slider('Score', min_value=0.0, max_value=5.0, value=(0.0, 5.0))
df_procesado = df_procesado[(df_procesado['score'] >= score[0]) & (df_procesado['score'] <= score[1])]

# Filter by number of reviews
reviews = st.sidebar.slider('Número de Reviews', min_value=0, max_value=int(df_procesado['reviews'].max()), value=(0, int(df_procesado['reviews'].max())))
df_procesado = df_procesado[(df_procesado['reviews'] >= reviews[0]) & (df_procesado['reviews'] <= reviews[1])]

# Hacer mapa con Folium y marcar cada uno de los hoteles, que muestre el score y nombre cuando se pasa por arriba
m = folium.Map(location=[-41.320084,-72.980447], zoom_start=14)
# Add a marker for each hotel and diferent color for each category
for i, row in df_procesado.iterrows():
    folium.Marker([row['latitud'], row['longitud']], 
                  popup=row['nombre'],
                    icon=folium.Icon(color='blue' if row['categorias'] == 'Excellent' else 'green',
                                     icon='star'),
                    tooltip=f"""<b>{row['nombre']}</b><br><br>Score: {row['score']}
                    <br>Reviews: {row['reviews']}
                    <br>Categoria: {row['categorias']}
                    <br>Direccion: {row['localidad']}
                    """
                    
                  ).add_to(m)
    
    
col1, col2 = st.columns([1, 1])


# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)

# Hacer grafico de proporciones de categorias
fig = px.pie(df_procesado, names='categorias', title='Proporción de categorías')
col2.plotly_chart(fig)

# Display the filtered dataframe
col1.write(df_procesado)

