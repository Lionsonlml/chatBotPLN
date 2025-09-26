#!/usr/bin/env python3
"""
Script de Prueba para Embeddings Semánticos
==========================================

Este script prueba todas las funcionalidades del módulo de embeddings semánticos
para asegurar que todo funciona correctamente.

Autor: Asistente IA
Fecha: 2024
"""

import sys
import logging
from pathlib import Path

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Agregar el directorio lib al path
sys.path.append(str(Path(__file__).parent.parent / "lib"))

def test_imports():
    """Prueba las importaciones necesarias."""
    logger.info("=== Probando Importaciones ===")
    
    try:
        from semantic_embeddings import SemanticEmbeddings, get_similar_terms_for_word, analyze_gaming_text_similarities
        logger.info("✓ Módulo semantic_embeddings importado correctamente")
        return True
    except ImportError as e:
        logger.error(f"✗ Error al importar semantic_embeddings: {e}")
        return False

def test_gaming_knowledge():
    """Prueba el módulo de conocimiento de videojuegos."""
    logger.info("=== Probando Gaming Knowledge ===")
    
    try:
        from gaming_knowledge import analyze_gaming_content, get_semantic_similar_terms, enhance_gaming_response_with_semantics
        logger.info("✓ Módulo gaming_knowledge importado correctamente")
        return True
    except ImportError as e:
        logger.error(f"✗ Error al importar gaming_knowledge: {e}")
        return False

def test_embeddings_basic():
    """Prueba funcionalidades básicas de embeddings."""
    logger.info("=== Probando Funcionalidades Básicas ===")
    
    try:
        from semantic_embeddings import SemanticEmbeddings
        
        # Crear instancia
        embeddings = SemanticEmbeddings()
        logger.info("✓ Instancia de SemanticEmbeddings creada")
        
        # Verificar si el modelo está entrenado
        if not embeddings.is_trained:
            logger.info("Modelo no entrenado, entrenando...")
            success = embeddings.train_model()
            if not success:
                logger.error("✗ Error al entrenar el modelo")
                return False
            logger.info("✓ Modelo entrenado exitosamente")
        else:
            logger.info("✓ Modelo ya está entrenado")
        
        # Probar obtención de información del modelo
        info = embeddings.get_model_info()
        logger.info(f"✓ Información del modelo: {info['vocabulary_size']} palabras, {info['vector_size']} dimensiones")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Error en funcionalidades básicas: {e}")
        return False

def test_similarity_calculation():
    """Prueba el cálculo de similitudes."""
    logger.info("=== Probando Cálculo de Similitudes ===")
    
    try:
        from semantic_embeddings import SemanticEmbeddings
        
        embeddings = SemanticEmbeddings()
        
        # Probar palabras conocidas
        test_pairs = [
            ("rpg", "aventura"),
            ("acción", "shooter"),
            ("nintendo", "switch"),
            ("minecraft", "construcción")
        ]
        
        for word1, word2 in test_pairs:
            similarity = embeddings.calculate_similarity(word1, word2)
            if similarity is not None:
                logger.info(f"✓ Similitud '{word1}' - '{word2}': {similarity:.3f}")
            else:
                logger.warning(f"⚠ No se pudo calcular similitud para '{word1}' - '{word2}'")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Error en cálculo de similitudes: {e}")
        return False

def test_similar_terms():
    """Prueba la obtención de términos similares."""
    logger.info("=== Probando Términos Similares ===")
    
    try:
        from semantic_embeddings import get_similar_terms_for_word
        
        test_words = ["rpg", "acción", "nintendo", "minecraft"]
        
        for word in test_words:
            similar_terms = get_similar_terms_for_word(word, topn=3)
            if similar_terms:
                logger.info(f"✓ Términos similares a '{word}':")
                for term in similar_terms:
                    logger.info(f"  {term['rank']}. {term['word']} ({term['similarity_percentage']}%)")
            else:
                logger.warning(f"⚠ No se encontraron términos similares para '{word}'")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Error en términos similares: {e}")
        return False

