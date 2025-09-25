"""
Módulo Mejorado de Procesamiento de Lenguaje Natural
Implementa tokenización, lematización y etiquetado POS robusto para el chatbot educativo

Requisitos:
- nltk
- spacy
- es_core_news_sm (modelo de spaCy para español)

Instalación:
pip install nltk spacy
python -m spacy download es_core_news_sm
"""

import re
import nltk
import spacy
from nltk.tokenize import word_tokenize, RegexpTokenizer, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import pos_tag
import json
from typing import Dict, List, Any

# Descargar recursos necesarios de NLTK
required_nltk_data = [
    ('tokenizers/punkt', 'punkt'),
    ('corpora/wordnet', 'wordnet'),
    ('averaged_perceptron_tagger', 'averaged_perceptron_tagger'),
    ('corpora/stopwords', 'stopwords'),
    ('taggers/averaged_perceptron_tagger', 'averaged_perceptron_tagger')
]

for path, name in required_nltk_data:
    try:
        nltk.data.find(path)
        print(f"✓ {name} ya está disponible")
    except LookupError:
        print(f"⬇ Descargando {name}...")
        nltk.download(name)

class EnhancedNLPProcessor:
    """
    Clase mejorada para el procesamiento de lenguaje natural
    Implementa tokenización, lematización y etiquetado POS con mayor precisión
    """
    
    def __init__(self):
        """Inicializa los componentes de PLN con manejo de errores robusto"""
        print("🚀 Inicializando procesador de PLN mejorado...")
        
        # Inicializar NLTK
        self.lemmatizer = WordNetLemmatizer()
        self.regexp_tokenizer = RegexpTokenizer(r'\w+')
        
        # Cargar stopwords en español
        try:
            self.spanish_stopwords = set(stopwords.words('spanish'))
            print("✓ Stopwords en español cargadas")
        except:
            self.spanish_stopwords = set()
            print("⚠ No se pudieron cargar stopwords")
        
        # Inicializar spaCy para español
        try:
            self.nlp = spacy.load("es_core_news_sm")
            self.spacy_available = True
            print("✓ spaCy con modelo español cargado correctamente")
        except OSError:
            print("⚠ spaCy no disponible. Instalando modelo...")
            try:
                import subprocess
                subprocess.run(["python", "-m", "spacy", "download", "es_core_news_sm"], check=True)
                self.nlp = spacy.load("es_core_news_sm")
                self.spacy_available = True
                print("✓ Modelo de spaCy instalado y cargado")
            except:
                print("❌ No se pudo instalar spaCy. Usando solo NLTK.")
                self.spacy_available = False
                self.nlp = None
        
        # Reglas morfológicas del español
        self.spanish_morphology = self._load_spanish_morphology()
        print("✓ Reglas morfológicas del español cargadas")
    
    def _load_spanish_morphology(self) -> Dict[str, Any]:
        """Carga reglas morfológicas específicas del español"""
        return {
            'verb_endings': {
                'ar': ['ando', 'ado', 'ada', 'ados', 'adas'],
                'er': ['iendo', 'ido', 'ida', 'idos', 'idas'],
                'ir': ['iendo', 'ido', 'ida', 'idos', 'idas']
            },
            'noun_plurals': ['s', 'es'],
            'adjective_endings': ['o', 'a', 'os', 'as', 'e', 'es'],
            'adverb_suffix': 'mente',
            'diminutives': ['ito', 'ita', 'itos', 'itas', 'illo', 'illa', 'illos', 'illas'],
            'augmentatives': ['ón', 'ona', 'ones', 'onas', 'ote', 'ota', 'otes', 'otas']
        }
    
    def tokenize_comprehensive(self, text: str) -> Dict[str, Any]:
        """
        Tokenización comprehensiva con múltiples métodos
        
        Args:
            text (str): Texto a tokenizar
            
        Returns:
            dict: Resultados completos de tokenización
        """
        results = {
            'original_text': text,
            'text_length': len(text),
            'methods': {}
        }
        
        # Método 1: División básica por espacios
        tokens_basic = text.split()
        results['methods']['basic_split'] = {
            'tokens': tokens_basic,
            'count': len(tokens_basic),
            'description': 'División simple por espacios en blanco'
        }
        
        # Método 2: Expresiones regulares
        tokens_regex = re.findall(r'\b\w+\b', text.lower())
        results['methods']['regex'] = {
            'tokens': tokens_regex,
            'count': len(tokens_regex),
            'description': 'Extracción de palabras usando expresiones regulares'
        }
        
        # Método 3: NLTK word_tokenize
        try:
            tokens_nltk = word_tokenize(text.lower(), language='spanish')
            results['methods']['nltk_word_tokenize'] = {
                'tokens': tokens_nltk,
                'count': len(tokens_nltk),
                'description': 'Tokenización avanzada de NLTK para español'
            }
        except:
            tokens_nltk = word_tokenize(text.lower())
            results['methods']['nltk_word_tokenize'] = {
                'tokens': tokens_nltk,
                'count': len(tokens_nltk),
                'description': 'Tokenización de NLTK (idioma por defecto)'
            }
        
        # Método 4: NLTK RegexpTokenizer
        tokens_regexp_nltk = self.regexp_tokenizer.tokenize(text.lower())
        results['methods']['nltk_regexp'] = {
            'tokens': tokens_regexp_nltk,
            'count': len(tokens_regexp_nltk),
            'description': 'Tokenización con RegexpTokenizer de NLTK'
        }
        
        # Método 5: spaCy (si está disponible)
        if self.spacy_available:
            doc = self.nlp(text)
            tokens_spacy = [token.text.lower() for token in doc if not token.is_punct and not token.is_space]
            results['methods']['spacy'] = {
                'tokens': tokens_spacy,
                'count': len(tokens_spacy),
                'description': 'Tokenización inteligente de spaCy para español'
            }
        
        # Tokenización de oraciones
        try:
            sentences = sent_tokenize(text, language='spanish')
            results['sentence_tokenization'] = {
                'sentences': sentences,
                'count': len(sentences),
                'description': 'División en oraciones usando NLTK'
            }
        except:
            sentences = sent_tokenize(text)
            results['sentence_tokenization'] = {
                'sentences': sentences,
                'count': len(sentences),
                'description': 'División en oraciones (idioma por defecto)'
            }
        
        # Seleccionar el mejor método (spaCy si está disponible, sino NLTK)
        if self.spacy_available:
            results['recommended_tokens'] = results['methods']['spacy']['tokens']
        else:
            results['recommended_tokens'] = results['methods']['nltk_word_tokenize']['tokens']
        
        return results
    
    def lemmatize_comprehensive(self, text: str, tokens: List[str] = None) -> Dict[str, Any]:
        """
        Lematización comprehensiva con múltiples enfoques
        
        Args:
            text (str): Texto original
            tokens (List[str]): Tokens pre-procesados (opcional)
            
        Returns:
            dict: Resultados completos de lematización
        """
        if tokens is None:
            tokens = re.findall(r'\b\w+\b', text.lower())
        
        results = {
            'original_text': text,
            'token_count': len(tokens),
            'methods': {}
        }
        
        # Método 1: NLTK WordNetLemmatizer
        lemmas_nltk = []
        for token in tokens:
            lemma_noun = self.lemmatizer.lemmatize(token, pos='n')
            lemma_verb = self.lemmatizer.lemmatize(token, pos='v')
            lemma_adj = self.lemmatizer.lemmatize(token, pos='a')
            lemma_adv = self.lemmatizer.lemmatize(token, pos='r')
            
            # Elegir la mejor lematización
            candidates = [lemma_noun, lemma_verb, lemma_adj, lemma_adv]
            best_lemma = min(candidates, key=len) if any(c != token for c in candidates) else token
            
            lemmas_nltk.append({
                'word': token,
                'lemma': best_lemma,
                'candidates': {
                    'noun': lemma_noun,
                    'verb': lemma_verb,
                    'adjective': lemma_adj,
                    'adverb': lemma_adv
                }
            })
        
        results['methods']['nltk_wordnet'] = {
            'lemmas': lemmas_nltk,
            'description': 'Lematización con WordNetLemmatizer de NLTK',
            'limitations': 'Optimizado para inglés, limitaciones en español'
        }
        
        # Método 2: Reglas morfológicas del español
        lemmas_rules = []
        for token in tokens:
            lemma = self._apply_spanish_morphology_rules(token)
            lemmas_rules.append({
                'word': token,
                'lemma': lemma,
                'rule_applied': self._get_applied_rule(token, lemma)
            })
        
        results['methods']['spanish_rules'] = {
            'lemmas': lemmas_rules,
            'description': 'Lematización usando reglas morfológicas del español',
            'advantages': 'Específico para español, maneja conjugaciones verbales'
        }
        
        # Método 3: spaCy (si está disponible)
        if self.spacy_available:
            doc = self.nlp(text)
            lemmas_spacy = []
            
            for token in doc:
                if not token.is_punct and not token.is_space and token.text.lower() in tokens:
                    lemmas_spacy.append({
                        'word': token.text.lower(),
                        'lemma': token.lemma_,
                        'pos': token.pos_,
                        'tag': token.tag_,
                        'morphology': str(token.morph)
                    })
            
            results['methods']['spacy_es'] = {
                'lemmas': lemmas_spacy,
                'description': 'Lematización con modelo español de spaCy',
                'advantages': 'Modelo entrenado específicamente para español'
            }
        
        # Seleccionar el mejor método
        if self.spacy_available:
            results['recommended_lemmas'] = results['methods']['spacy_es']['lemmas']
        else:
            results['recommended_lemmas'] = results['methods']['spanish_rules']['lemmas']
        
        return results
    
    def _apply_spanish_morphology_rules(self, word: str) -> str:
        """Aplica reglas morfológicas específicas del español"""
        original_word = word
        
        # Regla 1: Adverbios terminados en -mente
        if word.endswith('mente'):
            base = word[:-5]  # Quitar 'mente'
            if base.endswith('a'):
                return base[:-1] + 'o'  # rápidamente -> rápido
            return base
        
        # Regla 2: Gerundios
        if word.endswith('ando'):
            return word[:-4] + 'ar'  # hablando -> hablar
        if word.endswith('iendo'):
            return word[:-5] + 'er'  # comiendo -> comer
        
        # Regla 3: Participios
        if word.endswith('ado'):
            return word[:-3] + 'ar'  # hablado -> hablar
        if word.endswith('ido'):
            return word[:-3] + 'er'  # comido -> comer
        
        # Regla 4: Plurales
        if word.endswith('es') and len(word) > 3:
            return word[:-2]  # casas -> casa
        if word.endswith('s') and len(word) > 2 and not word.endswith('ss'):
            return word[:-1]  # libros -> libro
        
        # Regla 5: Femeninos
        if word.endswith('a') and len(word) > 2:
            # Verificar si es un adjetivo femenino
            masculine = word[:-1] + 'o'
            if masculine != word:  # pequeña -> pequeño
                return masculine
        
        # Regla 6: Diminutivos
        for dim in self.spanish_morphology['diminutives']:
            if word.endswith(dim):
                return word[:-len(dim)]
        
        return word
    
    def _get_applied_rule(self, original: str, lemma: str) -> str:
        """Identifica qué regla morfológica se aplicó"""
        if original == lemma:
            return "sin_cambio"
        if original.endswith('mente'):
            return "adverbio_mente"
        if original.endswith('ando') or original.endswith('iendo'):
            return "gerundio"
        if original.endswith('ado') or original.endswith('ido'):
            return "participio"
        if original.endswith('s') or original.endswith('es'):
            return "plural"
        if original.endswith('a') and lemma.endswith('o'):
            return "femenino_masculino"
        return "regla_personalizada"
    
    def pos_tag_comprehensive(self, text: str, tokens: List[str] = None) -> Dict[str, Any]:
        """
        Etiquetado POS comprehensivo con múltiples enfoques
        
        Args:
            text (str): Texto original
            tokens (List[str]): Tokens pre-procesados (opcional)
            
        Returns:
            dict: Resultados completos de etiquetado POS
        """
        if tokens is None:
            tokens = re.findall(r'\b\w+\b', text.lower())
        
        results = {
            'original_text': text,
            'token_count': len(tokens),
            'methods': {}
        }
        
        # Método 1: NLTK POS Tagger
        pos_nltk = pos_tag(tokens)
        tagged_nltk = []
        
        for word, tag in pos_nltk:
            tagged_nltk.append({
                'word': word,
                'pos': tag,
                'description': self._get_nltk_pos_description(tag),
                'category': self._nltk_to_universal_pos(tag)
            })
        
        results['methods']['nltk_pos_tag'] = {
            'tagged_words': tagged_nltk,
            'description': 'Etiquetado POS con NLTK',
            'tagset': 'Penn Treebank',
            'limitations': 'Entrenado principalmente para inglés'
        }
        
        # Método 2: Reglas heurísticas para español
        tagged_rules = []
        for token in tokens:
            pos_tag = self._spanish_pos_rules(token)
            tagged_rules.append({
                'word': token,
                'pos': pos_tag,
                'description': self._get_spanish_pos_description(pos_tag),
                'confidence': self._get_pos_confidence(token, pos_tag)
            })
        
        results['methods']['spanish_heuristics'] = {
            'tagged_words': tagged_rules,
            'description': 'Etiquetado usando reglas heurísticas para español',
            'advantages': 'Adaptado específicamente para morfología española'
        }
        
        # Método 3: spaCy (si está disponible)
        if self.spacy_available:
            doc = self.nlp(text)
            tagged_spacy = []
            
            for token in doc:
                if not token.is_punct and not token.is_space:
                    tagged_spacy.append({
                        'word': token.text.lower(),
                        'pos': token.pos_,
                        'tag': token.tag_,
                        'description': self._get_spanish_pos_description(token.pos_),
                        'lemma': token.lemma_,
                        'dependency': token.dep_,
                        'is_stop': token.is_stop,
                        'morphology': str(token.morph)
                    })
            
            results['methods']['spacy_es'] = {
                'tagged_words': tagged_spacy,
                'description': 'Etiquetado POS con modelo español de spaCy',
                'tagset': 'Universal Dependencies',
                'advantages': 'Modelo entrenado específicamente para español'
            }
        
        # Seleccionar el mejor método
        if self.spacy_available:
            results['recommended_tags'] = results['methods']['spacy_es']['tagged_words']
        else:
            results['recommended_tags'] = results['methods']['spanish_heuristics']['tagged_words']
        
        return results
    
    def _spanish_pos_rules(self, word: str) -> str:
        """Aplica reglas heurísticas para determinar POS en español"""
        # Diccionario de palabras comunes
        common_words = {
            # Determinantes
            'el': 'DET', 'la': 'DET', 'los': 'DET', 'las': 'DET',
            'un': 'DET', 'una': 'DET', 'unos': 'DET', 'unas': 'DET',
            'este': 'DET', 'esta': 'DET', 'estos': 'DET', 'estas': 'DET',
            'mi': 'DET', 'tu': 'DET', 'su': 'DET', 'nuestro': 'DET',
            
            # Pronombres
            'yo': 'PRON', 'tú': 'PRON', 'él': 'PRON', 'ella': 'PRON',
            'nosotros': 'PRON', 'vosotros': 'PRON', 'ellos': 'PRON', 'ellas': 'PRON',
            'me': 'PRON', 'te': 'PRON', 'se': 'PRON', 'nos': 'PRON', 'les': 'PRON',
            
            # Preposiciones
            'de': 'ADP', 'en': 'ADP', 'con': 'ADP', 'por': 'ADP', 'para': 'ADP',
            'sin': 'ADP', 'sobre': 'ADP', 'bajo': 'ADP', 'desde': 'ADP', 'hasta': 'ADP',
            
            # Conjunciones
            'y': 'CCONJ', 'o': 'CCONJ', 'pero': 'CCONJ', 'aunque': 'SCONJ',
            'porque': 'SCONJ', 'si': 'SCONJ', 'cuando': 'SCONJ', 'donde': 'SCONJ',
            
            # Adverbios comunes
            'muy': 'ADV', 'más': 'ADV', 'menos': 'ADV', 'bien': 'ADV', 'mal': 'ADV',
            'aquí': 'ADV', 'allí': 'ADV', 'ahora': 'ADV', 'después': 'ADV', 'antes': 'ADV',
            
            # Verbos auxiliares y copulativos
            'ser': 'AUX', 'estar': 'AUX', 'haber': 'AUX', 'tener': 'VERB',
            'es': 'AUX', 'está': 'AUX', 'son': 'AUX', 'están': 'AUX'
        }
        
        if word in common_words:
            return common_words[word]
        
        # Reglas morfológicas
        if word.endswith('mente'):
            return 'ADV'  # Adverbios terminados en -mente
        
        if word.endswith(('ando', 'iendo')):
            return 'VERB'  # Gerundios
        
        if word.endswith(('ado', 'ido', 'to', 'so', 'cho')):
            return 'VERB'  # Participios
        
        if word.endswith(('ción', 'sión', 'dad', 'tad', 'eza', 'ura', 'ismo', 'ista')):
            return 'NOUN'  # Sustantivos con sufijos típicos
        
        if word.endswith(('ar', 'er', 'ir')):
            return 'VERB'  # Infinitivos
        
        if word.endswith(('oso', 'osa', 'ivo', 'iva', 'able', 'ible')):
            return 'ADJ'  # Adjetivos con sufijos típicos
        
        # Por defecto, asumir sustantivo
        return 'NOUN'
    
    def _get_pos_confidence(self, word: str, pos: str) -> float:
        """Calcula la confianza en la etiqueta POS asignada"""
        # Palabras muy comunes tienen alta confianza
        high_confidence_words = {
            'el', 'la', 'de', 'en', 'y', 'es', 'que', 'se', 'no', 'un', 'por', 'con'
        }
        
        if word in high_confidence_words:
            return 0.95
        
        # Palabras con terminaciones claras tienen confianza media-alta
        clear_endings = {
            'mente': 0.9,  # Adverbios
            'ción': 0.85,  # Sustantivos
            'ando': 0.9,   # Gerundios
            'iendo': 0.9   # Gerundios
        }
        
        for ending, confidence in clear_endings.items():
            if word.endswith(ending):
                return confidence
        
        # Confianza por defecto
        return 0.6
    
    def _get_spanish_pos_description(self, pos: str) -> str:
        """Obtiene descripción en español para etiquetas POS"""
        descriptions = {
            'NOUN': 'Sustantivo',
            'VERB': 'Verbo',
            'ADJ': 'Adjetivo',
            'ADV': 'Adverbio',
            'PRON': 'Pronombre',
            'DET': 'Determinante',
            'ADP': 'Preposición',
            'CCONJ': 'Conjunción coordinante',
            'SCONJ': 'Conjunción subordinante',
            'NUM': 'Número',
            'PUNCT': 'Puntuación',
            'AUX': 'Verbo auxiliar',
            'INTJ': 'Interjección',
            'PART': 'Partícula',
            'X': 'Otro'
        }
        return descriptions.get(pos, pos)
    
    def _get_nltk_pos_description(self, tag: str) -> str:
        """Obtiene descripción para etiquetas NLTK POS"""
        descriptions = {
            'NN': 'Sustantivo singular',
            'NNS': 'Sustantivo plural',
            'NNP': 'Nombre propio singular',
            'NNPS': 'Nombre propio plural',
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
            'PRP$': 'Pronombre posesivo',
            'DT': 'Determinante',
            'IN': 'Preposición',
            'CC': 'Conjunción coordinante',
            'CD': 'Número cardinal',
            'WP': 'Pronombre interrogativo'
        }
        return descriptions.get(tag, f'Etiqueta {tag}')
    
    def _nltk_to_universal_pos(self, nltk_tag: str) -> str:
        """Convierte etiquetas NLTK a etiquetas universales"""
        mapping = {
            'NN': 'NOUN', 'NNS': 'NOUN', 'NNP': 'PROPN', 'NNPS': 'PROPN',
            'VB': 'VERB', 'VBD': 'VERB', 'VBG': 'VERB', 'VBN': 'VERB', 'VBP': 'VERB', 'VBZ': 'VERB',
            'JJ': 'ADJ', 'JJR': 'ADJ', 'JJS': 'ADJ',
            'RB': 'ADV', 'RBR': 'ADV', 'RBS': 'ADV',
            'PRP': 'PRON', 'PRP$': 'PRON',
            'DT': 'DET',
            'IN': 'ADP',
            'CC': 'CCONJ',
            'CD': 'NUM'
        }
        return mapping.get(nltk_tag, 'X')
    
    def process_complete_enhanced(self, text: str) -> Dict[str, Any]:
        """
        Procesamiento completo y mejorado de PLN
        
        Args:
            text (str): Texto a procesar
            
        Returns:
            dict: Análisis completo con múltiples métodos y métricas
        """
        print(f"\n🔍 Procesando texto: '{text}'")
        
        results = {
            'input': {
                'original_text': text,
                'text_length': len(text),
                'word_count': len(text.split()),
                'character_count': len(text.replace(' ', '')),
                'sentence_count': len(re.split(r'[.!?]+', text)) - 1
            },
            'timestamp': str(nltk.corpus.util.LazyCorpusLoader.__class__),
            'processor_info': {
                'nltk_available': True,
                'spacy_available': self.spacy_available,
                'spanish_model': 'es_core_news_sm' if self.spacy_available else None
            }
        }
        
        # 1. Tokenización comprehensiva
        print("📝 Ejecutando tokenización...")
        tokenization_results = self.tokenize_comprehensive(text)
        results['tokenization'] = tokenization_results
        
        # Usar tokens recomendados para análisis posterior
        recommended_tokens = tokenization_results['recommended_tokens']
        
        # 2. Lematización comprehensiva
        print("🔤 Ejecutando lematización...")
        lemmatization_results = self.lemmatize_comprehensive(text, recommended_tokens)
        results['lemmatization'] = lemmatization_results
        
        # 3. Etiquetado POS comprehensivo
        print("🏷️ Ejecutando etiquetado POS...")
        pos_results = self.pos_tag_comprehensive(text, recommended_tokens)
        results['pos_tagging'] = pos_results
        
        # 4. Análisis adicional
        print("📊 Generando análisis adicional...")
        results['analysis'] = self._generate_additional_analysis(text, recommended_tokens, results)
        
        # 5. Resumen ejecutivo
        results['summary'] = self._generate_summary(results)
        
        print("✅ Procesamiento completado")
        return results
    
    def _generate_additional_analysis(self, text: str, tokens: List[str], results: Dict) -> Dict[str, Any]:
        """Genera análisis adicional del texto"""
        analysis = {}
        
        # Análisis de frecuencia
        from collections import Counter
        token_freq = Counter(tokens)
        analysis['frequency'] = {
            'most_common': token_freq.most_common(5),
            'unique_tokens': len(set(tokens)),
            'total_tokens': len(tokens),
            'lexical_diversity': len(set(tokens)) / len(tokens) if tokens else 0
        }
        
        # Análisis de stopwords
        if self.spanish_stopwords:
            stopwords_found = [token for token in tokens if token in self.spanish_stopwords]
            analysis['stopwords'] = {
                'found': stopwords_found,
                'count': len(stopwords_found),
                'percentage': len(stopwords_found) / len(tokens) * 100 if tokens else 0
            }
        
        # Análisis de longitud de palabras
        word_lengths = [len(token) for token in tokens]
        if word_lengths:
            analysis['word_length'] = {
                'average': sum(word_lengths) / len(word_lengths),
                'min': min(word_lengths),
                'max': max(word_lengths),
                'distribution': Counter(word_lengths)
            }
        
        return analysis
    
    def _generate_summary(self, results: Dict) -> Dict[str, Any]:
        """Genera un resumen ejecutivo del análisis"""
        summary = {
            'text_stats': results['input'],
            'processing_methods': {
                'tokenization': len(results['tokenization']['methods']),
                'lemmatization': len(results['lemmatization']['methods']),
                'pos_tagging': len(results['pos_tagging']['methods'])
            }
        }
        
        # Recomendaciones
        recommendations = []
        if not results['processor_info']['spacy_available']:
            recommendations.append("Instalar spaCy para mejor precisión en español")
        
        if results['input']['word_count'] > 50:
            recommendations.append("Texto largo: considerar análisis por párrafos")
        
        summary['recommendations'] = recommendations
        
        return summary

