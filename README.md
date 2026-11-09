# Asistente legal RAG para contratos de arrendamiento

Aplicación local hecha con Streamlit y LangChain para consultar contratos de arrendamiento en PDF. Busca fragmentos relevantes en una base vectorial de Chroma y genera una respuesta en español basada en esos fragmentos.

> **Aviso:** este asistente no sustituye el asesoramiento de un profesional del derecho. La aplicación envía consultas y contenido recuperado a los servicios de OpenAI. Antes de procesar contratos confidenciales, verifica que tienes autorización para hacerlo y que el uso cumple tus políticas de privacidad.

## Qué hace

1. `00_vector_store.py` carga los PDF de la carpeta `contratos`, divide su contenido en fragmentos de 5.000 caracteres con un solapamiento de 1.000 y genera embeddings con `text-embedding-3-large`. Guarda los datos en Chroma.
2. `app.py` inicia una interfaz de chat de Streamlit para hacer preguntas sobre los contratos.
3. `rag_system.py` genera consultas alternativas con `gpt-4o-mini`, combina los resultados de un recuperador MMR con una búsqueda por similitud mediante `EnsembleRetriever` y rank fusion ponderado, y redacta la respuesta con `gpt-4o`.
4. La interfaz muestra hasta dos fragmentos recuperados, con su fuente y página, junto a la respuesta.

La respuesta se solicita basándose únicamente en los fragmentos recuperados. La calidad depende de que los PDF tengan texto legible y de que la base vectorial se haya creado correctamente.

## Recuperación de documentos

La configuración actual recupera hasta dos documentos (`SEARCH_K = 2`). MMR examina hasta 20 candidatos (`MMR_FETCH_K = 20`) y usa un factor de diversidad de `0.7` (`MMR_DIVERSITY_LAMBDA`). Con la búsqueda híbrida habilitada (`ENABLE_HYBRID_SEARCH = True`), `EnsembleRetriever` combina MultiQuery sobre MMR y búsqueda por similitud, con pesos `0.7` y `0.3`, respectivamente. La combinación se realiza por rank fusion; no se aplica un umbral de similitud.

Estos parámetros están definidos en `config.py`. Para usar solo MultiQuery sobre MMR, cambia `ENABLE_HYBRID_SEARCH` a `False`.

## Requisitos

- Python 3.10 o posterior.
- Una clave de API de OpenAI con acceso a los modelos configurados: `text-embedding-3-large`, `gpt-4o-mini` y `gpt-4o`.
- Dependencias de Python declaradas en [`pyproject.toml`](./pyproject.toml).
- Los PDF en `D:\python\tema3\contratos` (o actualizar las rutas del proyecto).

## Instalación en Windows (PowerShell)

Desde la carpeta `sistemLegal`, crea un entorno virtual e instala el proyecto y sus dependencias. El modo editable (`-e`) permite instalar dependencias usando la configuración de `pyproject.toml` y ejecutar los módulos desde el directorio del proyecto.

```powershell
cd D:\python\tema3\sistemLegal
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

`pyproject.toml` declara `langchain-classic`, que proporciona `MultiQueryRetriever` y `EnsembleRetriever`. Si ya tenías una instalación anterior, activa el mismo entorno virtual que utilizas para Streamlit y vuelve a instalar el proyecto con el comando anterior.

Configura la clave de OpenAI en la sesión actual de PowerShell:

```powershell
$env:OPENAI_API_KEY = "tu-clave-de-openai"
```

No escribas la clave directamente en el código ni la compartas.

## Preparar la base vectorial

El proyecto necesita una base Chroma creada a partir de los contratos. El cargador busca la carpeta `contratos` relativa al directorio actual; por eso ejecuta el script desde `D:\python\tema3`:

```powershell
cd D:\python\tema3
.\sistemLegal\.venv\Scripts\Activate.ps1
python .\sistemLegal\00_vector_store.py
```

El script guarda la base en `D:\python\tema3\chroma_db`. La generación de embeddings puede tener coste en la cuenta de OpenAI. Vuelve a ejecutar el script cuando quieras reconstruir la base con los PDF actuales.

## Ejecutar la aplicación

Desde la carpeta `sistemLegal`, con el entorno virtual activado y `OPENAI_API_KEY` configurada:

```powershell
cd D:\python\tema3\sistemLegal
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

Streamlit mostrará en la terminal la dirección local para abrir la aplicación en el navegador. Escribe una pregunta sobre los contratos en el chat. Usa **Limpiar Chat** para borrar el historial de la sesión.

## Rutas y configuración

- `config.py` define los modelos, los parámetros de búsqueda y la ruta de Chroma (`CHROMA_DB_PATH`).
- `00_vector_store.py` espera encontrar `contratos` en el directorio desde el que se ejecuta y tiene configurada la ruta de Chroma `D:\python\tema3\chroma_db`.
- Si mueves el proyecto a otra ubicación, actualiza la ruta en `config.py` y en `00_vector_store.py`. Ejecuta el cargador desde el directorio que contiene `contratos`.
- `prompts.py` contiene las instrucciones para generar respuestas y consultas alternativas, además de prompts auxiliares.

## Archivos principales

| Archivo | Función |
|---|---|
| `app.py` | Interfaz Streamlit del chat y visualización de los fragmentos. |
| `rag_system.py` | Inicialización de Chroma, recuperación de documentos y generación de respuestas. |
| `00_vector_store.py` | Carga de PDF, división en fragmentos y creación de la base vectorial. |
| `config.py` | Modelos y parámetros de búsqueda. |
| `prompts.py` | Prompts utilizados por el sistema y prompts auxiliares. |
| `pyproject.toml` | Metadatos del proyecto, versión mínima de Python y dependencias de instalación. |
