# Este script carga los archivos PDF del directorio "contratos", divide su
# contenido en fragmentos de texto y crea embeddings con el modelo
# "text-embedding-3-large". Guarda los fragmentos y sus vectores en una base
# Chroma local; después busca los dos fragmentos más similares a una consulta
# sobre el local mencionado en un contrato e imprime su contenido y metadatos.

# Herramientas para crear la base vectorial, generar embeddings, cargar PDFs
# desde un directorio y dividir el texto en fragmentos manejables.


#pip install chromadb


from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Carga todos los documentos PDF encontrados en el directorio "contratos".
#loader = PyPDFDirectoryLoader("C:\\Users\\santiago\\curso_langchain\\Tema 3\\contratos")
loader = PyPDFDirectoryLoader("contratos")
documentos = loader.load()

# Informa cuántos documentos se cargaron antes de procesar su contenido.
print(f"Se cargaron {len(documentos)} documentos desde el directorio.")

# Divide el texto en fragmentos de hasta 5000 caracteres. Mantiene 1000
# caracteres compartidos entre fragmentos consecutivos para conservar contexto.
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=5000,
    chunk_overlap=1000
)

# Aplica la configuración de división a los documentos cargados.
docs_split = text_splitter.split_documents(documentos)

# Muestra cuántos fragmentos se usarán para crear la base vectorial.
print(f"Se crearon {len(docs_split)} chunks de texto.")

# Genera embeddings para cada fragmento y los almacena en Chroma. El directorio
# indicado permite guardar la base vectorial localmente.
vectorstore = Chroma.from_documents(
    docs_split,
    embedding=OpenAIEmbeddings(model="text-embedding-3-large"),
    persist_directory="D:\\python\\tema3\\chroma_db"
)

# Busca fragmentos relacionados semánticamente con esta pregunta y solicita
# como máximo los dos resultados más similares.
consulta = "¿Dónde se encuentra el local del contrato en el que participa María Jiménez Campos"

resultados = vectorstore.similarity_search(consulta, k=2)

# Imprime el contenido y los metadatos de cada fragmento recuperado.
print("Top 3 documentos mas similares a la consulta:\n")
for i, doc in enumerate(resultados, start=1):
    print(f"Contenido: {doc.page_content}")
    print(f"Metadatos: {doc.metadata}")