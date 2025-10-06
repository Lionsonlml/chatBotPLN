# Chatbot con GPT-2 en Español

Este chatbot utiliza un modelo GPT-2 entrenado en español para generar respuestas conversacionales y analiza los sentimientos de los mensajes usando pysentimiento.

## Características

- **GPT-2 en Español**: Modelo `datificate/gpt2-small-spanish` para respuestas conversacionales
- **Análisis de Sentimientos**: Usando pysentimiento para detectar emociones
- **Análisis de PLN Completo**: Tokenización, lematización, POS tagging y embeddings semánticos
- **Configuración Dinámica**: Ajusta parámetros del modelo en tiempo real
- **Interfaz Moderna**: UI responsive con análisis visual completo

## Instalación

### Para Windows (Recomendado)

```bash
# Ejecutar el script de instalación para Windows
install_windows.bat

# O usar el script Python específico para Windows
python scripts/install_windows.py
```

### Para otros sistemas

```bash
# Ejecutar el script de instalación automática
python scripts/install_dependencies.py

# O instalar manualmente
pip install -r requirements.txt

# Descargar modelo de spaCy para español
python -m spacy download es_core_news_sm
```

### Solución de problemas de instalación

**Error de compilación en Windows:**
- Usa `install_windows.bat` que instala paquetes pre-compilados
- O instala Visual Studio Build Tools si necesitas compilar

**Error con gensim:**
- El sistema tiene fallback automático a scikit-learn
- No es crítico para el funcionamiento básico

**Error con numpy 2.0:**
- Se usa numpy < 2.0.0 para compatibilidad
- Se instala automáticamente la versión correcta

### 2. Instalar dependencias de Node.js

```bash
npm install
```

### 3. Verificar instalación

```bash
# Probar que todo funciona
python scripts/test_system.py
```

## Uso

### 1. Iniciar el servidor

```bash
npm run dev
```

### 2. Abrir en el navegador

Ve a `http://localhost:3000`

### 3. Comenzar conversación

1. Escribe "hola" para iniciar
2. Conversa normalmente con el bot
3. Ajusta los parámetros GPT-2 en el panel lateral
4. Observa el análisis de sentimientos en tiempo real

## Configuración GPT-2

Puedes ajustar estos parámetros en la interfaz:

- **Longitud máxima**: Controla la longitud de las respuestas (50-200 tokens)
- **Temperatura**: Controla la creatividad (0.1 = más serio, 1.0 = más creativo)
- **Top-p**: Controla la diversidad de vocabulario (0.1-1.0)

## API Endpoints

### GPT-2 Chat
```
POST /api/gpt2-chat
{
  "text": "tu mensaje aquí",
  "max_length": 120,
  "temperature": 0.1,
  "top_p": 0.9
}
```

### Análisis de Sentimientos
```
POST /api/sentiment-analysis
{
  "text": "texto a analizar"
}
```

## Estructura del Proyecto

```
├── app/
│   ├── api/
│   │   ├── gpt2-chat/route.ts          # Endpoint GPT-2
│   │   └── sentiment-analysis/route.ts # Endpoint sentimientos
│   └── page.tsx                        # Página principal
├── components/
│   └── chatbot-interface.tsx           # Interfaz del chat
├── scripts/
│   ├── gpt2_processor.py               # Script GPT-2
│   ├── sentiment_analyzer.py           # Script sentimientos
│   ├── install_dependencies.py         # Instalador
│   └── test_system.py                  # Verificador
└── requirements.txt                    # Dependencias Python
```

## Solución de Problemas

### Error al cargar GPT-2
- Verifica que transformers y torch estén instalados
- El modelo se descarga automáticamente la primera vez

### Error en análisis de sentimientos
- Verifica que pysentimiento esté instalado
- El sistema tiene fallback automático

### Scripts de Python no funcionan
- Verifica que Python 3.8+ esté instalado
- Ejecuta `python scripts/test_system.py` para diagnóstico

## Tecnologías Utilizadas

- **Frontend**: Next.js, TypeScript, Tailwind CSS
- **Backend**: Next.js API Routes
- **IA**: Transformers (GPT-2), PySentimiento
- **Procesamiento**: spaCy, NLTK, Gensim

