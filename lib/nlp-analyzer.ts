import { spawn } from 'child_process';
import path from 'path';

export interface NLPAnalysis {
  tokens: string[];
  lemmas: Array<{ word: string; lemma: string }>;
  posTags: Array<{ word: string; pos: string; description: string }>;
}

export async function analyzePythonCode(text: string): Promise<NLPAnalysis> {
  return new Promise((resolve, reject) => {
    const process = spawn('python', [
      '-c',
      `
import stanza
import json

# Initialize stanza
try:
    nlp = stanza.Pipeline('es')
except:
    stanza.download('es')
    nlp = stanza.Pipeline('es')

# Process text
text = """${text}"""
doc = nlp(text)

# Get analysis
result = {
    "tokens": [],
    "lemmas": [],
    "posTags": []
}

for sent in doc.sentences:
    for word in sent.words:
        result["tokens"].append(word.text)
        result["lemmas"].append({"word": word.text, "lemma": word.lemma})
        result["posTags"].append({
            "word": word.text,
            "pos": word.upos,
            "description": {
                "ADJ": "Adjetivo",
                "ADP": "Preposición",
                "ADV": "Adverbio",
                "AUX": "Verbo auxiliar",
                "CCONJ": "Conjunción coordinada",
                "DET": "Determinante",
                "INTJ": "Interjección",
                "NOUN": "Sustantivo",
                "NUM": "Número",
                "PART": "Partícula",
                "PRON": "Pronombre",
                "PROPN": "Nombre propio",
                "PUNCT": "Puntuación",
                "SCONJ": "Conjunción subordinada",
                "SYM": "Símbolo",
                "VERB": "Verbo",
                "X": "Otro"
            }.get(word.upos, word.upos)
        })

print(json.dumps(result))
      `
    ]);

    let output = '';
    let errorOutput = '';

    process.stdout.on('data', (data) => {
      output += data.toString();
    });

    process.stderr.on('data', (data) => {
      errorOutput += data.toString();
    });

    process.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`Process exited with code ${code}\n${errorOutput}`));
        return;
      }

      try {
        const result = JSON.parse(output);
        resolve(result);
      } catch (error) {
        reject(error);
      }
    });
  });
}
