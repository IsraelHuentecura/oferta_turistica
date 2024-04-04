import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
import folium


# Load the data
df_procesado = pd.read_csv('./data/hoteles_puerto_varas_prototipo_merge.csv')


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

# Hacer mapa con Folium y marcar cada uno de los hoteles, que muestre el score y nombre cuando se pasa por arriba
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
        
    folium.Marker([row['latitud'], row['longitud']], 
                  popup=row['nombre'],
                    icon=folium.Icon(color=color,
                                     icon='star'),
                    tooltip=f"""<b>{row['nombre']}</b><br><br>Score: {row['score']}
                    <br>Reviews: {row['reviews']}
                    <br>Categoria: {row['categorias']}
                    <br>Direccion: {row['localidad']}
                    """
                    
                  ).add_to(m)
    
# Agregar columna de mapa
leyenda_html = """
<div style="
    position: fixed;
    bottom: 50px;
    left: 50px;
    z-index: 1000;
    padding: 6px 8px;
    background: #FFFFFF;
    border-radius: 5px;
    border: 2px solid grey;
    font-size: 14px;
    font-weight: bold;
    width: 200px;
    height: 100px;
    ">
    <p> Leyenda </p>
    <p> Excellent: Azul </p>
    <p> Very Good: Verde </p>
    <p> Average: Naranjo </p>
    <p> Poor: Rojo </p>
</div>
"""
m.get_root().html.add_child(folium.Element(leyenda_html))

    
col1, col2 = st.columns([1, 1])


# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)

# Hacer grafico de proporciones de categorias
fig = px.pie(df_procesado, names='categorias', title='Proporción de categorías')
# Very good es verde
fig.update_traces(marker=dict(colors=['blue', 'green', 'orange', 'red', 'black']))


col2.plotly_chart(fig)



# Display the filtered dataframe
col1.write(df_procesado)

# Cuantos hoteles o restaurantes hay en total
col1.write(f'Número de hoteles o restaurantes: {len(df_procesado)}')

