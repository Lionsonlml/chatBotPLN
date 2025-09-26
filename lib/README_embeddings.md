# Módulo de Embeddings Semánticos para Chatbot de Videojuegos

## Descripción

Este módulo implementa embeddings semánticos usando Word2Vec de Gensim para mejorar la comprensión del chatbot sobre términos relacionados con videojuegos. Permite calcular similitudes entre términos, encontrar palabras relacionadas y enriquecer las respuestas del chatbot.

## Características

- ✅ **Entrenamiento automático**: Modelo Word2Vec entrenado con corpus de videojuegos
- ✅ **Similitudes semánticas**: Cálculo de similitudes entre términos gaming
- ✅ **Búsqueda de términos similares**: Encuentra los 5 términos más similares a una palabra
- ✅ **Integración completa**: Se integra con el flujo de procesamiento existente
- ✅ **Interfaz visual**: Muestra resultados de embeddings en la interfaz del chatbot
- ✅ **Respuestas enriquecidas**: Mejora las respuestas del bot con información semántica

## Archivos del Módulo

### `semantic_embeddings.py`
Módulo principal que implementa la clase `SemanticEmbeddings` con las siguientes funcionalidades:

- **Entrenamiento del modelo**: Entrena Word2Vec con corpus de videojuegos
- **Cálculo de similitudes**: Encuentra términos similares usando similitud coseno
- **Análisis de texto**: Analiza similitudes en textos de videojuegos
- **Persistencia**: Guarda y carga modelos entrenados

### `gaming_knowledge.py` (actualizado)
Módulo de conocimiento de videojuegos enriquecido con:

- **Análisis semántico**: Integra embeddings en el análisis de contenido
- **Respuestas mejoradas**: Enriquece respuestas con información semántica
- **Términos similares**: Obtiene términos relacionados usando embeddings

### `nlp_processor_with_embeddings.py`
Script de procesamiento que integra:

- **Procesamiento tradicional**: Tokenización, lematización, POS tagging
- **Análisis semántico**: Embeddings y similitudes
- **Análisis gaming**: Detección de contenido relacionado con videojuegos

## Instalación y Configuración

### 1. Instalar Dependencias

```bash
# Instalar dependencias básicas
pip install gensim numpy scipy spacy

# Descargar modelo de español para spaCy
python -m spacy download es_core_news_sm
```

### 2. Configuración Automática

```bash
# Ejecutar script de configuración
python scripts/setup_embeddings.py
```

### 3. Verificación

```python
# Probar el módulo
python lib/semantic_embeddings.py
```

## Uso del Módulo

### Uso Básico

```python
from lib.semantic_embeddings import SemanticEmbeddings

# Crear instancia
embeddings = SemanticEmbeddings()

# Entrenar modelo (si no existe)
if not embeddings.is_trained:
    embeddings.train_model()

# Obtener términos similares
similar_terms = embeddings.get_similar_terms("rpg", topn=5)
print(similar_terms)
```

### Uso con Análisis de Texto

```python
from lib.gaming_knowledge import analyze_gaming_content

# Analizar texto con embeddings
text = "me gusta jugar rpg de acción"
analysis = analyze_gaming_content(text)

# Ver análisis semántico
print(analysis['semantic_analysis'])
print(analysis['similar_terms'])
```

### Uso con Respuestas del Chatbot

```python
from lib.gaming_knowledge import get_gaming_response

# Obtener respuesta enriquecida
response = get_gaming_response("me gusta jugar minecraft")
print(response)
```

## Funcionalidades Principales

### 1. Entrenamiento del Modelo

El modelo se entrena automáticamente con un corpus de más de 100 oraciones relacionadas con videojuegos, incluyendo:

- **Géneros**: RPG, acción, aventura, estrategia, etc.
- **Plataformas**: PC, PlayStation, Xbox, Nintendo, móvil
- **Compañías**: Nintendo, Sony, Microsoft, Ubisoft, etc.
- **Juegos**: Minecraft, Fortnite, Call of Duty, etc.
- **Términos técnicos**: FPS, gráficos, resolución, etc.
- **Gameplay**: Niveles, misiones, multijugador, etc.

