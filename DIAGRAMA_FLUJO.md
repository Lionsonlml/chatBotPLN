# Diagrama de Flujo del Chatbot de PLN

## 1. Flujo Principal de la Aplicación

```
+---------------------+     +----------------------+     +---------------------+
|                     |     |                      |     |                     |
| Inicio de Aplicación|---->| Carga de Componentes |---->| Mensaje de Bienvenida|
|                     |     |                      |     |                     |
+---------------------+     +----------------------+     +----------+----------+
                                                                   |
                                                                   v
+---------------------+     +----------------------+     +---------------------+
|                     |     |                      |     |                     |
| Respuesta del Bot   |<----| Procesamiento PLN    |<----| Entrada del Usuario |
|                     |     |                      |     |                     |
+----------+----------+     +----------------------+     +---------------------+
           |
           v
+---------------------+     +----------------------+
|                     |     |                      |
| Análisis Visualizado|     | ¿Despedida Detectada?|---->+---------------------+
|                     |     |                      |     |                     |
+---------------------+     +----------+----------+     | Fin de Conversación |
                                        |                |                     |
                                        | No             +---------------------+
                                        v
                             +----------------------+
                             |                      |
                             | Espera Nueva Entrada |
                             |                      |
                             +----------------------+
```

## 2. Flujo de Procesamiento de Mensajes

```
+---------------------+
|                     |
| Mensaje del Usuario |
|                     |
+----------+----------+
           |
           v
+---------------------+     +----------------------+
|                     | No  |                      |
| ¿Es un Saludo?     |---->| ¿Es una Despedida?   |
|                     |     |                      |
+----------+----------+     +----------+----------+
           | Sí                        | No
           v                           v
+---------------------+     +----------------------+
|                     |     |                      |
| Activar Conversación|     | ¿Relacionado con    |
|                     |     | Videojuegos?        |
+----------+----------+     +----------+----------+
                                        | Sí
                                        v
+---------------------+     +----------------------+
|                     |     |                      |
| Respuesta General   |<----| Respuesta Específica |
|                     |     | de Videojuegos      |
+---------------------+     +----------------------+
```

## 3. Flujo de Procesamiento PLN

```
+---------------------+
|                     |
| Texto a Procesar    |
|                     |
+----------+----------+
           |
           v
+---------------------+     +----------------------+
|                     | Sí  |                      |
| ¿API Disponible?    |---->| Procesamiento API    |
|                     |     |                      |
+----------+----------+     +----------+----------+
           | No                        |
           v                           |
+---------------------+                |
|                     |                |
| Procesamiento Local |                |
|                     |                |
+----------+----------+                |
           |                           |
           v                           v
+---------------------+     +----------------------+
|                     |     |                      |
| Tokenización        |     | Tokenización        |
|                     |     |                      |
+----------+----------+     +----------+----------+
           |                           |
           v                           v
+---------------------+     +----------------------+
|                     |     |                      |
| Lematización        |     | Lematización        |
|                     |     |                      |
+----------+----------+     +----------+----------+
           |                           |
           v                           v
+---------------------+     +----------------------+
|                     |     |                      |
| Etiquetado POS      |     | Etiquetado POS      |
|                     |     |                      |
+----------+----------+     +----------+----------+
           |                           |
           v                           v
+---------------------+     +----------------------+
|                     |     |                      |
| Análisis Videojuegos|     | Análisis Videojuegos|
|                     |     |                      |
+----------+----------+     +----------+----------+
           |                           |
           v                           v
+---------------------+
|                     |
| Resultados Análisis |
|                     |
+---------------------+
```

## 4. Flujo de Análisis de Videojuegos

```
+---------------------+
|                     |
| Texto a Analizar    |
|                     |
+----------+----------+
           |
           v
+---------------------+     +----------------------+
|                     | No  |                      |
| ¿Relacionado con    |---->| Respuesta Fuera     |
| Videojuegos?        |     | de Tema             |
+----------+----------+     +----------------------+
           | Sí
           v
+---------------------+
|                     |
| Extracción de       |
| Palabras Clave      |
+----------+----------+
           |
           v
+---------------------+     +----------------------+     +---------------------+
|                     |     |                      |     |                     |
| ¿Menciona Juegos    | Sí  | Respuesta Específica|     | Respuesta sobre     |
| Específicos?        |---->| sobre el Juego      |---->| Otros Aspectos      |
|                     |     |                      |     |                     |
+----------+----------+     +----------------------+     +---------------------+
           | No
           v
+---------------------+     +----------------------+
|                     | Sí  |                      |
| ¿Menciona Géneros?  |---->| Respuesta sobre     |
|                     |     | el Género           |
+----------+----------+     +----------------------+
           | No
           v
+---------------------+     +----------------------+
|                     | Sí  |                      |
| ¿Menciona           |---->| Respuesta sobre     |
| Plataformas?        |     | la Plataforma       |
+----------+----------+     +----------------------+
           | No
           v
+---------------------+     +----------------------+
|                     | Sí  |                      |
| ¿Menciona           |---->| Respuesta sobre     |
| Compañías?          |     | la Compañía         |
+----------+----------+     +----------------------+
           | No
           v
+---------------------+
|                     |
| Respuesta General   |
| sobre Videojuegos   |
+---------------------+
```

## 5. Arquitectura del Sistema

```
+-------------------+     +-------------------+     +-------------------+
|                   |     |                   |     |                   |
|  Interfaz Usuario |<--->|  Lógica Chatbot   |<--->|  Procesamiento   |
|  (React/Next.js)  |     |  (TypeScript)     |     |  PLN             |
|                   |     |                   |     |                   |
+-------------------+     +-------------------+     +--------+----------+
                                                             |
                                                             v
                          +-------------------+     +-------------------+
                          |                   |     |                   |
                          |  API Routes       |<--->|  Scripts Python   |
                          |  (Next.js)        |     |  (NLTK/spaCy)     |
                          |                   |     |                   |
                          +-------------------+     +-------------------+
                                    ^
                                    |
                                    v
                          +-------------------+
                          |                   |
                          |  Conocimiento     |
                          |  Videojuegos      |
                          |  (TypeScript)     |
                          +-------------------+
```

Estos diagramas proporcionan una visualización clara de los diferentes flujos y componentes del sistema, facilitando la comprensión de su funcionamiento y arquitectura.