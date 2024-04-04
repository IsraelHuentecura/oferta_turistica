import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import streamlit as st

# Asumimos que 'comentarios' es tu lista de textos de TripAdvisor
comentarios = [
    'Excelente restaurante en Puerto, uno de los mejores del sur de Chile[^1^][1]',
    'La Olla es un lugar autóctono para degustar en familia deliciosos platos frescos, abundantes de mariscos[^1^][1]',
    'Pésima atención en La Olla, el lugar está sucio[^1^][1]',
    'CasaValdes es uno de mis imperdibles en Puerto , su gastronomía es excelente[^2^][2]',
    'Mantiene la tradición de sus ostras de criadero propio en Casa Valdés[^2^][2]',
    'La comida muy rica, buena preparación de cocteles en Casa Valdés[^2^][2]',
    'Aunque los ingredientes son frescos, las preparaciones no son las mejores en Casa Valdés[^2^][2]',
    'Soy de Puerto, siempre vamos para allá con mi familia. Muy bien logrado, la decoración, el personal muy agradable, todo muy limpio y ordenado[^3^][4]',
    'La atención muy buena e informada, los aperitivos bien hechos y muy fríos en La Marca[^4^][5]',
    'El Centro de Puerto es encantador, con su arquitectura alemana y sus vistas al lago[^1^][1]',
    'La Iglesia del Sagrado Corazón de Jesús es una joya arquitectónica, no puedes dejar de visitarla[^1^][1]',
    'La Costanera de Puerto ofrece unas vistas impresionantes del lago y los volcanes[^1^][1]',
    'El Muelle Piedraplen es un lugar perfecto para pasear y disfrutar de la puesta de sol[^1^][1]',
    'La Plaza Princesa Likanrayen es un lugar tranquilo para descansar después de un día de turismo[^1^][1]',
    'El Parque Philippi es ideal para una caminata tranquila, con vistas panorámicas de la ciudad[^1^][1]',
    'La Ruta de las Casas coloniales es un viaje al pasado, muy recomendable[^1^][1]',
    'El Museo Pablo Fierro es un lugar fascinante, lleno de historia y cultura local[^1^][1]'

]


# Stopwords en español
stopwords = [
    'de', 'la', 'que', 'el',
    'en', 'y', 'a', 'los', 'del',
    'se', 'las', 'por', 'un', 'para',
    'con', 'no', 'una', 'su','muy', 'puerto', 
    'varas','sus','casa', 'lugar', 'e','es','mi','al','lo','me','mi','mis','mis','son','uno'
]
# Eliminar stopwords de los comentarios
comentarios = [comentario.lower() for comentario in comentarios]
comentarios = [' '.join([word for word in comentario.split() if word not in stopwords]) for comentario in comentarios]
# Unir todos los comentarios en un solo texto
texto = ' '.join(comentarios)
# Creamos la nube de palabras
wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = None, 
                min_font_size = 10).generate(texto)

# Ploteamos la nube de palabras
plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 

st.pyplot(plt)

import plotly.express as px
from collections import Counter

# Contamos la frecuencia de cada palabra
frecuencia_palabras = Counter(' '.join(comentarios).split())

# Creamos un DataFrame con las palabras y sus frecuencias
df = pd.DataFrame.from_dict(frecuencia_palabras, orient='index').reset_index()
df = df.rename(columns={'index':'Palabra', 0:'Frecuencia'})

# Creamos el gráfico de barras con Plotly
fig = px.bar(df, x='Palabra', y='Frecuencia', title='Frecuencia de las palabras en los comentarios de TripAdvisor sobre Puerto Varas')
st.plotly_chart(fig)
