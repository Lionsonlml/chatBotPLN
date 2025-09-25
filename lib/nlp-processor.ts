import { spawn } from 'child_process';
import path from 'path';

interface NLPResult {
  tokens: string[];
  lemmas: Array<{ word: string; lemma: string }>;
  posTags: Array<{ word: string; pos: string; description: string }>;
}

export async function processText(text: string): Promise<NLPResult> {
  // Ejecutamos el script de Python que usa spaCy
  const pythonProcess = spawn('python', [
    path.join(process.cwd(), 'scripts', 'nlp_processor.py'),
    text
  ]);

  return new Promise((resolve, reject) => {
    let outputData = '';

    pythonProcess.stdout.on('data', (data) => {
      outputData += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error(`Error: ${data}`);
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`Process exited with code ${code}`));
        return;
      }

      try {
        const result = JSON.parse(outputData);
        resolve(result);
      } catch (error) {
        reject(error);
      }
    });
  });
}
