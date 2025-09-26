#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json

def main():
    # Escribir a stderr para que aparezca en los logs
    print("DEBUG: Script ejecutado", file=sys.stderr)
    print(f"DEBUG: Argumentos: {sys.argv}", file=sys.stderr)
    
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No text provided"}))
        return
    
    text = sys.argv[1]
    print(f"DEBUG: Procesando texto: {text}", file=sys.stderr)
    
    # Respuesta simple para probar
    result = {
        "text": text,
        "tokens": text.split(),
        "test": "API funcionando correctamente",
        "gaming_analysis": {
            "is_gaming_related": True,
            "keywords": [{"word": "test", "category": "test"}],
            "games_mentioned": [],
            "categories": {"test": 1},
            "semantic_analysis": {
                "gaming_words_found": ["test"],
                "similarities": [],
                "most_similar_pairs": [],
                "message": "Test de embeddings"
            },
            "similar_terms": []
        }
    }
    
    print("DEBUG: Enviando resultado", file=sys.stderr)
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
