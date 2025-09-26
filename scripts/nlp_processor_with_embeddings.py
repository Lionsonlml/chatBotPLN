#!/usr/bin/env python3
"""
Script de Procesamiento de Lenguaje Natural con Embeddings Semánticos
====================================================================

Este script integra el procesamiento de PLN tradicional (tokenización, lematización, POS tagging)
con embeddings semánticos usando Word2Vec para análisis de videojuegos.

Funcionalidades:
- Tokenización y lematización con spaCy
- POS tagging
- Análisis de contenido de videojuegos
- Embeddings semánticos con Word2Vec
- Similitudes entre términos
- Integración completa del flujo de procesamiento

Autor: Asistente IA
Fecha: 2024
"""

import sys
import json
import logging
from pathlib import Path

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Agregar el directorio lib al path para importar módulos
sys.path.append(str(Path(__file__).parent.parent / "lib"))

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    logger.warning("spaCy no está disponible")
    SPACY_AVAILABLE = False

try:
    from gaming_knowledge import analyze_gaming_content, get_semantic_similar_terms
    from semantic_embeddings import SemanticEmbeddings
    EMBEDDINGS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Módulos de embeddings no disponibles: {e}")
    EMBEDDINGS_AVAILABLE = False

def load_spacy_model():
    """Carga el modelo de spaCy para procesamiento de PLN."""
    try:
        # Intentar cargar el modelo de español
        nlp = spacy.load("es_core_news_sm")
        logger.info("Modelo spaCy español cargado exitosamente")
        return nlp
    except OSError:
        try:
            # Fallback al modelo de inglés si el español no está disponible
            nlp = spacy.load("en_core_web_sm")
            logger.warning("Modelo español no disponible, usando modelo inglés")
            return nlp
        except OSError:
            logger.error("No se pudo cargar ningún modelo de spaCy")
            return None

def process_text_with_spacy(text: str, nlp) -> dict:
    """
    Procesa texto usando spaCy para tokenización, lematización y POS tagging.
    
    Args:
        text (str): Texto a procesar
        nlp: Modelo de spaCy cargado
        
    Returns:
        dict: Resultados del procesamiento
    """
    if nlp is None:
        return {
            'tokens': [],
            'lemmas': [],
            'pos_tags': [],
            'error': 'Modelo spaCy no disponible'
        }
    
    try:
        doc = nlp(text)
        
        # Tokenización
        tokens = [token.text for token in doc]
        
        # Lematización
        lemmas = []
        for token in doc:
            lemmas.append({
                'word': token.text,
                'lemma': token.lemma_,
                'context': token.sent.text if hasattr(token, 'sent') else None
            })
        
        # POS Tagging
        pos_tags = []
        for token in doc:
            pos_tags.append({
                'word': token.text,
                'pos': token.pos_,
                'description': spacy.explain(token.pos_) or 'Desconocido',
                'relationship': f"Head: {token.head.text}" if token.head != token else None
            })
        
        return {
            'tokens': tokens,
            'lemmas': lemmas,
            'pos_tags': pos_tags
        }
        
    except Exception as e:
        logger.error(f"Error en procesamiento spaCy: {str(e)}")
        return {
            'tokens': [],
            'lemmas': [],
            'pos_tags': [],
            'error': str(e)
        }

def process_text_with_embeddings(text: str) -> dict:
    """
    Procesa texto usando embeddings semánticos para análisis de videojuegos.
    
    Args:
        text (str): Texto a procesar
        
    Returns:
        dict: Análisis con embeddings semánticos
    """
    if not EMBEDDINGS_AVAILABLE:
        return {
            'error': 'Módulos de embeddings no disponibles',
            'gaming_analysis': None,
            'semantic_analysis': None
        }
    
    try:
        # Análisis de contenido de videojuegos con embeddings
        gaming_analysis = analyze_gaming_content(text)
        
        return {
            'gaming_analysis': gaming_analysis,
            'semantic_analysis': gaming_analysis.get('semantic_analysis'),
            'similar_terms': gaming_analysis.get('similar_terms', [])
        }
        
    except Exception as e:
        logger.error(f"Error en análisis con embeddings: {str(e)}")
        return {
            'error': str(e),
            'gaming_analysis': None,
            'semantic_analysis': None
        }

def main():
    """Función principal del script."""
    if len(sys.argv) < 2:
        print(json.dumps({
            'error': 'Se requiere texto como argumento',
            'usage': 'python nlp_processor_with_embeddings.py "texto a procesar"'
        }))
        sys.exit(1)
    
    text = sys.argv[1]
    
    if not text.strip():
        print(json.dumps({
            'error': 'El texto no puede estar vacío'
        }))
        sys.exit(1)
    
    logger.info(f"Procesando texto: '{text[:50]}...'")
    
    # Inicializar resultados
    result = {
        'text': text,
        'processing_method': 'spacy_with_embeddings',
        'tokens': [],
        'lemmas': [],
        'pos_tags': [],
        'gaming_analysis': None,
        'semantic_analysis': None,
        'similar_terms': [],
        'errors': []
    }
    
    # Procesamiento con spaCy
    if SPACY_AVAILABLE:
        nlp = load_spacy_model()
        if nlp:
            spacy_result = process_text_with_spacy(text, nlp)
            result.update({
                'tokens': spacy_result.get('tokens', []),
                'lemmas': spacy_result.get('lemmas', []),
                'pos_tags': spacy_result.get('pos_tags', [])
            })
            
            if 'error' in spacy_result:
                result['errors'].append(f"spaCy: {spacy_result['error']}")
        else:
            result['errors'].append("No se pudo cargar modelo spaCy")
    else:
        result['errors'].append("spaCy no está disponible")
    
    # Procesamiento con embeddings semánticos
    if EMBEDDINGS_AVAILABLE:
        embeddings_result = process_text_with_embeddings(text)
        
        result.update({
            'gaming_analysis': embeddings_result.get('gaming_analysis'),
            'semantic_analysis': embeddings_result.get('semantic_analysis'),
            'similar_terms': embeddings_result.get('similar_terms', [])
        })
        
        if 'error' in embeddings_result:
            result['errors'].append(f"Embeddings: {embeddings_result['error']}")
    else:
        result['errors'].append("Módulos de embeddings no disponibles")
    
    # Información adicional
    result['processing_info'] = {
        'spacy_available': SPACY_AVAILABLE,
        'embeddings_available': EMBEDDINGS_AVAILABLE,
        'total_tokens': len(result['tokens']),
        'gaming_related': result['gaming_analysis']['is_gaming_related'] if result['gaming_analysis'] else False
    }
    
    # Mostrar resultado
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
