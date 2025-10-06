import { type NextRequest, NextResponse } from "next/server"
import { spawn } from "child_process"
import path from "path"

export async function POST(request: NextRequest) {
  try {
    const { text } = await request.json()

    if (!text) {
      return NextResponse.json({ error: "Texto requerido" }, { status: 400 })
    }

    // Usar el analizador de sentimientos
    const analysis = await analyzeSentiment(text)

    return NextResponse.json(analysis)
  } catch (error) {
    console.error("Error procesando análisis de sentimientos:", error)
    return NextResponse.json({ error: "Error interno del servidor" }, { status: 500 })
  }
}

async function analyzeSentiment(text: string): Promise<any> {
  return new Promise((resolve, reject) => {
    const scriptPath = path.join(process.cwd(), 'scripts', 'sentiment_analyzer.py')
    console.log(`Ejecutando script de sentimientos: ${scriptPath}`)
    console.log(`Texto a analizar: ${text}`)
    
    const pythonProcess = spawn('py', [
      '-3.12',
      scriptPath,
      text
    ])

    let outputData = ''
    let errorData = ''

    pythonProcess.stdout.on('data', (data) => {
      outputData += data.toString()
    })

    pythonProcess.stderr.on('data', (data) => {
      errorData += data.toString()
      console.error(`Python Error: ${data}`)
    })

    pythonProcess.on('close', (code) => {
      console.log(`Python process exited with code ${code}`)
      console.log(`Output length: ${outputData.length}`)
      console.log(`Error: ${errorData}`)
      
      if (code !== 0) {
        console.error(`Python process exited with code ${code}`)
        // Fallback al análisis simulado si hay error
        resolve(generateFallbackSentiment(text))
        return
      }

      try {
        const result = JSON.parse(outputData)
        console.log('Resultado de sentimientos parseado correctamente')
        resolve(result)
      } catch (error) {
        console.error("Error parsing Python output:", error)
        console.error("Raw output:", outputData)
        // Fallback al análisis simulado si hay error de parsing
        resolve(generateFallbackSentiment(text))
      }
    })
  })
}

function generateFallbackSentiment(text: string) {
  // Análisis básico de sentimientos basado en palabras clave
  const positiveWords = ['bueno', 'excelente', 'genial', 'fantástico', 'maravilloso', 'increíble', 'perfecto', 'me gusta', 'amor', 'feliz']
  const negativeWords = ['malo', 'terrible', 'horrible', 'odio', 'triste', 'enojado', 'molesto', 'problema', 'difícil', 'mal']
  
  const lowerText = text.toLowerCase()
  
  let positiveCount = 0
  let negativeCount = 0
  
  positiveWords.forEach(word => {
    if (lowerText.includes(word)) positiveCount++
  })
  
  negativeWords.forEach(word => {
    if (lowerText.includes(word)) negativeCount++
  })
  
  let sentiment = "NEU"
  let confidence = 0.5
  
  if (positiveCount > negativeCount) {
    sentiment = "POS"
    confidence = Math.min(0.5 + (positiveCount * 0.1), 0.9)
  } else if (negativeCount > positiveCount) {
    sentiment = "NEG"
    confidence = Math.min(0.5 + (negativeCount * 0.1), 0.9)
  }
  
  return {
    text: text,
    sentiment: sentiment,
    confidence: confidence,
    probabilities: {
      POS: sentiment === "POS" ? confidence : (1 - confidence) / 2,
      NEG: sentiment === "NEG" ? confidence : (1 - confidence) / 2,
      NEU: sentiment === "NEU" ? confidence : (1 - confidence) / 2
    },
    model: "fallback-basic",
    timestamp: new Date().toISOString()
  }
}

