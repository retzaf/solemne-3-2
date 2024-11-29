import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

def show():
    # Cargar los datos
    try:
        book = pd.read_csv('books_of_the_decade.csv')
        user_reviews = pd.read_csv('user_reviews_dataset.csv')
        st.success('📊 ¡Datos cargados correctamente!')
    except FileNotFoundError as e:
        st.error(f"⚠️ Error al cargar los datos: {e}")
        st.stop()

    # Limpiar datos problemáticos
    # Limpiar la columna Rating para convertir a numérico (extrayendo valores numéricos)
    if 'Rating' in book.columns:
        book['Rating'] = book['Rating'].str.extract(r'(\d+\.\d+)').astype(float)

    # Limpiar la columna Score (por si contiene texto)
    if 'Score' in book.columns:
        book['Score'] = pd.to_numeric(book['Score'], errors='coerce')

    # Limpiar la columna Number of Votes
    if 'Number of Votes' in book.columns:
        book['Number of Votes'] = pd.to_numeric(book['Number of Votes'], errors='coerce')

    # Fusionar datasets
    books = pd.merge(user_reviews, book, left_on='bookIndex', right_on='Index', how='inner')

    # Análisis General
    st.markdown("<h2>📊 Análisis General</h2>", unsafe_allow_html=True)
    st.subheader('Top 10 Libros de la Década por Puntaje')

    # Mostrar tabla de los 10 mejores libros
    col1, col2 = st.columns([2, 1])
    with col1:
        top_ten_books = book.sort_values(by='Score', ascending=False).head(10)
        st.dataframe(top_ten_books[['Book Name', 'Author', 'Score', 'Rating', 'Number of Votes']])

    with col2:
        st.markdown("""
        <div style='padding: 10px; background-color: #eef; border-radius: 8px;'>
        Aquí se muestran los 10 libros mejor rankeados de la década en base al puntaje total otorgado por los lectores.
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Análisis con gráficos
    st.markdown("<h2>📈 Visualizaciones</h2>", unsafe_allow_html=True)

    # Histograma de puntuaciones
    st.subheader('Distribución de Puntajes de los Libros')
    fig, ax = plt.subplots()
    sns.histplot(book['Score'], kde=True, bins=20, ax=ax, color='skyblue')
    ax.set_title('Distribución de los Puntajes')
    ax.set_xlabel('Puntaje')
    ax.set_ylabel('Frecuencia')
    st.pyplot(fig)

    # Mapa de calor de correlaciones
    st.subheader('Mapa de Calor de Correlaciones')
    numeric_columns = book[['Score', 'Rating', 'Number of Votes']].dropna()
    corr = numeric_columns.corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title('Correlaciones entre Variables')
    st.pyplot(fig)

    # Gráfico de barras de los libros con más votos
    st.subheader('Top 10 Libros con Más Votos')
    top_voted_books = book.sort_values(by='Number of Votes', ascending=False).head(10)
    fig, ax = plt.subplots()
    sns.barplot(data=top_voted_books, x='Number of Votes', y='Book Name', palette='viridis', ax=ax)
    ax.set_title('Top 10 Libros con Más Votos')
    ax.set_xlabel('Número de Votos')
    ax.set_ylabel('Nombre del Libro')
    st.pyplot(fig)

    # Gráfico de barras de puntajes promedio por autor
    st.subheader('Puntaje Promedio de los Autores Principales')
    top_authors = book.groupby('Author')['Score'].mean().sort_values(ascending=False).head(10).reset_index()
    fig, ax = plt.subplots()
    sns.barplot(data=top_authors, x='Score', y='Author', palette='magma', ax=ax)
    ax.set_title('Puntaje Promedio de los Mejores Autores')
    ax.set_xlabel('Puntaje Promedio')
    ax.set_ylabel('Autor')
    st.pyplot(fig)

    st.divider()

    # Mensaje final
    st.markdown("<h3>📚 ¡Gracias por explorar los mejores libros de la década!</h3>", unsafe_allow_html=True)
