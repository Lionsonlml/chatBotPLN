#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador NLP simplificado que funciona sin gensim
"""

import sys
import json
import re

def tokenize_text(text):
    """Tokenización básica"""
    # Limpiar texto y dividir en tokens
    text = text.lower()
    # Remover caracteres especiales excepto letras, números y espacios
    text = re.sub(r'[^\w\sáéíóúüñ]', ' ', text)
    tokens = text.split()
    return [token for token in tokens if len(token) > 0]

def lemmatize_tokens(tokens):
    """Lematización básica usando reglas"""
    lemmas = []
    
    # Diccionario básico de lemas
    lemma_dict = {
        # Verbos conjugados
        'corro': 'correr', 'corres': 'correr', 'corre': 'correr', 'corremos': 'correr', 'corren': 'correr',
        'como': 'comer', 'comes': 'comer', 'come': 'comer', 'comemos': 'comer', 'comen': 'comer',
        'hablo': 'hablar', 'hablas': 'hablar', 'habla': 'hablar', 'hablamos': 'hablar', 'hablan': 'hablar',
        'estudio': 'estudiar', 'estudias': 'estudiar', 'estudia': 'estudiar', 'estudiamos': 'estudiar', 'estudian': 'estudiar',
        'trabajo': 'trabajar', 'trabajas': 'trabajar', 'trabaja': 'trabajar', 'trabajamos': 'trabajar', 'trabajan': 'trabajar',
        'juego': 'jugar', 'juegas': 'jugar', 'juega': 'jugar', 'jugamos': 'jugar', 'juegan': 'jugar',
        'leo': 'leer', 'lees': 'leer', 'lee': 'leer', 'leemos': 'leer', 'leen': 'leer',
        'escribo': 'escribir', 'escribes': 'escribir', 'escribe': 'escribir', 'escribimos': 'escribir', 'escriben': 'escribir',
        
        # Gerundios
        'corriendo': 'correr', 'comiendo': 'comer', 'hablando': 'hablar', 'estudiando': 'estudiar',
        'trabajando': 'trabajar', 'jugando': 'jugar', 'leyendo': 'leer', 'escribiendo': 'escribir',
        
        # Sustantivos plurales
        'casas': 'casa', 'libros': 'libro', 'niños': 'niño', 'niñas': 'niña',
        'mujeres': 'mujer', 'hombres': 'hombre', 'estudiantes': 'estudiante',
        'profesores': 'profesor', 'universidades': 'universidad', 'escuelas': 'escuela',
        
        # Adjetivos
        'pequeña': 'pequeño', 'pequeñas': 'pequeño', 'pequeños': 'pequeño',
        'buena': 'bueno', 'buenas': 'bueno', 'buenos': 'bueno',
        'grande': 'grande', 'grandes': 'grande',
        
        # Adverbios
        'rápidamente': 'rápido', 'lentamente': 'lento', 'fácilmente': 'fácil',
        'claramente': 'claro', 'perfectamente': 'perfecto'
    }
    
    for token in tokens:
        # Verificar diccionario primero
        if token in lemma_dict:
            lemmas.append({'word': token, 'lemma': lemma_dict[token]})
            continue
            
        # Reglas morfológicas básicas
        lemma = token
        
        # Adverbios terminados en -mente
        if token.endswith('mente'):
            lemma = token[:-5]  # Quitar 'mente'
            if lemma.endswith('a'):
                lemma = lemma[:-1] + 'o'  # rápidamente -> rápido
        
        # Gerundios
        elif token.endswith('ando'):
            lemma = token[:-4] + 'ar'  # hablando -> hablar
        elif token.endswith('iendo'):
            lemma = token[:-5] + 'er'  # comiendo -> comer
        
        # Participios
        elif token.endswith('ado'):
            lemma = token[:-3] + 'ar'  # hablado -> hablar
        elif token.endswith('ido'):
            lemma = token[:-3] + 'er'  # comido -> comer
        
        # Plurales simples
        elif token.endswith('s') and len(token) > 3:
            lemma = token[:-1]  # libros -> libro
        
        lemmas.append({'word': token, 'lemma': lemma})
    
    return lemmas

def pos_tag_tokens(tokens):
    """POS tagging básico usando reglas"""
    pos_tags = []
    
    # Diccionario básico de POS tags
    pos_dict = {
        # Determinantes
        'el': 'DET', 'la': 'DET', 'los': 'DET', 'las': 'DET',
        'un': 'DET', 'una': 'DET', 'este': 'DET', 'esta': 'DET',
        'estos': 'DET', 'estas': 'DET', 'mi': 'DET', 'tu': 'DET',
        
        # Sustantivos
        'casa': 'NOUN', 'libro': 'NOUN', 'niño': 'NOUN', 'niña': 'NOUN',
        'mujer': 'NOUN', 'hombre': 'NOUN', 'estudiante': 'NOUN',
        'profesor': 'NOUN', 'universidad': 'NOUN', 'escuela': 'NOUN',
        'parque': 'NOUN', 'cocina': 'NOUN', 'gato': 'NOUN', 'perro': 'NOUN',
        'ciudad': 'NOUN', 'juego': 'NOUN', 'videojuego': 'NOUN',
        
        # Verbos
        'es': 'VERB', 'está': 'VERB', 'son': 'VERB', 'están': 'VERB',
        'tiene': 'VERB', 'tienen': 'VERB', 'hay': 'VERB',
        'come': 'VERB', 'comen': 'VERB', 'estudia': 'VERB', 'estudian': 'VERB',
        'trabaja': 'VERB', 'trabajan': 'VERB', 'juega': 'VERB', 'juegan': 'VERB',
        'lee': 'VERB', 'leen': 'VERB', 'escribe': 'VERB', 'escriben': 'VERB',
        
        # Adjetivos
        'grande': 'ADJ', 'pequeño': 'ADJ', 'bueno': 'ADJ', 'malo': 'ADJ',
        'nuevo': 'ADJ', 'viejo': 'ADJ', 'rojo': 'ADJ', 'azul': 'ADJ',
        'verde': 'ADJ', 'amarillo': 'ADJ', 'blanco': 'ADJ', 'negro': 'ADJ',
        
        # Adverbios
        'muy': 'ADV', 'más': 'ADV', 'menos': 'ADV', 'bien': 'ADV',
        'mal': 'ADV', 'aquí': 'ADV', 'allí': 'ADV', 'ahora': 'ADV',
        'después': 'ADV', 'antes': 'ADV', 'siempre': 'ADV', 'nunca': 'ADV',
        
        # Pronombres
        'yo': 'PRON', 'tú': 'PRON', 'él': 'PRON', 'ella': 'PRON',
        'nosotros': 'PRON', 'me': 'PRON', 'te': 'PRON', 'se': 'PRON',
        'nos': 'PRON', 'les': 'PRON',
        
        # Preposiciones
        'de': 'PREP', 'en': 'PREP', 'con': 'PREP', 'por': 'PREP',
        'para': 'PREP', 'sin': 'PREP', 'sobre': 'PREP', 'bajo': 'PREP',
        'desde': 'PREP', 'hasta': 'PREP', 'entre': 'PREP',
        
        # Conjunciones
        'y': 'CONJ', 'o': 'CONJ', 'pero': 'CONJ', 'aunque': 'CONJ',
        'porque': 'CONJ', 'si': 'CONJ', 'cuando': 'CONJ', 'donde': 'CONJ',
        'como': 'CONJ'
    }
    
    # Descripciones de POS tags
    pos_descriptions = {
        'NOUN': 'Sustantivo',
        'VERB': 'Verbo',
        'ADJ': 'Adjetivo',
        'ADV': 'Adverbio',
        'PRON': 'Pronombre',
        'DET': 'Determinante',
        'PREP': 'Preposición',
        'CONJ': 'Conjunción',
        'NUM': 'Número',
        'PUNCT': 'Puntuación'
    }
    
    for token in tokens:
        # Verificar diccionario primero
        if token in pos_dict:
            pos = pos_dict[token]
        else:
            # Reglas heurísticas
            if token.endswith('mente'):
                pos = 'ADV'
            elif token.endswith('ando') or token.endswith('iendo'):
                pos = 'VERB'
            elif token.endswith('ción') or token.endswith('sión') or token.endswith('dad') or token.endswith('tad'):
                pos = 'NOUN'
            elif token.endswith('oso') or token.endswith('osa') or token.endswith('ivo') or token.endswith('iva'):
                pos = 'ADJ'
            elif token.endswith('ar') or token.endswith('er') or token.endswith('ir'):
                pos = 'VERB'
            elif token.endswith('s') and len(token) > 2:
                pos = 'NOUN'
            else:
                pos = 'NOUN'  # Por defecto
        
        pos_tags.append({
            'word': token,
            'pos': pos,
            'description': pos_descriptions.get(pos, 'Desconocido')
        })
    
    return pos_tags

def analyze_gaming_content(text):
    """Análisis básico de contenido de videojuegos"""
    text_lower = text.lower()
    
    # Palabras clave de videojuegos
    gaming_keywords = [
        'juego', 'videojuego', 'gaming', 'consola', 'playstation', 'xbox', 'nintendo',
        'pc', 'steam', 'epic', 'mario', 'zelda', 'pokemon', 'fifa', 'call of duty',
        'fortnite', 'minecraft', 'roblox', 'among us', 'valorant', 'league of legends',
        'controles', 'mando', 'teclado', 'mouse', 'gráficos', 'fps', 'online',
        'multijugador', 'single player', 'campaign', 'modo historia'
    ]
    
    # Juegos populares
    popular_games = [
        'mario', 'zelda', 'pokemon', 'fifa', 'call of duty', 'fortnite', 'minecraft',
        'roblox', 'among us', 'valorant', 'league of legends', 'gta', 'witcher',
        'elden ring', 'god of war', 'spider-man', 'horizon', 'uncharted'
    ]
    
    # Detectar contenido gaming
    is_gaming_related = any(keyword in text_lower for keyword in gaming_keywords)
    
    # Encontrar juegos mencionados
    games_mentioned = [game for game in popular_games if game in text_lower]
    
    # Encontrar palabras clave
    keywords_found = [keyword for keyword in gaming_keywords if keyword in text_lower]
    keywords = [{'word': kw, 'category': 'gaming'} for kw in keywords_found]
    
    # Análisis semántico simulado
    semantic_analysis = {
        'gaming_words_found': keywords_found,
        'total_similarities': len(keywords_found),
        'similarities': [],
        'most_similar_pairs': [],
        'average_similarity': 0.8 if keywords_found else 0.0
    }
    
    return {
        'is_gaming_related': is_gaming_related,
        'keywords': keywords,
        'games_mentioned': games_mentioned,
        'categories': {'gaming': len(keywords_found)},
        'semantic_analysis': semantic_analysis,
        'similar_terms': []
    }

def main():
    """Función principal"""
    if len(sys.argv) < 2:
        result = {
            "error": "Texto requerido como parámetro"
        }
        print(json.dumps(result, ensure_ascii=False))
        return
    
    text = sys.argv[1]
    
    # Procesar texto
    tokens = tokenize_text(text)
    lemmas = lemmatize_tokens(tokens)
    pos_tags = pos_tag_tokens(tokens)
    gaming_analysis = analyze_gaming_content(text)
    
    # Crear resultado
    result = {
        'tokens': tokens,
        'lemmas': lemmas,
        'posTags': pos_tags,
        'gamingAnalysis': gaming_analysis
    }
    
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
