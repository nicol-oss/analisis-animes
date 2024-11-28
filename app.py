import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


st.set_page_config(page_title="Análisis de Animes", layout="wide")


@st.cache_data
def load_data(file_path):
    df = pd.ExcelFile(file_path).parse('Hoja1')
    df['Fecha Emisión'] = pd.to_datetime(df['Fecha Emisión'], errors='coerce')
    df['Popularidad'] = pd.to_numeric(df['Popularidad'], errors='coerce')
    df['N° Episodios'] = pd.to_numeric(df['N° Episodios'], errors='coerce')
    return df

file_path = "Animes Estadisticas con la API.xlsx"
df = load_data(file_path)


st.title("Análisis Interactivo de Animes")


st.sidebar.header("Filtros de Datos")
temporada_seleccionada = st.sidebar.multiselect(
    "Selecciona la(s) Temporada(s):",
    options=df['Temporada'].dropna().unique(),
    default=df['Temporada'].dropna().unique()
)
genero_seleccionado = st.sidebar.multiselect(
    "Selecciona el/los Género(s):",
    options=df['Género'].str.split(', ').explode().unique(),
    default=df['Género'].str.split(', ').explode().unique()
)


df_filtrado = df[ 
    (df['Temporada'].isin(temporada_seleccionada)) & 
    (df['Género'].apply(lambda x: any(genre in x.split(', ') for genre in genero_seleccionado)))
]


st.write(f"### Datos Filtrados: {len(df_filtrado)} Animes")
st.dataframe(df_filtrado)


st.subheader("Estadísticas Descriptivas")

popularidad_stats = {
    'Moda': int(df_filtrado['Popularidad'].mode().values[0]) if not df_filtrado['Popularidad'].mode().empty else 'N/A',  
    'Desviación Estándar': df_filtrado['Popularidad'].std(),
    'Máximo': int(df_filtrado['Popularidad'].max()),  
    'Mínimo': int(df_filtrado['Popularidad'].min()),  
    'Promedio': df_filtrado['Popularidad'].mean()
}

episodios_stats = {
    'Moda': int(df_filtrado['N° Episodios'].mode().values[0]) if not df_filtrado['N° Episodios'].mode().empty else 'N/A',  
    'Desviación Estándar': df_filtrado['N° Episodios'].std(),
    'Máximo': int(df_filtrado['N° Episodios'].max()),  
    'Mínimo': int(df_filtrado['N° Episodios'].min()),  
    'Promedio': df_filtrado['N° Episodios'].mean()
}

st.write("### Estadísticas de Popularidad:")
st.write(popularidad_stats)

st.write("### Estadísticas de Número de Episodios:")
st.write(episodios_stats)


st.subheader("Popularidad y Número de Episodios (Top 20)")
top_20 = df_filtrado.sort_values('Popularidad', ascending=False).head(20)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(top_20['Nombre'], top_20['Popularidad'], label='Popularidad', marker='o', color='blue')


ax.set_xticks(range(len(top_20)))


ax.set_xticklabels(top_20['Nombre'], rotation=90)

ax.set_title('Popularidad por Anime')
ax.set_xlabel('Nombre')
ax.set_ylabel('Popularidad')
ax.legend()
st.pyplot(fig)


st.subheader("Cantidad de Animes por Género")
genre_counts = df_filtrado['Género'].str.split(', ').explode().value_counts()
st.bar_chart(genre_counts)


st.subheader("Distribución por Temporada")
season_counts = df_filtrado['Temporada'].value_counts()
fig, ax = plt.subplots()
ax.pie(season_counts, labels=season_counts.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
ax.set_title('Distribución por Temporada')
st.pyplot(fig)


st.subheader("Serie de Tiempo: Lanzamientos de Animes")
anime_releases_by_date = df_filtrado.groupby('Fecha Emisión').size()
st.line_chart(anime_releases_by_date)


st.subheader("Dispersión: Popularidad vs N° Episodios")
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(df_filtrado['N° Episodios'], df_filtrado['Popularidad'], alpha=0.6, color='purple')
ax.set_title('Dispersión: Popularidad vs N° Episodios')
ax.set_xlabel('N° Episodios')
ax.set_ylabel('Popularidad')
st.pyplot(fig)



