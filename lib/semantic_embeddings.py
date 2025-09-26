"""
Módulo de Embeddings Semánticos para Chatbot de Videojuegos
===========================================================

Este módulo implementa embeddings semánticos usando Word2Vec de Gensim
para mejorar la comprensión del chatbot sobre términos relacionados con videojuegos.

Funcionalidades:
- Entrenamiento de modelo Word2Vec con corpus de videojuegos
- Conversión de palabras clave a vectores
- Cálculo de similitudes entre términos
- Búsqueda de términos más similares
- Integración con el flujo de procesamiento del chatbot

Autor: Asistente IA
Fecha: 2024
"""

import os
import json
import pickle
import numpy as np
from typing import List, Dict, Tuple, Any, Optional
from collections import defaultdict
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from gensim.models import Word2Vec
    from gensim.models.word2vec import LineSentence
    GENSIM_AVAILABLE = True
except ImportError:
    logger.warning("Gensim no está disponible. Instalando...")
    GENSIM_AVAILABLE = False

class SemanticEmbeddings:
    """
    Clase para manejar embeddings semánticos de videojuegos usando Word2Vec.
    """
    
    def __init__(self, model_path: str = "models/gaming_word2vec.model"):
        """
        Inicializa el módulo de embeddings semánticos.
        
        Args:
            model_path (str): Ruta donde se guardará/cargará el modelo
        """
        self.model_path = model_path
        self.model = None
        self.vocabulary = set()
        self.is_trained = False
        
        # Crear directorio de modelos si no existe
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # Cargar modelo existente si está disponible
        self._load_model()
    
    def _create_gaming_corpus(self) -> List[List[str]]:
        """
        Crea un corpus de texto relacionado con videojuegos para entrenar el modelo.
        
        Returns:
            List[List[str]]: Lista de oraciones tokenizadas
        """
        logger.info("Creando corpus de videojuegos...")
        
        # Corpus de frases relacionadas con videojuegos
        gaming_sentences = [
            # Géneros de videojuegos
            ["rpg", "es", "un", "género", "de", "videojuegos", "donde", "desarrollas", "personajes"],
            ["los", "juegos", "de", "acción", "tienen", "mucho", "ritmo", "y", "emociones"],
            ["los", "shooters", "en", "primera", "persona", "son", "muy", "populares"],
            ["los", "juegos", "de", "estrategia", "requieren", "planificación", "y", "táctica"],
            ["los", "juegos", "de", "aventura", "tienen", "historias", "emocionantes"],
            ["los", "juegos", "de", "simulación", "recrean", "experiencias", "reales"],
            ["los", "juegos", "de", "deportes", "simulan", "deportes", "reales"],
            ["los", "juegos", "de", "carreras", "son", "divertidos", "y", "competitivos"],
            ["los", "juegos", "de", "puzzle", "desafían", "tu", "inteligencia"],
            ["los", "juegos", "de", "plataformas", "requieren", "precisión", "y", "timing"],
            ["los", "roguelikes", "tienen", "mecánicas", "de", "muerte", "permanente"],
            ["los", "metroidvanias", "combinan", "exploración", "y", "progresión"],
            ["los", "battle", "royale", "son", "competitivos", "y", "emocionantes"],
            ["los", "moba", "requieren", "trabajo", "en", "equipo", "y", "estrategia"],
            ["los", "juegos", "sandbox", "ofrecen", "libertad", "total", "de", "creación"],
            ["los", "juegos", "de", "mundo", "abierto", "permiten", "exploración", "libre"],
            ["los", "juegos", "de", "supervivencia", "desafían", "tu", "capacidad", "de", "adaptación"],
            ["los", "juegos", "de", "terror", "crean", "atmósferas", "tenebrosas"],
            
            # Plataformas
            ["pc", "es", "la", "plataforma", "más", "versátil", "para", "jugar"],
            ["playstation", "tiene", "exclusivos", "increíbles"],
            ["xbox", "ofrece", "game", "pass", "y", "servicios", "en", "la", "nube"],
            ["nintendo", "switch", "es", "portátil", "y", "versátil"],
            ["los", "juegos", "móviles", "son", "accesibles", "y", "convenientes"],
            ["android", "y", "ios", "tienen", "juegos", "exclusivos"],
            
            # Compañías y desarrolladores
            ["nintendo", "crea", "juegos", "familiares", "y", "divertidos"],
            ["sony", "desarrolla", "juegos", "exclusivos", "de", "alta", "calidad"],
            ["microsoft", "posee", "xbox", "y", "estudios", "de", "desarrollo"],
            ["ubisoft", "crea", "juegos", "de", "mundo", "abierto", "inmersivos"],
            ["electronic", "arts", "desarrolla", "fifa", "y", "otros", "deportes"],
            ["activision", "crea", "call", "of", "duty", "y", "otros", "shooters"],
            ["blizzard", "desarrolla", "world", "of", "warcraft", "y", "overwatch"],
            ["rockstar", "crea", "grand", "theft", "auto", "y", "red", "dead", "redemption"],
            ["valve", "desarrolla", "half", "life", "y", "portal"],
            ["bethesda", "crea", "the", "elder", "scrolls", "y", "fallout"],
            ["capcom", "desarrolla", "resident", "evil", "y", "street", "fighter"],
            ["square", "enix", "crea", "final", "fantasy", "y", "kingdom", "hearts"],
            ["epic", "games", "desarrolla", "fortnite", "y", "unreal", "engine"],
            ["riot", "games", "crea", "league", "of", "legends", "y", "valorant"],
            
            # Juegos populares
            ["minecraft", "es", "un", "juego", "de", "construcción", "y", "supervivencia"],
            ["fortnite", "es", "un", "battle", "royale", "muy", "popular"],
            ["call", "of", "duty", "es", "una", "serie", "de", "shooters", "famosos"],
            ["grand", "theft", "auto", "es", "un", "juego", "de", "mundo", "abierto"],
            ["fifa", "es", "el", "juego", "de", "fútbol", "más", "popular"],
            ["the", "legend", "of", "zelda", "es", "una", "serie", "de", "aventuras"],
            ["mario", "es", "el", "personaje", "más", "famoso", "de", "nintendo"],
            ["pokemon", "es", "una", "serie", "de", "rpg", "muy", "popular"],
            ["overwatch", "es", "un", "shooter", "multijugador", "colorido"],
            ["league", "of", "legends", "es", "el", "moba", "más", "jugado"],
            ["world", "of", "warcraft", "es", "el", "mmorpg", "más", "famoso"],
            ["the", "witcher", "es", "una", "serie", "de", "rpg", "fantásticos"],
            ["dark", "souls", "es", "conocido", "por", "su", "dificultad"],
            ["elden", "ring", "es", "el", "último", "juego", "de", "from", "software"],
            ["assassins", "creed", "es", "una", "serie", "de", "aventuras", "históricas"],
            ["red", "dead", "redemption", "es", "un", "western", "interactivo"],
            ["halo", "es", "la", "serie", "exclusiva", "de", "xbox"],
            ["god", "of", "war", "es", "una", "aventura", "épica", "de", "playstation"],
            ["horizon", "zero", "dawn", "es", "un", "juego", "de", "mundo", "abierto"],
            ["final", "fantasy", "es", "una", "serie", "de", "rpg", "japoneses"],
            ["resident", "evil", "es", "una", "serie", "de", "terror", "survival"],
            ["valorant", "es", "un", "shooter", "táctico", "competitivo"],
            ["apex", "legends", "es", "un", "battle", "royale", "futurista"],
            ["among", "us", "es", "un", "juego", "de", "trabajo", "en", "equipo"],
            ["roblox", "es", "una", "plataforma", "de", "creación", "de", "juegos"],
            
            # Términos técnicos
            ["fps", "significa", "frames", "por", "segundo"],
            ["los", "gráficos", "modernos", "son", "muy", "realistas"],
            ["la", "resolución", "4k", "ofrece", "imágenes", "nítidas"],
            ["hdr", "mejora", "el", "contraste", "y", "los", "colores"],
            ["ray", "tracing", "crea", "iluminación", "realista"],
            ["dlss", "mejora", "el", "rendimiento", "con", "ia"],
            ["la", "latencia", "baja", "es", "importante", "para", "jugar"],
            ["el", "ping", "afecta", "la", "conexión", "multijugador"],
            ["el", "lag", "puede", "arruinar", "la", "experiencia", "de", "juego"],
            ["los", "bugs", "son", "errores", "en", "el", "código", "del", "juego"],
            ["los", "glitches", "pueden", "ser", "divertidos", "o", "problemáticos"],
            ["los", "parches", "corrigen", "errores", "y", "mejoran", "el", "juego"],
            ["las", "actualizaciones", "añaden", "nuevo", "contenido"],
            ["los", "dlc", "expanden", "el", "contenido", "del", "juego"],
            ["las", "expansiones", "añaden", "nuevas", "áreas", "y", "mecánicas"],
            ["los", "mods", "modifican", "el", "juego", "creado", "por", "la", "comunidad"],
            ["los", "shaders", "mejoran", "los", "efectos", "visuales"],
            ["las", "texturas", "definen", "la", "apariencia", "de", "los", "objetos"],
            ["el", "renderizado", "procesa", "las", "imágenes", "del", "juego"],
            
            # Términos de gameplay
            ["los", "niveles", "desafían", "al", "jugador", "progresivamente"],
            ["las", "misiones", "avanzan", "la", "historia", "del", "juego"],
            ["las", "quest", "son", "tareas", "específicas", "para", "completar"],
            ["los", "jefes", "son", "enemigos", "poderosos", "y", "desafiantes"],
            ["los", "boss", "requieren", "estrategia", "y", "habilidad"],
            ["los", "npc", "son", "personajes", "no", "jugables", "controlados", "por", "ia"],
            ["los", "personajes", "tienen", "habilidades", "y", "atributos", "únicos"],
            ["el", "inventario", "almacena", "objetos", "y", "equipamiento"],
            ["las", "habilidades", "mejoran", "con", "la", "experiencia"],
            ["las", "armas", "varían", "en", "daño", "y", "alcance"],
            ["el", "equipo", "protege", "y", "mejora", "las", "capacidades"],
            ["el", "crafteo", "permite", "crear", "objetos", "nuevos"],
            ["el", "crafting", "es", "una", "mecánica", "de", "creación"],
            ["el", "farmeo", "consiste", "en", "repetir", "actividades", "para", "obtener", "recursos"],
            ["el", "farming", "es", "una", "estrategia", "de", "obtención", "de", "recursos"],
            ["el", "loot", "son", "recompensas", "obtenidas", "al", "completar", "actividades"],
            ["el", "botín", "incluye", "objetos", "y", "recursos", "valiosos"],
            ["el", "pvp", "es", "combate", "jugador", "contra", "jugador"],
            ["el", "pve", "es", "combate", "jugador", "contra", "entorno"],
            ["el", "multijugador", "permite", "jugar", "con", "otros", "jugadores"],
            ["el", "modo", "cooperativo", "fomenta", "el", "trabajo", "en", "equipo"],
            ["el", "modo", "competitivo", "desafía", "las", "habilidades", "de", "los", "jugadores"],
            ["la", "campaña", "es", "la", "historia", "principal", "del", "juego"],
            ["la", "historia", "inmersa", "al", "jugador", "en", "el", "mundo", "del", "juego"],
            ["los", "logros", "reconocen", "el", "progreso", "del", "jugador"],
            ["los", "trofeos", "son", "recompensas", "por", "completar", "objetivos"],
            ["los", "achievements", "registran", "los", "logros", "del", "jugador"],
            ["el", "speedrun", "consiste", "en", "completar", "el", "juego", "lo", "más", "rápido", "posible"],
            ["los", "easter", "eggs", "son", "referencias", "ocultas", "en", "el", "juego"],
            
            # Frases conversacionales sobre videojuegos
            ["me", "gusta", "jugar", "videojuegos", "en", "mi", "tiempo", "libre"],
            ["los", "videojuegos", "son", "una", "forma", "de", "entretenimiento", "interactivo"],
            ["jugar", "videojuegos", "me", "ayuda", "a", "relajarme", "y", "divertirme"],
            ["los", "videojuegos", "pueden", "enseñar", "habilidades", "y", "conocimientos"],
            ["me", "encanta", "explorar", "mundos", "virtuales", "en", "los", "videojuegos"],
            ["los", "videojuegos", "multijugador", "me", "permiten", "conectar", "con", "amigos"],
            ["jugar", "videojuegos", "es", "una", "experiencia", "inmersiva", "y", "emocionante"],
            ["los", "videojuegos", "indie", "ofrecen", "experiencias", "únicas", "y", "creativas"],
            ["me", "gusta", "completar", "logros", "y", "desbloquear", "contenido", "nuevo"],
            ["los", "videojuegos", "de", "realidad", "virtual", "son", "increíblemente", "inmersivos"],
            ["jugar", "videojuegos", "me", "ayuda", "a", "mejorar", "mi", "coordinación", "y", "reflejos"],
            ["los", "videojuegos", "pueden", "contar", "historias", "emocionantes", "y", "profundas"],
            ["me", "encanta", "la", "música", "y", "los", "efectos", "sonoros", "de", "los", "videojuegos"],
            ["los", "videojuegos", "de", "estrategia", "desafían", "mi", "capacidad", "de", "planificación"],
            ["jugar", "videojuegos", "es", "una", "forma", "de", "arte", "interactivo"],
            ["los", "videojuegos", "pueden", "ser", "educativos", "y", "divertidos", "al", "mismo", "tiempo"],
            ["me", "gusta", "coleccionar", "videojuegos", "y", "descubrir", "nuevos", "títulos"],
            ["los", "videojuegos", "retro", "tienen", "un", "encanto", "especial", "y", "nostálgico"],
            ["jugar", "videojuegos", "me", "permite", "vivir", "aventuras", "imposibles", "en", "la", "vida", "real"],
            ["los", "videojuegos", "son", "una", "industria", "en", "constante", "evolución", "y", "crecimiento"],
        ]
        
        logger.info(f"Corpus creado con {len(gaming_sentences)} oraciones")
        return gaming_sentences
    
    def train_model(self, sentences: Optional[List[List[str]]] = None) -> bool:
        """
        Entrena el modelo Word2Vec con el corpus de videojuegos.
        
        Args:
            sentences (Optional[List[List[str]]]): Oraciones para entrenar. Si es None, usa el corpus por defecto.
            
        Returns:
            bool: True si el entrenamiento fue exitoso
        """
        if not GENSIM_AVAILABLE:
            logger.error("Gensim no está disponible. Instala con: pip install gensim")
            return False
        
        try:
            if sentences is None:
                sentences = self._create_gaming_corpus()
            
            logger.info("Iniciando entrenamiento del modelo Word2Vec...")
            
            # Configuración del modelo Word2Vec
            self.model = Word2Vec(
                sentences=sentences,
                vector_size=100,        # Dimensión de los vectores
                window=5,              # Ventana de contexto
                min_count=1,          # Frecuencia mínima de palabras
                workers=4,            # Número de hilos
                epochs=100,           # Número de épocas de entrenamiento
                sg=1,                 # Skip-gram (1) o CBOW (0)
                negative=5,           # Muestreo negativo
                ns_exponent=0.75,     # Exponente para muestreo negativo
                alpha=0.025,         # Tasa de aprendizaje inicial
                min_alpha=0.0001,     # Tasa de aprendizaje mínima
                seed=42               # Semilla para reproducibilidad
            )
            
            # Construir vocabulario
            self.vocabulary = set(self.model.wv.key_to_index.keys())
            self.is_trained = True
            
            # Guardar modelo
            self._save_model()
            
            logger.info(f"Modelo entrenado exitosamente. Vocabulario: {len(self.vocabulary)} palabras")
            return True
            
        except Exception as e:
            logger.error(f"Error durante el entrenamiento: {str(e)}")
            return False
    
    def _save_model(self) -> bool:
        """
        Guarda el modelo entrenado en disco.
        
        Returns:
            bool: True si se guardó exitosamente
        """
        try:
            if self.model is not None:
                self.model.save(self.model_path)
                logger.info(f"Modelo guardado en: {self.model_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error al guardar el modelo: {str(e)}")
            return False
    
    def _load_model(self) -> bool:
        """
        Carga un modelo previamente entrenado desde disco.
        
        Returns:
            bool: True si se cargó exitosamente
        """
        try:
            if os.path.exists(self.model_path):
                self.model = Word2Vec.load(self.model_path)
                self.vocabulary = set(self.model.wv.key_to_index.keys())
                self.is_trained = True
                logger.info(f"Modelo cargado desde: {self.model_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error al cargar el modelo: {str(e)}")
            return False
    
    def get_word_vector(self, word: str) -> Optional[np.ndarray]:
        """
        Obtiene el vector de una palabra específica.
        
        Args:
            word (str): Palabra para obtener su vector
            
        Returns:
            Optional[np.ndarray]: Vector de la palabra o None si no existe
        """
        if not self.is_trained or self.model is None:
            logger.warning("Modelo no entrenado")
            return None
        
        word_lower = word.lower()
        if word_lower in self.vocabulary:
            return self.model.wv[word_lower]
        else:
            logger.warning(f"Palabra '{word}' no encontrada en el vocabulario")
            return None
    
    def calculate_similarity(self, word1: str, word2: str) -> Optional[float]:
        """
        Calcula la similitud coseno entre dos palabras.
        
        Args:
            word1 (str): Primera palabra
            word2 (str): Segunda palabra
            
        Returns:
            Optional[float]: Similitud coseno (0-1) o None si hay error
        """
        if not self.is_trained or self.model is None:
            logger.warning("Modelo no entrenado")
            return None
        
        try:
            word1_lower = word1.lower()
            word2_lower = word2.lower()
            
            if word1_lower not in self.vocabulary or word2_lower not in self.vocabulary:
                logger.warning(f"Una o ambas palabras no están en el vocabulario: {word1}, {word2}")
                return None
            
            similarity = self.model.wv.similarity(word1_lower, word2_lower)
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Error al calcular similitud: {str(e)}")
            return None
    
    def get_most_similar(self, word: str, topn: int = 5) -> List[Tuple[str, float]]:
        """
        Obtiene las palabras más similares a una palabra dada.
        
        Args:
            word (str): Palabra de referencia
            topn (int): Número de palabras similares a devolver
            
        Returns:
            List[Tuple[str, float]]: Lista de tuplas (palabra, similitud)
        """
        if not self.is_trained or self.model is None:
            logger.warning("Modelo no entrenado")
            return []
        
        try:
            word_lower = word.lower()
            if word_lower not in self.vocabulary:
                logger.warning(f"Palabra '{word}' no encontrada en el vocabulario")
                return []
            
            similar_words = self.model.wv.most_similar(word_lower, topn=topn)
            return [(word, float(similarity)) for word, similarity in similar_words]
            
        except Exception as e:
            logger.error(f"Error al obtener palabras similares: {str(e)}")
            return []
    
    def get_similar_terms(self, word: str, topn: int = 5) -> List[Dict[str, Any]]:
        """
        Obtiene términos similares con información adicional.
        
        Args:
            word (str): Palabra de referencia
            topn (int): Número de términos similares a devolver
            
        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con información de términos similares
        """
        similar_words = self.get_most_similar(word, topn)
        
        results = []
        for i, (similar_word, similarity) in enumerate(similar_words, 1):
            results.append({
                'rank': i,
                'word': similar_word,
                'similarity': similarity,
                'similarity_percentage': round(similarity * 100, 2),
                'vector': self.get_word_vector(similar_word).tolist() if self.get_word_vector(similar_word) is not None else None
            })
        
        return results
    
    def analyze_text_similarities(self, text: str) -> Dict[str, Any]:
        """
        Analiza las similitudes semánticas en un texto.
        
        Args:
            text (str): Texto a analizar
            
        Returns:
            Dict[str, Any]: Análisis de similitudes semánticas
        """
        if not self.is_trained or self.model is None:
            return {
                'error': 'Modelo no entrenado',
                'similarities': [],
                'most_similar_pairs': []
            }
        
        # Tokenizar el texto
        words = text.lower().split()
        gaming_words = [word for word in words if word in self.vocabulary]
        
        if len(gaming_words) < 2:
            return {
                'gaming_words_found': gaming_words,
                'similarities': [],
                'most_similar_pairs': [],
                'message': 'Se necesitan al menos 2 palabras del vocabulario gaming'
            }
        
        # Calcular similitudes entre todas las palabras
        similarities = []
        for i, word1 in enumerate(gaming_words):
            for j, word2 in enumerate(gaming_words[i+1:], i+1):
                similarity = self.calculate_similarity(word1, word2)
                if similarity is not None:
                    similarities.append({
                        'word1': word1,
                        'word2': word2,
                        'similarity': similarity,
                        'similarity_percentage': round(similarity * 100, 2)
                    })
        
        # Ordenar por similitud
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        
        # Obtener los pares más similares
        most_similar_pairs = similarities[:3] if similarities else []
        
        return {
            'gaming_words_found': gaming_words,
            'total_similarities': len(similarities),
            'similarities': similarities,
            'most_similar_pairs': most_similar_pairs,
            'average_similarity': round(sum(s['similarity'] for s in similarities) / len(similarities), 3) if similarities else 0
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Obtiene información sobre el modelo entrenado.
        
        Returns:
            Dict[str, Any]: Información del modelo
        """
        if not self.is_trained or self.model is None:
            return {
                'is_trained': False,
                'model_path': self.model_path,
                'vocabulary_size': 0,
                'vector_size': 0
            }
        
        return {
            'is_trained': True,
            'model_path': self.model_path,
            'vocabulary_size': len(self.vocabulary),
            'vector_size': self.model.wv.vector_size,
            'total_words': self.model.corpus_total_words,
            'epochs': self.model.epochs,
            'window': self.model.window,
            'min_count': self.model.min_count
        }


def create_semantic_embeddings() -> SemanticEmbeddings:
    """
    Función de conveniencia para crear una instancia de SemanticEmbeddings.
    
    Returns:
        SemanticEmbeddings: Instancia configurada del módulo de embeddings
    """
    return SemanticEmbeddings()


def get_similar_terms_for_word(word: str, topn: int = 5) -> List[Dict[str, Any]]:
    """
    Función de conveniencia para obtener términos similares a una palabra.
    
    Args:
        word (str): Palabra de referencia
        topn (int): Número de términos similares a devolver
        
    Returns:
        List[Dict[str, Any]]: Lista de términos similares
    """
    embeddings = create_semantic_embeddings()
    
    # Si el modelo no está entrenado, entrenarlo
    if not embeddings.is_trained:
        logger.info("Modelo no encontrado, entrenando...")
        embeddings.train_model()
    
    return embeddings.get_similar_terms(word, topn)


def analyze_gaming_text_similarities(text: str) -> Dict[str, Any]:
    """
    Función de conveniencia para analizar similitudes en texto de videojuegos.
    
    Args:
        text (str): Texto a analizar
        
    Returns:
        Dict[str, Any]: Análisis de similitudes semánticas
    """
    embeddings = create_semantic_embeddings()
    
    # Si el modelo no está entrenado, entrenarlo
    if not embeddings.is_trained:
        logger.info("Modelo no encontrado, entrenando...")
        embeddings.train_model()
    
    return embeddings.analyze_text_similarities(text)


if __name__ == "__main__":
    # Ejemplo de uso del módulo
    print("=== Módulo de Embeddings Semánticos para Videojuegos ===")
    
    # Crear instancia
    embeddings = create_semantic_embeddings()
    
    # Entrenar modelo si no existe
    if not embeddings.is_trained:
        print("Entrenando modelo...")
        success = embeddings.train_model()
        if not success:
            print("Error al entrenar el modelo")
            exit(1)
    
    # Mostrar información del modelo
    info = embeddings.get_model_info()
    print(f"\nInformación del modelo:")
    print(f"- Entrenado: {info['is_trained']}")
    print(f"- Vocabulario: {info['vocabulary_size']} palabras")
    print(f"- Dimensión de vectores: {info['vector_size']}")
    
    # Ejemplos de uso
    test_words = ["rpg", "acción", "nintendo", "minecraft", "multijugador"]
    
    print(f"\n=== Ejemplos de términos similares ===")
    for word in test_words:
        similar_terms = embeddings.get_similar_terms(word, topn=3)
        print(f"\nPalabra: '{word}'")
        for term in similar_terms:
            print(f"  {term['rank']}. {term['word']} (similitud: {term['similarity_percentage']}%)")
    
    # Ejemplo de análisis de texto
    test_text = "me gusta jugar rpg de acción en nintendo switch"
    print(f"\n=== Análisis de similitudes en texto ===")
    print(f"Texto: '{test_text}'")
    analysis = embeddings.analyze_text_similarities(test_text)
    print(f"Palabras gaming encontradas: {analysis['gaming_words_found']}")
    print(f"Pares más similares:")
    for pair in analysis['most_similar_pairs']:
        print(f"  {pair['word1']} - {pair['word2']}: {pair['similarity_percentage']}%")
