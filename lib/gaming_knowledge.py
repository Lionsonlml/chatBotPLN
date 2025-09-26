'''
Módulo de Conocimiento sobre Videojuegos
Contiene información, vocabulario y respuestas relacionadas con videojuegos
para ser utilizado por el chatbot de PLN especializado en videojuegos.
'''

from typing import Dict, List, Tuple, Any
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importar módulo de embeddings semánticos
try:
    from semantic_embeddings import SemanticEmbeddings, get_similar_terms_for_word, analyze_gaming_text_similarities
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    try:
        from .semantic_embeddings import SemanticEmbeddings, get_similar_terms_for_word, analyze_gaming_text_similarities
        EMBEDDINGS_AVAILABLE = True
    except ImportError:
        logger.warning("Módulo de embeddings semánticos no disponible")
        EMBEDDINGS_AVAILABLE = False

# Vocabulario de videojuegos (palabras clave y sus categorías)
GAMING_VOCABULARY = {
    # Géneros de videojuegos
    'acción': 'género',
    'aventura': 'género',
    'rpg': 'género',
    'estrategia': 'género',
    'shooter': 'género',
    'fps': 'género',
    'mmorpg': 'género',
    'simulación': 'género',
    'deportes': 'género',
    'carreras': 'género',
    'puzzle': 'género',
    'plataformas': 'género',
    'roguelike': 'género',
    'metroidvania': 'género',
    'battle royale': 'género',
    'moba': 'género',
    'sandbox': 'género',
    'mundo abierto': 'género',
    'survival': 'género',
    'terror': 'género',
    'horror': 'género',
    
    # Plataformas
    'pc': 'plataforma',
    'playstation': 'plataforma',
    'ps4': 'plataforma',
    'ps5': 'plataforma',
    'xbox': 'plataforma',
    'xbox one': 'plataforma',
    'xbox series': 'plataforma',
    'nintendo': 'plataforma',
    'switch': 'plataforma',
    'móvil': 'plataforma',
    'android': 'plataforma',
    'ios': 'plataforma',
    
    # Compañías y desarrolladores
    'nintendo': 'compañía',
    'sony': 'compañía',
    'microsoft': 'compañía',
    'ubisoft': 'compañía',
    'ea': 'compañía',
    'electronic arts': 'compañía',
    'activision': 'compañía',
    'blizzard': 'compañía',
    'rockstar': 'compañía',
    'valve': 'compañía',
    'bethesda': 'compañía',
    'capcom': 'compañía',
    'square enix': 'compañía',
    'konami': 'compañía',
    'sega': 'compañía',
    'bandai namco': 'compañía',
    'cd projekt': 'compañía',
    'epic games': 'compañía',
    'riot games': 'compañía',
    
    # Juegos populares
    'minecraft': 'juego',
    'fortnite': 'juego',
    'call of duty': 'juego',
    'gta': 'juego',
    'grand theft auto': 'juego',
    'fifa': 'juego',
    'the legend of zelda': 'juego',
    'mario': 'juego',
    'super mario': 'juego',
    'pokemon': 'juego',
    'overwatch': 'juego',
    'league of legends': 'juego',
    'dota': 'juego',
    'world of warcraft': 'juego',
    'the witcher': 'juego',
    'dark souls': 'juego',
    'elden ring': 'juego',
    'cyberpunk': 'juego',
    'assassin\'s creed': 'juego',
    'red dead redemption': 'juego',
    'halo': 'juego',
    'god of war': 'juego',
    'horizon': 'juego',
    'final fantasy': 'juego',
    'resident evil': 'juego',
    'valorant': 'juego',
    'apex legends': 'juego',
    'among us': 'juego',
    'roblox': 'juego',
    
    # Términos técnicos
    'fps': 'técnico',
    'gráficos': 'técnico',
    'resolución': 'técnico',
    'hdr': 'técnico',
    'ray tracing': 'técnico',
    'dlss': 'técnico',
    'latencia': 'técnico',
    'ping': 'técnico',
    'lag': 'técnico',
    'bug': 'técnico',
    'glitch': 'técnico',
    'parche': 'técnico',
    'actualización': 'técnico',
    'dlc': 'técnico',
    'expansión': 'técnico',
    'mod': 'técnico',
    'shader': 'técnico',
    'textura': 'técnico',
    'renderizado': 'técnico',
    
    # Términos de gameplay
    'nivel': 'gameplay',
    'misión': 'gameplay',
    'quest': 'gameplay',
    'jefe': 'gameplay',
    'boss': 'gameplay',
    'npc': 'gameplay',
    'personaje': 'gameplay',
    'inventario': 'gameplay',
    'habilidad': 'gameplay',
    'skill': 'gameplay',
    'arma': 'gameplay',
    'equipo': 'gameplay',
    'crafteo': 'gameplay',
    'crafting': 'gameplay',
    'farmeo': 'gameplay',
    'farming': 'gameplay',
    'loot': 'gameplay',
    'botín': 'gameplay',
    'pvp': 'gameplay',
    'pve': 'gameplay',
    'multijugador': 'gameplay',
    'cooperativo': 'gameplay',
    'competitivo': 'gameplay',
    'campaña': 'gameplay',
    'historia': 'gameplay',
    'logro': 'gameplay',
    'trofeo': 'gameplay',
    'achievement': 'gameplay',
    'speedrun': 'gameplay',
    'easter egg': 'gameplay',
}

