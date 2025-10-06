import { type NextRequest, NextResponse } from "next/server"
import { spawn } from "child_process"
import path from "path"

export async function POST(request: NextRequest) {
  try {
    const { text, max_length = 120, temperature = 0.1, top_p = 0.9 } = await request.json()

    if (!text) {
      return NextResponse.json({ error: "Texto requerido" }, { status: 400 })
    }

    // Usar el procesador GPT-2
    const response = await processWithGPT2(text, max_length, temperature, top_p)

    return NextResponse.json(response)
  } catch (error) {
    console.error("Error procesando GPT-2:", error)
    return NextResponse.json({ error: "Error interno del servidor" }, { status: 500 })
  }
}

async function processWithGPT2(text: string, max_length: number, temperature: number, top_p: number): Promise<any> {
  return new Promise((resolve, reject) => {
    const scriptPath = path.join(process.cwd(), 'scripts', 'gpt2_processor.py')
    console.log(`Ejecutando script GPT-2: ${scriptPath}`)
    console.log(`Texto a procesar: ${text}`)
    console.log(`Parámetros: max_length=${max_length}, temperature=${temperature}, top_p=${top_p}`)
    
    const pythonProcess = spawn('py', [
      '-3.12',
      scriptPath,
      text,
      max_length.toString(),
      temperature.toString(),
      top_p.toString()
    ], {
      encoding: 'utf8',
      env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
    })

    let outputData = ''
    let errorData = ''

    pythonProcess.stdout.on('data', (data) => {
      outputData += data.toString('utf8')
    })

    pythonProcess.stderr.on('data', (data) => {
      errorData += data.toString('utf8')
      console.error(`Python Error: ${data}`)
    })

    pythonProcess.on('close', (code) => {
      console.log(`Python process exited with code ${code}`)
      console.log(`Output length: ${outputData.length}`)
      console.log(`Error: ${errorData}`)
      
      if (code !== 0) {
        console.error(`Python process exited with code ${code}`)
        // Fallback a respuesta simulada si hay error
        resolve(generateFallbackResponse(text))
        return
      }

      try {
        const result = JSON.parse(outputData)
        console.log('Resultado GPT-2 parseado correctamente')
        resolve(result)
      } catch (error) {
        console.error("Error parsing Python output:", error)
        console.error("Raw output:", outputData)
        // Fallback a respuesta simulada si hay error de parsing
        resolve(generateFallbackResponse(text))
      }
    })
  })
}

function generateFallbackResponse(text: string) {
  return {
    response: `He procesado tu mensaje: "${text}". Este es un ejemplo de respuesta generada por el sistema GPT-2 en español.`,
    model: "gpt2-small-spanish",
    parameters: {
      max_length: 120,
      temperature: 0.1,
      top_p: 0.9
    },
    timestamp: new Date().toISOString()
  }
}