### 2. Cálculo de Similitudes

```python
# Calcular similitud entre dos palabras
similarity = embeddings.calculate_similarity("rpg", "aventura")
print(f"Similitud: {similarity:.3f}")

# Obtener palabras más similares
similar_words = embeddings.get_most_similar("rpg", topn=5)
for word, similarity in similar_words:
    print(f"{word}: {similarity:.3f}")
```

### 3. Análisis de Texto

```python
# Analizar similitudes en un texto
text = "me gusta jugar rpg de acción en nintendo"
analysis = embeddings.analyze_text_similarities(text)

print(f"Palabras gaming: {analysis['gaming_words_found']}")
print(f"Pares similares: {analysis['most_similar_pairs']}")
```

## Integración con la Interfaz

El módulo se integra automáticamente con la interfaz del chatbot y muestra:

### 1. Sección de Embeddings Semánticos
- **Palabras Gaming Encontradas**: Muestra las palabras del vocabulario gaming detectadas
- **Pares Más Similares**: Muestra los pares de palabras con mayor similitud
- **Términos Similares**: Lista los términos más similares a las palabras encontradas
- **Estadísticas Semánticas**: Muestra métricas de similitud

### 2. Respuestas Enriquecidas
El chatbot ahora puede:
- Detectar conceptos relacionados semánticamente
- Sugerir términos similares
- Proporcionar respuestas más contextuales
- Mantener conversaciones más fluidas sobre videojuegos

## Configuración Avanzada

### Parámetros del Modelo Word2Vec

```python
# Configuración personalizada
embeddings = SemanticEmbeddings()
embeddings.model = Word2Vec(
    vector_size=100,      # Dimensión de vectores
    window=5,            # Ventana de contexto
    min_count=1,         # Frecuencia mínima
    workers=4,           # Número de hilos
    epochs=100,          # Épocas de entrenamiento
    sg=1,                # Skip-gram
    negative=5,          # Muestreo negativo
    alpha=0.025,         # Tasa de aprendizaje
    seed=42              # Semilla para reproducibilidad
)
```

### Agregar Nuevo Corpus

```python
# Agregar nuevas oraciones al corpus
new_sentences = [
    ["nuevo", "género", "de", "videojuegos"],
    ["realidad", "virtual", "es", "inmersivo"]
]

# Reentrenar con corpus extendido
embeddings.train_model(new_sentences)
```

## Solución de Problemas

### Error: "Gensim no está disponible"
```bash
pip install gensim
```

### Error: "Modelo spaCy no encontrado"
```bash
python -m spacy download es_core_news_sm
```

### Error: "Modelo no entrenado"
```python
# Entrenar manualmente
embeddings = SemanticEmbeddings()
embeddings.train_model()
```

### Rendimiento Lento
- Reducir `vector_size` en la configuración del modelo
- Usar menos `epochs` para entrenamiento más rápido
- Reducir el tamaño del corpus

## Estructura de Datos

### Resultado de `get_similar_terms()`
```python
[
    {
        'rank': 1,
        'word': 'aventura',
        'similarity': 0.85,
        'similarity_percentage': 85.0,
        'vector': [0.1, 0.2, ...]  # Vector de 100 dimensiones
    },
    # ... más términos
]
```

### Resultado de `analyze_text_similarities()`
```python
{
    'gaming_words_found': ['rpg', 'acción', 'nintendo'],
    'total_similarities': 3,
    'similarities': [
        {
            'word1': 'rpg',
            'word2': 'acción',
            'similarity': 0.75,
            'similarity_percentage': 75.0
        }
    ],
    'most_similar_pairs': [...],
    'average_similarity': 0.65
}
```

## Contribuciones

Para mejorar el módulo:

1. **Agregar más corpus**: Añadir más oraciones relacionadas con videojuegos
2. **Mejorar parámetros**: Ajustar configuración del modelo Word2Vec
3. **Nuevas funcionalidades**: Implementar análisis semántico avanzado
4. **Optimización**: Mejorar rendimiento y eficiencia

## Licencia

Este módulo es parte del proyecto Chatbot de Videojuegos y sigue la misma licencia del proyecto principal.