# Respuestas temáticas sobre videojuegos
GAMING_RESPONSES = {
    'general': [
        "Los videojuegos son una forma de entretenimiento interactivo que ha evolucionado enormemente desde sus inicios. ¿Qué aspecto te interesa más?",
        "El mundo de los videojuegos es muy amplio, abarcando desde juegos indie hasta grandes producciones AAA. ¿Tienes algún género favorito?",
        "Los videojuegos combinan narrativa, arte, música y tecnología de formas únicas. ¿Qué juegos has disfrutado recientemente?",
        "La industria de los videojuegos genera más ingresos que la música y el cine combinados. ¿Qué plataforma utilizas para jugar?",
        "Los videojuegos pueden ser experiencias solitarias profundas o conectar a millones de personas en todo el mundo. ¿Prefieres jugar solo o en multijugador?",
    ],
    
    'géneros': [
        "Los géneros de videojuegos incluyen acción, aventura, RPG, estrategia, simulación, deportes, y muchos más. Cada uno ofrece experiencias muy diferentes.",
        "Los RPG (juegos de rol) te permiten desarrollar personajes a lo largo de extensas historias, mientras que los FPS se centran en la acción en primera persona.",
        "Los juegos de mundo abierto como GTA o The Witcher ofrecen libertad para explorar, mientras que los roguelikes como Hades o Dead Cells se basan en partidas cortas con alta rejugabilidad.",
        "Los MOBA como League of Legends y los Battle Royale como Fortnite han dominado la escena competitiva en los últimos años.",
        "Los juegos de plataformas como Mario siguen siendo populares décadas después de su creación, mostrando que el buen diseño de niveles es atemporal.",
    ],
    
    'plataformas': [
        "Las principales plataformas de juego actuales son PC, PlayStation 5, Xbox Series X/S y Nintendo Switch, cada una con sus exclusivos y ventajas.",
        "El PC ofrece la mayor versatilidad y potencia gráfica, mientras que las consolas proporcionan una experiencia más accesible y optimizada.",
        "El gaming móvil ha crecido enormemente, con títulos como Genshin Impact demostrando que los juegos de alta calidad también pueden funcionar en smartphones.",
        "La retrocompatibilidad es una característica importante en las consolas modernas, permitiéndote jugar a títulos de generaciones anteriores.",
        "Las plataformas de streaming como Xbox Cloud Gaming y GeForce Now están cambiando la forma en que accedemos a los juegos, eliminando la necesidad de hardware potente.",
    ],
    
    'tecnología': [
        "Los avances en ray tracing están revolucionando los gráficos de los videojuegos, creando iluminación y reflejos mucho más realistas.",
        "Las tecnologías como DLSS de NVIDIA utilizan IA para mejorar el rendimiento sin sacrificar la calidad visual.",
        "Los SSD de alta velocidad en las consolas de nueva generación han reducido drásticamente los tiempos de carga y permiten mundos más detallados.",
        "La realidad virtual (VR) y aumentada (AR) están creando nuevas formas de interactuar con los videojuegos, aumentando la inmersión.",
        "El audio 3D y las características hápticas de controladores como el DualSense de PS5 añaden nuevas dimensiones a la experiencia de juego.",
    ],
    
    'industria': [
        "La industria de los videojuegos está en constante evolución, con nuevos modelos de negocio como el free-to-play y los servicios de suscripción.",
        "Los estudios indie han florecido en la última década, creando algunos de los juegos más innovadores y aclamados por la crítica.",
        "Las adquisiciones de estudios por parte de grandes compañías como Microsoft (Bethesda, Activision Blizzard) están cambiando el panorama de la industria.",
        "Los eventos como E3, Gamescom y The Game Awards son momentos clave donde se anuncian los nuevos títulos y tendencias.",
        "El desarrollo de videojuegos es un proceso complejo que puede llevar años y requiere equipos multidisciplinares de programadores, artistas, diseñadores y más.",
    ],
    
    'cultura': [
        "Los esports han crecido hasta convertirse en un fenómeno global con millones de espectadores y premios millonarios.",
        "Los streamers y creadores de contenido han transformado cómo descubrimos y experimentamos los videojuegos.",
        "Los videojuegos han inspirado películas, series, libros y otros medios, demostrando su impacto cultural.",
        "Muchos videojuegos exploran temas profundos como la ética, la filosofía, la política y las relaciones humanas.",
        "Las comunidades de modding extienden la vida de los juegos creando nuevo contenido y mejoras para títulos existentes.",
    ],
    
    'fuera_de_tema': [
        "Estamos hablando de videojuegos. Si tienes alguna pregunta o comentario sobre juegos, consolas, o la industria gaming, estaré encantado de seguir la conversación.",
        "Parece que nos estamos desviando del tema de los videojuegos. ¿Te gustaría que volvamos a hablar sobre algún aspecto del mundo gaming?",
        "Como especialista en videojuegos, puedo ofrecerte información sobre juegos, plataformas, géneros y más. ¿Hay algo específico del mundo gaming que te interese?",
        "Mi conocimiento se centra en videojuegos. Si quieres hablar de otro tema, puedo intentar relacionarlo con el mundo de los videojuegos si es posible.",
        "Estoy especializado en conversar sobre videojuegos. ¿Quieres que hablemos sobre algún juego, consola o tendencia reciente en la industria?",
    ]
}

