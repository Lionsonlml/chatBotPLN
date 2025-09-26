#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import os

def main():
    # Escribir a un archivo de debug
    with open('api_debug_final3.txt', 'w', encoding='utf-8') as f:
        f.write(f"Script ejecutado con argumentos: {sys.argv}\n")
        f.write(f"Directorio actual: {os.getcwd()}\n")
        f.write(f"Archivo ejecutado: {__file__}\n")
    
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No text provided"}))
        return
    
    text = sys.argv[1]
    
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
    
    # Escribir el resultado a un archivo también
    with open('api_debug_final3.txt', 'a', encoding='utf-8') as f:
        f.write(f"Resultado: {json.dumps(result, ensure_ascii=False)}\n")
    
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
