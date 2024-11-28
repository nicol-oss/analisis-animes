import pandas as pd
import matplotlib.pyplot as plt


file_path = 'Animes Estadisticas con la API.xlsx'
data = pd.ExcelFile(file_path)


df = data.parse('Hoja1')


df['Fecha Emisión'] = pd.to_datetime(df['Fecha Emisión'], errors='coerce')
df['Popularidad'] = pd.to_numeric(df['Popularidad'], errors='coerce')
df['N° Episodios'] = pd.to_numeric(df['N° Episodios'], errors='coerce')


stats = {
    'Popularidad': {
        'Promedio': df['Popularidad'].mean(),
        'Desviación estándar': df['Popularidad'].std(),
        'Moda': df['Popularidad'].mode().iloc[0] if not df['Popularidad'].mode().empty else None,
        'Máximo': df['Popularidad'].max(),
        'Mínimo': df['Popularidad'].min()
    },
    'N° Episodios': {
        'Promedio': df['N° Episodios'].mean(),
        'Desviación estándar': df['N° Episodios'].std(),
        'Moda': df['N° Episodios'].mode().iloc[0] if not df['N° Episodios'].mode().empty else None,
        'Máximo': df['N° Episodios'].max(),
        'Mínimo': df['N° Episodios'].min()
    }
}


plt.figure(figsize=(20, 20))


plt.subplot(3, 2, 1)
df_sorted_popularity = df.sort_values('Popularidad', ascending=False).head(20)
plt.plot(df_sorted_popularity['Nombre'], df_sorted_popularity['Popularidad'], label='Popularidad', marker='o', color='blue')
plt.xticks(rotation=90)
plt.title('Popularidad y N° Episodios por Anime (Top 20)')
plt.ylabel('Popularidad')
plt.xlabel('Anime')

plt.twinx()
plt.plot(df_sorted_popularity['Nombre'], df_sorted_popularity['N° Episodios'], label='N° Episodios', marker='x', color='orange')
plt.ylabel('N° Episodios')
plt.legend(loc='upper left')


plt.subplot(3, 2, 2)
genre_counts = df['Género'].str.split(', ').explode().value_counts()
genre_counts.plot(kind='bar', color='skyblue', title='Cantidad de Animes por Género')
plt.ylabel('Cantidad')
plt.xlabel('Género')
plt.xticks(rotation=45)


plt.subplot(3, 2, 3)
season_counts = df['Temporada'].value_counts()
season_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, title='Distribución por Temporada', colors=plt.cm.Paired.colors)
plt.ylabel('')


plt.subplot(3, 2, 4)
df_time_series = df.dropna(subset=['Fecha Emisión'])
anime_releases_by_date = df_time_series.groupby('Fecha Emisión').size()
anime_releases_by_date.plot(kind='line', marker='o', title='Serie de Tiempo: Lanzamientos de Anime')
plt.ylabel('Cantidad de Animes')
plt.xlabel('Fecha Emisión')


plt.subplot(3, 2, 5)
plt.scatter(df['N° Episodios'], df['Popularidad'], alpha=0.6, color='purple')
plt.title('Dispersión: Popularidad vs N° Episodios')
plt.xlabel('N° Episodios')
plt.ylabel('Popularidad')


plt.subplot(3, 2, 6)
stats_text = '\n'.join([
    f"{key}: Promedio={values['Promedio']:.2f}, Desv.Est.={values['Desviación estándar']:.2f}, "
    f"Moda={values['Moda']}, Máximo={values['Máximo']}, Mínimo={values['Mínimo']}"
    for key, values in stats.items()
])
plt.axis('off')  
plt.text(0.5, 0.5, stats_text, fontsize=12, ha='center', va='center', wrap=True)
plt.title('Estadísticas Generales')


plt.tight_layout(pad=3.0, h_pad=2.0, w_pad=3.0)
plt.show()
