"""
Módulo de Procesamiento de Lenguaje Natural
Implementa tokenización, lematización y etiquetado POS para el chatbot educativo

Requisitos:
- stanza (para procesamiento avanzado de español)

Instalación:
pip install stanza
"""

import stanza
import sys
import json
from typing import Dict, List, Tuple

# Inicializar Stanza con el modelo español
try:
    nlp = stanza.Pipeline('es')
except:
    stanza.download('es')
    nlp = stanza.Pipeline('es')
from nltk import pos_tag
import json

# Descargar recursos necesarios de NLTK
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

try:
    nltk.data.find('averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class NLPProcessor:
    """
    Clase principal para el procesamiento de lenguaje natural
    Implementa tokenización, lematización y etiquetado POS
    """
    
    def __init__(self):
        """Inicializa los componentes de PLN"""
        # Inicializar NLTK
        self.lemmatizer = WordNetLemmatizer()
        self.regexp_tokenizer = RegexpTokenizer(r'\w+')
        
        # Inicializar spaCy para español
        try:
            self.nlp = spacy.load("es_core_news_sm")
            self.spacy_available = True
            print("✓ spaCy cargado correctamente")
        except OSError:
            print("⚠ spaCy no disponible. Usando solo NLTK.")
            self.spacy_available = False
            self.nlp = None
    
    def tokenize_basic(self, text):
        """
        Tokenización básica usando expresiones regulares y espacios
        
        Args:
            text (str): Texto a tokenizar
            
        Returns:
            list: Lista de tokens
        """
        # Método 1: División por espacios (muy básico)
        tokens_spaces = text.split()
        
        # Método 2: Expresiones regulares para palabras
        tokens_regex = re.findall(r'\b\w+\b', text.lower())
        
        return {
            'method': 'basic',
            'tokens_spaces': tokens_spaces,
            'tokens_regex': tokens_regex,
            'count': len(tokens_regex)
        }
    
    def tokenize_nltk(self, text):
        """
        Tokenización usando NLTK
        
        Args:
            text (str): Texto a tokenizar
            
        Returns:
            dict: Resultados de tokenización con NLTK
        """
        # Tokenización con NLTK
        tokens_nltk = word_tokenize(text.lower())
        
        # Tokenización con RegexpTokenizer (solo palabras)
        tokens_regexp = self.regexp_tokenizer.tokenize(text.lower())
        
        return {
            'method': 'nltk',
            'tokens_word_tokenize': tokens_nltk,
            'tokens_regexp': tokens_regexp,
            'count': len(tokens_regexp)
        }
    
    def tokenize_spacy(self, text):
        """
        Tokenización usando spaCy
        
        Args:
            text (str): Texto a tokenizar
            
        Returns:
            dict: Resultados de tokenización con spaCy
        """
        if not self.spacy_available:
            return {'method': 'spacy', 'error': 'spaCy no disponible'}
        
        doc = self.nlp(text)
        tokens = [token.text.lower() for token in doc if not token.is_punct and not token.is_space]
        
        return {
            'method': 'spacy',
            'tokens': tokens,
            'count': len(tokens)
        }
    
    def lemmatize_nltk(self, tokens):
        """
        Lematización usando NLTK WordNetLemmatizer
        
        Args:
            tokens (list): Lista de tokens
            
        Returns:
            dict: Resultados de lematización
        """
        lemmas = []
        for token in tokens:
            # Lematización como sustantivo por defecto
            lemma_noun = self.lemmatizer.lemmatize(token, pos='n')
            # Lematización como verbo
            lemma_verb = self.lemmatizer.lemmatize(token, pos='v')
            
            # Elegir la mejor lematización
            if lemma_verb != token:
                lemma = lemma_verb
            else:
                lemma = lemma_noun
            
            lemmas.append({
                'word': token,
                'lemma': lemma,
                'lemma_noun': lemma_noun,
                'lemma_verb': lemma_verb
            })
        
        return {
            'method': 'nltk_wordnet',
            'lemmas': lemmas,
            'limitations': 'WordNetLemmatizer está optimizado para inglés. Para español tiene limitaciones.'
        }
    
    def lemmatize_spacy(self, text):
        """
        Lematización usando spaCy
        
        Args:
            text (str): Texto a lematizar
            
        Returns:
            dict: Resultados de lematización con spaCy
        """
        if not self.spacy_available:
            return {'method': 'spacy', 'error': 'spaCy no disponible'}
        
        doc = self.nlp(text)
        lemmas = []
        
        for token in doc:
            if not token.is_punct and not token.is_space:
                lemmas.append({
                    'word': token.text,
                    'lemma': token.lemma_,
                    'pos': token.pos_
                })
        
        return {
            'method': 'spacy_es',
            'lemmas': lemmas,
            'advantages': 'spaCy con modelo en español ofrece mejor lematización para este idioma'
        }
    
    def pos_tag_nltk(self, tokens):
        """
        Etiquetado POS usando NLTK
        
        Args:
            tokens (list): Lista de tokens
            
        Returns:
            dict: Resultados de etiquetado POS
        """
        pos_tags = pos_tag(tokens)
        
        # Mapeo de etiquetas POS de NLTK a descripciones
        pos_descriptions = {
            'NN': 'Sustantivo singular',
            'NNS': 'Sustantivo plural',
            'VB': 'Verbo base',
            'VBD': 'Verbo pasado',
            'VBG': 'Verbo gerundio',
            'VBN': 'Verbo participio',
            'VBP': 'Verbo presente',
            'VBZ': 'Verbo 3ra persona singular',
            'JJ': 'Adjetivo',
            'JJR': 'Adjetivo comparativo',
            'JJS': 'Adjetivo superlativo',
            'RB': 'Adverbio',
            'RBR': 'Adverbio comparativo',
            'RBS': 'Adverbio superlativo',
            'PRP': 'Pronombre personal',
            'DT': 'Determinante',
            'IN': 'Preposición',
            'CC': 'Conjunción coordinante'
        }
        
        tagged_words = []
        for word, tag in pos_tags:
            tagged_words.append({
                'word': word,
                'pos': tag,
                'description': pos_descriptions.get(tag, 'Etiqueta desconocida')
            })
        
        return {
            'method': 'nltk_pos_tag',
            'tagged_words': tagged_words,
            'limitations': 'NLTK POS tagger está entrenado principalmente para inglés'
        }
    
    def pos_tag_spacy(self, text):
        """
        Etiquetado POS usando spaCy
        
        Args:
            text (str): Texto a etiquetar
            
        Returns:
            dict: Resultados de etiquetado POS con spaCy
        """
        if not self.spacy_available:
            return {'method': 'spacy', 'error': 'spaCy no disponible'}
        
        doc = self.nlp(text)
        tagged_words = []
        
        # Mapeo de etiquetas POS de spaCy a español
        pos_spanish = {
            'NOUN': 'Sustantivo',
            'VERB': 'Verbo',
            'ADJ': 'Adjetivo',
            'ADV': 'Adverbio',
            'PRON': 'Pronombre',
            'DET': 'Determinante',
            'ADP': 'Preposición',
            'CONJ': 'Conjunción',
            'NUM': 'Número',
            'PUNCT': 'Puntuación',
            'X': 'Otro',
            'SPACE': 'Espacio'
        }
        
        for token in doc:
            if not token.is_space:
                tagged_words.append({
                    'word': token.text,
                    'pos': token.pos_,
                    'tag': token.tag_,
                    'description': pos_spanish.get(token.pos_, token.pos_),
                    'dependency': token.dep_,
                    'is_alpha': token.is_alpha,
                    'is_stop': token.is_stop
                })
        
        return {
            'method': 'spacy_es',
            'tagged_words': tagged_words,
            'advantages': 'spaCy con modelo español ofrece mejor precisión para POS tagging'
        }
    
    def process_complete(self, text):
        """
        Procesamiento completo de PLN: tokenización, lematización y POS tagging
        
        Args:
            text (str): Texto a procesar
            
        Returns:
            dict: Resultados completos del análisis
        """
        results = {
            'original_text': text,
            'text_length': len(text),
            'word_count': len(text.split())
        }
        
        # Tokenización
        results['tokenization'] = {
            'basic': self.tokenize_basic(text),
            'nltk': self.tokenize_nltk(text)
        }
        
        if self.spacy_available:
            results['tokenization']['spacy'] = self.tokenize_spacy(text)
        
        # Usar tokens de NLTK para procesamiento posterior
        tokens = results['tokenization']['nltk']['tokens_regexp']
        
        # Lematización
        results['lemmatization'] = {
            'nltk': self.lemmatize_nltk(tokens)
        }
        
        if self.spacy_available:
            results['lemmatization']['spacy'] = self.lemmatize_spacy(text)
        
        # POS Tagging
        results['pos_tagging'] = {
            'nltk': self.pos_tag_nltk(tokens)
        }
        
        if self.spacy_available:
            results['pos_tagging']['spacy'] = self.pos_tag_spacy(text)
        
        return results

def main():
    """
    Función principal para demostrar el uso del procesador de PLN
    """
    processor = NLPProcessor()
    
    # Textos de ejemplo
    ejemplos = [
        "El gato come pescado en la cocina.",
        "Los niños están jugando en el parque.",
        "María estudia programación en la universidad.",
        "El procesamiento de lenguaje natural es fascinante."
    ]
    
    print("=== DEMOSTRACIÓN DEL PROCESADOR DE PLN ===\n")
    
    for i, texto in enumerate(ejemplos, 1):
        print(f"EJEMPLO {i}: {texto}")
        print("-" * 50)
        
        # Procesamiento completo
        resultado = processor.process_complete(texto)
        
        # Mostrar tokenización
        print("TOKENIZACIÓN:")
        tokens_basic = resultado['tokenization']['basic']['tokens_regex']
        tokens_nltk = resultado['tokenization']['nltk']['tokens_regexp']
        print(f"  Básica: {tokens_basic}")
        print(f"  NLTK: {tokens_nltk}")
        
        if 'spacy' in resultado['tokenization']:
            tokens_spacy = resultado['tokenization']['spacy']['tokens']
            print(f"  spaCy: {tokens_spacy}")
        
        # Mostrar lematización
        print("\nLEMATIZACIÓN:")
        lemmas_nltk = resultado['lemmatization']['nltk']['lemmas']
        for lemma in lemmas_nltk[:5]:  # Mostrar solo los primeros 5
            print(f"  {lemma['word']} → {lemma['lemma']}")
        
        if 'spacy' in resultado['lemmatization']:
            lemmas_spacy = resultado['lemmatization']['spacy']['lemmas']
            print("  spaCy:")
            for lemma in lemmas_spacy[:5]:
                print(f"    {lemma['word']} → {lemma['lemma']}")
        
        # Mostrar POS tagging
        print("\nETIQUETADO POS:")
        pos_nltk = resultado['pos_tagging']['nltk']['tagged_words']
        for pos in pos_nltk[:5]:
            print(f"  {pos['word']}: {pos['pos']} ({pos['description']})")
        
        if 'spacy' in resultado['pos_tagging']:
            pos_spacy = resultado['pos_tagging']['spacy']['tagged_words']
            print("  spaCy:")
            for pos in pos_spacy[:5]:
                print(f"    {pos['word']}: {pos['pos']} ({pos['description']})")
        
        print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
