# Chatbot de Procesamiento de Lenguaje Natural

Una aplicación educativa que implementa técnicas básicas de PLN (tokenización, lematización y etiquetado morfosintáctico) integradas en un chatbot con frontend visual interactivo.

## 🎯 Objetivo de Aprendizaje

Implementar técnicas básicas de Procesamiento de Lenguaje Natural e integrarlas en un chatbot con frontend visual, identificando su relación con la Ingeniería de Sistemas y Computación en el contexto de aplicaciones web.

## 🚀 Características

### Backend (PLN)
- **Tokenización**: Métodos básicos con regex/espacios y librerías (NLTK/spaCy)
- **Lematización**: WordNetLemmatizer y spaCy con explicación de limitaciones
- **POS Tagging**: Etiquetado morfosintáctico usando NLTK y spaCy
- **Documentación completa**: Código documentado con ejemplos de uso

### Frontend (Interfaz del Chatbot)
- **Interfaz visual moderna**: Desarrollada con React/Next.js
- **Chat interactivo**: Permite escribir mensajes y ver respuestas procesadas
- **Análisis en tiempo real**: Panel lateral que muestra tokenización, lematización y POS tagging
- **Diseño educativo**: Interfaz clara con códigos de colores para diferentes categorías gramaticales

## 🛠️ Tecnologías Utilizadas

- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS
- **Backend**: Python con NLTK y spaCy
- **UI Components**: shadcn/ui
- **Análisis PLN**: NLTK, spaCy (modelo es_core_news_sm)

## 📋 Requisitos del Sistema

### Para el Frontend
- Node.js 18+
- npm o yarn

### Para el Backend de PLN
- Python 3.8+
- pip

## 🔧 Instalación y Configuración

### 1. Configuración del Frontend

\`\`\`bash
# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev
\`\`\`

### 2. Configuración del Backend de PLN

\`\`\`bash
# Instalar librerías de Python
pip install nltk spacy

# Descargar modelo de spaCy para español
python -m spacy download es_core_news_sm

# Ejecutar el procesador de PLN (opcional, para pruebas)
python scripts/nlp_processor.py
\`\`\`

## 🎮 Uso de la Aplicación

1. **Acceder a la interfaz**: Abrir http://localhost:3000 en el navegador
2. **Escribir mensaje**: Introducir texto en el campo de entrada del chat
3. **Ver análisis**: El panel lateral mostrará automáticamente:
   - **Tokenización**: División del texto en tokens
   - **Lematización**: Forma base de cada palabra
   - **POS Tagging**: Categoría gramatical con códigos de colores

## 📊 Ejemplos de Análisis

### Entrada: "Los niños están jugando en el parque"

**Tokenización:**
- `los`, `niños`, `están`, `jugando`, `en`, `el`, `parque`

**Lematización:**
- `niños` → `niño`
- `están` → `estar`
- `jugando` → `jugar`

**POS Tagging:**
- `los`: DET (Determinante)
- `niños`: NOUN (Sustantivo)
- `están`: VERB (Verbo)
- `jugando`: VERB (Verbo)
- `en`: PREP (Preposición)
- `el`: DET (Determinante)
- `parque`: NOUN (Sustantivo)

## 🔍 Arquitectura del Sistema

\`\`\`
├── app/
│   ├── page.tsx                 # Página principal
│   ├── layout.tsx              # Layout de la aplicación
│   ├── globals.css             # Estilos globales
│   └── api/
│       └── nlp-process/
│           └── route.ts        # API endpoint para PLN
├── components/
│   └── chatbot-interface.tsx   # Componente principal del chatbot
├── scripts/
│   └── nlp_processor.py        # Procesador de PLN en Python
└── README.md                   # Documentación
\`\`\`

## 🎨 Características del Diseño

- **Colores semánticos**: Verde para elementos educativos y de crecimiento
- **Códigos de colores POS**: Cada categoría gramatical tiene su color distintivo
- **Interfaz responsiva**: Adaptable a diferentes tamaños de pantalla
- **Feedback visual**: Indicadores de procesamiento y estados de carga

## 🧪 Limitaciones y Consideraciones

### Lematización
- **NLTK WordNetLemmatizer**: Optimizado para inglés, limitaciones en español
- **spaCy**: Mejor rendimiento con modelo específico para español

### POS Tagging
- **NLTK**: Entrenado principalmente para inglés
- **spaCy**: Mayor precisión con modelo es_core_news_sm para español

## 🚀 Mejoras Futuras

1. **Integración completa con Python**: Ejecutar scripts de PLN desde la API
2. **Análisis sintáctico**: Agregar parsing y análisis de dependencias
3. **Reconocimiento de entidades**: NER (Named Entity Recognition)
4. **Análisis de sentimientos**: Clasificación emocional del texto
5. **Soporte multiidioma**: Expandir a otros idiomas
6. **Exportación de resultados**: Generar reportes en PDF

## 📚 Referencias Bibliográficas

- Bird, S., Klein, E., & Loper, E. (2009). Natural Language Processing with Python. O'Reilly Media.
- Honnibal, M., & Montani, I. (2017). spaCy 2: Natural language understanding with Bloom embeddings, convolutional neural networks and incremental parsing.
- Manning, C. D., & Schütze, H. (1999). Foundations of Statistical Natural Language Processing. MIT Press.
- Jurafsky, D., & Martin, J. H. (2020). Speech and Language Processing (3rd ed.). Pearson.

## 📄 Licencia

Este proyecto es de uso educativo y está desarrollado para fines académicos.