def demonstrate_enhanced_nlp():
    """Función de demostración del procesador mejorado"""
    processor = EnhancedNLPProcessor()
    
    # Textos de ejemplo más complejos
    ejemplos = [
        "El procesamiento de lenguaje natural es una disciplina fascinante que combina lingüística y computación.",
        "Los estudiantes están aprendiendo rápidamente las técnicas avanzadas de tokenización y lematización.",
        "María y José trabajan colaborativamente en el desarrollo de algoritmos inteligentes para análisis textual.",
        "¿Cómo podemos mejorar significativamente la precisión de nuestros modelos de PLN en español?"
    ]
    
    print("=" * 80)
    print("🚀 DEMOSTRACIÓN DEL PROCESADOR DE PLN MEJORADO")
    print("=" * 80)
    
    for i, texto in enumerate(ejemplos, 1):
        print(f"\n📄 EJEMPLO {i}")
        print("-" * 60)
        print(f"Texto: {texto}")
        
        # Procesamiento completo
        resultado = processor.process_complete_enhanced(texto)
        
        # Mostrar resumen
        print(f"\n📊 RESUMEN:")
        print(f"  • Longitud: {resultado['input']['text_length']} caracteres")
        print(f"  • Palabras: {resultado['input']['word_count']}")
        print(f"  • Tokens únicos: {resultado['analysis']['frequency']['unique_tokens']}")
        print(f"  • Diversidad léxica: {resultado['analysis']['frequency']['lexical_diversity']:.2f}")
        
        # Mostrar tokens recomendados
        tokens = resultado['tokenization']['recommended_tokens']
        print(f"\n🔤 TOKENS ({len(tokens)}): {tokens}")
        
        # Mostrar lemas recomendados
        lemmas = resultado['lemmatization']['recommended_lemmas'][:5]
        print(f"\n🧠 LEMATIZACIÓN (primeros 5):")
        for lemma in lemmas:
            print(f"  • {lemma['word']} → {lemma['lemma']}")
        
        # Mostrar etiquetas POS recomendadas
        pos_tags = resultado['pos_tagging']['recommended_tags'][:5]
        print(f"\n🏷️ ETIQUETADO POS (primeros 5):")
        for tag in pos_tags:
            print(f"  • {tag['word']}: {tag['pos']} ({tag['description']})")
        
        print("\n" + "=" * 80)

if __name__ == "__main__":
    demonstrate_enhanced_nlp()