# Información sobre juegos específicos
GAME_INFO = {
    'minecraft': {
        'descripción': 'Juego sandbox de mundo abierto donde puedes construir, explorar y sobrevivir.',
        'desarrollador': 'Mojang Studios',
        'año': 2011,
        'plataformas': ['PC', 'Consolas', 'Móvil'],
        'género': 'Sandbox, Supervivencia',
    },
    'fortnite': {
        'descripción': 'Battle royale gratuito con elementos de construcción y eventos en vivo.',
        'desarrollador': 'Epic Games',
        'año': 2017,
        'plataformas': ['PC', 'Consolas', 'Móvil'],
        'género': 'Battle Royale, Shooter',
    },
    'the legend of zelda': {
        'descripción': 'Serie de aventuras épicas en el mundo de Hyrule, protagonizada por Link.',
        'desarrollador': 'Nintendo',
        'año': 1986,
        'plataformas': ['Consolas Nintendo'],
        'género': 'Acción-Aventura',
    },
    'grand theft auto': {
        'descripción': 'Serie de mundo abierto ambientada en ciudades ficticias inspiradas en lugares reales.',
        'desarrollador': 'Rockstar Games',
        'año': 1997,
        'plataformas': ['PC', 'Consolas'],
        'género': 'Acción-Aventura, Mundo Abierto',
    },
    'call of duty': {
        'descripción': 'Serie de shooters en primera persona con modos campaña y multijugador.',
        'desarrollador': 'Activision (varios estudios)',
        'año': 2003,
        'plataformas': ['PC', 'Consolas'],
        'género': 'FPS, Shooter',
    },
}

def is_gaming_related(text: str) -> bool:
    """Determina si un texto está relacionado con videojuegos."""
    text_lower = text.lower()
    
    # Buscar palabras clave de videojuegos en el texto
    for keyword in GAMING_VOCABULARY.keys():
        if keyword in text_lower:
            return True
    
    # Buscar nombres de juegos específicos
    for game in GAME_INFO.keys():
        if game in text_lower:
            return True
    
    return False

def get_gaming_response(text: str) -> str:
    """Genera una respuesta relacionada con videojuegos basada en el texto de entrada."""
    text_lower = text.lower()
    
    # Verificar si el texto está relacionado con videojuegos
    if not is_gaming_related(text_lower):
        # Si no está relacionado, devolver una respuesta que redirija al tema de videojuegos
        import random
        return random.choice(GAMING_RESPONSES['fuera_de_tema'])
    
    # Buscar menciones de juegos específicos
    for game, info in GAME_INFO.items():
        if game in text_lower:
            base_response = f"{info['descripción']} Desarrollado por {info['desarrollador']} en {info['año']}, está disponible para {', '.join(info['plataformas'])} y pertenece al género {info['género']}."
            # Enriquecer con análisis semántico
            return enhance_gaming_response_with_semantics(text, base_response)
    
    # Identificar la categoría más relevante basada en palabras clave
    categories = {
        'géneros': 0,
        'plataformas': 0,
        'tecnología': 0,
        'industria': 0,
        'cultura': 0,
    }
    
    for keyword, category in GAMING_VOCABULARY.items():
        if keyword in text_lower:
            if category == 'género':
                categories['géneros'] += 1
            elif category == 'plataforma':
                categories['plataformas'] += 1
            elif category == 'técnico':
                categories['tecnología'] += 1
            elif category == 'compañía':
                categories['industria'] += 1
            elif category in ['gameplay', 'juego']:
                # Distribuir entre varias categorías
                categories['géneros'] += 0.5
                categories['cultura'] += 0.5
    
    # Determinar la categoría más relevante
    max_category = max(categories.items(), key=lambda x: x[1])
    
    # Si no hay una categoría clara, usar respuesta general
    if max_category[1] == 0:
        import random
        base_response = random.choice(GAMING_RESPONSES['general'])
    else:
        # Devolver respuesta de la categoría más relevante
        import random
        base_response = random.choice(GAMING_RESPONSES[max_category[0]])
    
    # Enriquecer con análisis semántico
    return enhance_gaming_response_with_semantics(text, base_response)

