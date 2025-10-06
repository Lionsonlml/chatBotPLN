#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analizador de sentimientos usando pysentimiento
"""

import sys
import json

def load_sentiment_analyzer():
    """Carga el analizador de sentimientos"""
    try:
        from pysentimiento import create_analyzer
        analyzer = create_analyzer(task="sentiment", lang="es")
        return analyzer
    except Exception as e:
        print(f"Error cargando el analizador de sentimientos: {e}", file=sys.stderr)
        return None

def analyze_sentiment(analyzer, text):
    """Analiza el sentimiento del texto"""
    try:
        # Analizar el sentimiento
        result = analyzer.predict(text)
        
        # Obtener las probabilidades
        probabilities = result.probas
        
        return {
            "text": text,
            "sentiment": result.output,
            "confidence": max(probabilities.values()),
            "probabilities": probabilities,
            "model": "pysentimiento",
            "timestamp": "2024-01-01T00:00:00"  # Se puede mejorar con datetime real
        }
    except Exception as e:
        print(f"Error analizando sentimiento: {e}", file=sys.stderr)
        return None

def main():
    """Función principal"""
    if len(sys.argv) < 2:
        result = {
            "error": "Texto requerido como parámetro"
        }
        print(json.dumps(result, ensure_ascii=False))
        return
    
    text = sys.argv[1]
    
    # Cargar analizador
    analyzer = load_sentiment_analyzer()
    
    if analyzer is None:
        result = {
            "error": "No se pudo cargar el analizador de sentimientos",
            "fallback_analysis": {
                "text": text,
                "sentiment": "NEU",
                "confidence": 0.5,
                "probabilities": {"POS": 0.33, "NEG": 0.33, "NEU": 0.34},
                "model": "fallback"
            }
        }
        print(json.dumps(result, ensure_ascii=False))
        return
    
    # Analizar sentimiento
    result = analyze_sentiment(analyzer, text)
    
    if result is None:
        result = {
            "error": "Error en el análisis de sentimientos",
            "fallback_analysis": {
                "text": text,
                "sentiment": "NEU",
                "confidence": 0.5,
                "probabilities": {"POS": 0.33, "NEG": 0.33, "NEU": 0.34},
                "model": "fallback"
            }
        }
    
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()

