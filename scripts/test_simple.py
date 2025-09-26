#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json

def main():
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
    
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