def analyze_gaming_content(text: str) -> Dict[str, Any]:
    """Analiza el contenido relacionado con videojuegos en un texto."""
    text_lower = text.lower()
    result = {
        'is_gaming_related': is_gaming_related(text_lower),
        'keywords': [],
        'games_mentioned': [],
        'categories': {},
        'semantic_analysis': None,
        'similar_terms': []
    }
    
    # Extraer palabras clave de videojuegos
    for keyword, category in GAMING_VOCABULARY.items():
        if keyword in text_lower:
            result['keywords'].append({
                'word': keyword,
                'category': category
            })
            
            # Actualizar conteo de categorías
            if category not in result['categories']:
                result['categories'][category] = 0
            result['categories'][category] += 1
    
    # Identificar juegos mencionados
    for game in GAME_INFO.keys():
        if game in text_lower:
            result['games_mentioned'].append(game)
    
    # Análisis semántico con embeddings si está disponible
    if EMBEDDINGS_AVAILABLE:
        try:
            # Análisis de similitudes semánticas
            semantic_analysis = analyze_gaming_text_similarities(text)
            result['semantic_analysis'] = semantic_analysis
            
            # Obtener términos similares para las palabras clave encontradas
            for keyword_info in result['keywords']:
                word = keyword_info['word']
                similar_terms = get_similar_terms_for_word(word, topn=3)
                result['similar_terms'].extend(similar_terms)
            
        except Exception as e:
            logger.error(f"Error en análisis semántico: {str(e)}")
            result['semantic_analysis'] = {'error': str(e)}
    
    return result

def get_semantic_similar_terms(word: str, topn: int = 5) -> List[Dict[str, Any]]:
    """
    Obtiene términos semánticamente similares a una palabra usando embeddings.
    
    Args:
        word (str): Palabra de referencia
        topn (int): Número de términos similares a devolver
        
    Returns:
        List[Dict[str, Any]]: Lista de términos similares con información adicional
    """
    if not EMBEDDINGS_AVAILABLE:
        logger.warning("Embeddings semánticos no disponibles")
        return []
    
    try:
        return get_similar_terms_for_word(word, topn)
    except Exception as e:
        logger.error(f"Error al obtener términos similares: {str(e)}")
        return []

def enhance_gaming_response_with_semantics(text: str, base_response: str) -> str:
    """
    Enriquece una respuesta de videojuegos usando análisis semántico.
    
    Args:
        text (str): Texto del usuario
        base_response (str): Respuesta base del chatbot
        
    Returns:
        str: Respuesta enriquecida con información semántica
    """
    if not EMBEDDINGS_AVAILABLE:
        return base_response
    
    try:
        # Obtener análisis semántico
        analysis = analyze_gaming_content(text)
        
        if not analysis.get('semantic_analysis'):
            return base_response
        
        semantic_info = analysis['semantic_analysis']
        
        # Si hay términos similares interesantes, mencionarlos
        if semantic_info.get('most_similar_pairs'):
            similar_pairs = semantic_info['most_similar_pairs'][:2]  # Top 2 pares
            similar_text = " Por cierto, veo que mencionas conceptos relacionados como "
            similar_concepts = []
            
            for pair in similar_pairs:
                if pair['similarity_percentage'] > 60:  # Solo si la similitud es alta
                    similar_concepts.append(f"{pair['word1']} y {pair['word2']}")
            
            if similar_concepts:
                similar_text += ", ".join(similar_concepts) + "."
                base_response += similar_text
        
        # Si hay términos similares específicos, sugerir exploración
        if analysis.get('similar_terms'):
            top_terms = analysis['similar_terms'][:3]
            if top_terms:
                suggestions = []
                for term in top_terms:
                    if term['similarity_percentage'] > 70:
                        suggestions.append(term['word'])
                
                if suggestions:
                    suggestion_text = f" También podrías estar interesado en: {', '.join(suggestions)}."
                    base_response += suggestion_text
        
        return base_response
        
    except Exception as e:
        logger.error(f"Error al enriquecer respuesta: {str(e)}")
        return base_response