def test_text_analysis():
    """Prueba el análisis de texto con embeddings."""
    logger.info("=== Probando Análisis de Texto ===")
    
    try:
        from semantic_embeddings import analyze_gaming_text_similarities
        
        test_texts = [
            "me gusta jugar rpg de acción",
            "nintendo switch es genial",
            "minecraft es un juego de construcción",
            "los shooters son emocionantes"
        ]
        
        for text in test_texts:
            analysis = analyze_gaming_text_similarities(text)
            logger.info(f"✓ Análisis de '{text}':")
            logger.info(f"  Palabras gaming: {analysis.get('gaming_words_found', [])}")
            logger.info(f"  Total similitudes: {analysis.get('total_similarities', 0)}")
            logger.info(f"  Similitud promedio: {analysis.get('average_similarity', 0):.3f}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Error en análisis de texto: {e}")
        return False

def test_gaming_analysis():
    """Prueba el análisis de contenido de videojuegos."""
    logger.info("=== Probando Análisis Gaming ===")
    
    try:
        from gaming_knowledge import analyze_gaming_content, get_gaming_response
        
        test_texts = [
            "me gusta jugar rpg de acción en nintendo switch",
            "minecraft es un juego de construcción muy divertido",
            "los shooters en primera persona son emocionantes",
            "hola, ¿cómo estás?"  # Texto no relacionado
        ]
        
        for text in test_texts:
            analysis = analyze_gaming_content(text)
            logger.info(f"✓ Análisis de '{text}':")
            logger.info(f"  Relacionado con gaming: {analysis['is_gaming_related']}")
            logger.info(f"  Palabras clave: {[kw['word'] for kw in analysis['keywords']]}")
            logger.info(f"  Juegos mencionados: {analysis['games_mentioned']}")
            
            # Probar respuesta del chatbot
            response = get_gaming_response(text)
            logger.info(f"  Respuesta: {response[:100]}...")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Error en análisis gaming: {e}")
        return False

def test_integration():
    """Prueba la integración completa."""
    logger.info("=== Probando Integración Completa ===")
    
    try:
        from gaming_knowledge import analyze_gaming_content
        
        # Texto de prueba completo
        text = "me gusta jugar rpg de acción como final fantasy en nintendo switch"
        
        # Análisis completo
        analysis = analyze_gaming_content(text)
        
        logger.info(f"✓ Análisis completo de '{text}':")
        logger.info(f"  Relacionado con gaming: {analysis['is_gaming_related']}")
        logger.info(f"  Palabras clave: {len(analysis['keywords'])}")
        logger.info(f"  Juegos mencionados: {analysis['games_mentioned']}")
        logger.info(f"  Categorías: {analysis['categories']}")
        
        # Verificar análisis semántico
        if analysis.get('semantic_analysis'):
            semantic = analysis['semantic_analysis']
            logger.info(f"  Análisis semántico disponible: {len(semantic.get('gaming_words_found', []))} palabras")
            logger.info(f"  Similitudes: {semantic.get('total_similarities', 0)}")
        
        # Verificar términos similares
        if analysis.get('similar_terms'):
            logger.info(f"  Términos similares: {len(analysis['similar_terms'])}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Error en integración: {e}")
        return False

def main():
    """Función principal del script de prueba."""
    logger.info("=== Iniciando Pruebas de Embeddings Semánticos ===")
    
    tests = [
        ("Importaciones", test_imports),
        ("Gaming Knowledge", test_gaming_knowledge),
        ("Funcionalidades Básicas", test_embeddings_basic),
        ("Cálculo de Similitudes", test_similarity_calculation),
        ("Términos Similares", test_similar_terms),
        ("Análisis de Texto", test_text_analysis),
        ("Análisis Gaming", test_gaming_analysis),
        ("Integración Completa", test_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n--- {test_name} ---")
        try:
            if test_func():
                logger.info(f"✓ {test_name}: PASÓ")
                passed += 1
            else:
                logger.error(f"✗ {test_name}: FALLÓ")
        except Exception as e:
            logger.error(f"✗ {test_name}: ERROR - {e}")
    
    logger.info(f"\n=== Resumen de Pruebas ===")
    logger.info(f"Pruebas pasadas: {passed}/{total}")
    logger.info(f"Porcentaje de éxito: {(passed/total)*100:.1f}%")
    
    if passed == total:
        logger.info("🎉 ¡Todas las pruebas pasaron! El módulo está funcionando correctamente.")
        return True
    else:
        logger.error(f"❌ {total-passed} pruebas fallaron. Revisa los errores anteriores.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
