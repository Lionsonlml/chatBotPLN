import { type NextRequest, NextResponse } from "next/server"
import { spawn } from "child_process"
import path from "path"

export async function POST(request: NextRequest) {
  try {
    const { text } = await request.json()

    if (!text) {
      return NextResponse.json({ error: "Texto requerido" }, { status: 400 })
    }

    // Usar el procesador con embeddings
    const analysis = await processTextWithEmbeddings(text)

    return NextResponse.json(analysis)
  } catch (error) {
    console.error("Error procesando PLN:", error)
    return NextResponse.json({ error: "Error interno del servidor" }, { status: 500 })
  }
}

async function processTextWithEmbeddings(text: string): Promise<any> {
  return new Promise((resolve, reject) => {
    const scriptPath = path.join(process.cwd(), 'scripts', 'nlp_processor_with_embeddings.py')
    console.log(`Ejecutando script: ${scriptPath}`)
    console.log(`Texto a procesar: ${text}`)
    
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
        resolve(enhancedNLPAnalysis(text))
        return
      }

      try {
        const result = JSON.parse(outputData)
        console.log('Resultado parseado correctamente')
        resolve(result)
      } catch (error) {
        console.error("Error parsing Python output:", error)
        console.error("Raw output:", outputData)
        // Fallback al análisis simulado si hay error de parsing
        resolve(enhancedNLPAnalysis(text))
      }
    })
  })
}

function enhancedNLPAnalysis(text: string) {
  // Tokenización mejorada que maneja mejor la puntuación y casos especiales
  const tokens = text
    .toLowerCase()
    .replace(/[^\w\sáéíóúüñ]/g, " ") // Mantener caracteres españoles
    .split(/\s+/)
    .filter((token) => token.length > 0)

  // Lematización mejorada con más reglas morfológicas
  const lemmas = tokens.map((token) => ({
    word: token,
    lemma: getEnhancedLemma(token),
  }))

  // POS Tagging mejorado con mayor precisión
  const posTags = tokens.map((token) => ({
    word: token,
    pos: getEnhancedPOSTag(token),
    description: getPOSDescription(getEnhancedPOSTag(token)),
  }))

  return { tokens, lemmas, posTags }
}

function getEnhancedLemma(word: string): string {
  const lemmaRules: { [key: string]: string } = {
    // Verbos en gerundio (-ando, -iendo)
    corriendo: "correr",
    comiendo: "comer",
    hablando: "hablar",
    estudiando: "estudiar",
    trabajando: "trabajar",
    jugando: "jugar",
    leyendo: "leer",
    escribiendo: "escribir",
    viviendo: "vivir",
    aprendiendo: "aprender",
    enseñando: "enseñar",
    pensando: "pensar",

    // Verbos conjugados (presente)
    corro: "correr",
    corres: "correr",
    corre: "correr",
    corremos: "correr",
    corren: "correr",
    como: "comer",
    comes: "comer",
    come: "comer",
    comemos: "comer",
    comen: "comer",
    hablo: "hablar",
    hablas: "hablar",
    habla: "hablar",
    hablamos: "hablar",
    hablan: "hablar",
    estudio: "estudiar",
    estudias: "estudiar",
    estudia: "estudiar",
    estudiamos: "estudiar",
    estudian: "estudiar",

    // Verbos ser/estar
    soy: "ser",
    eres: "ser",
    es: "ser",
    somos: "ser",
    son: "ser",
    estoy: "estar",
    estás: "estar",
    está: "estar",
    estamos: "estar",
    están: "estar",

    // Sustantivos plurales
    casas: "casa",
    libros: "libro",
    niños: "niño",
    niñas: "niña",
    estudiantes: "estudiante",
    profesores: "profesor",
    profesoras: "profesor",
    universidades: "universidad",
    escuelas: "escuela",
    algoritmos: "algoritmo",
    técnicas: "técnica",
    modelos: "modelo",
    análisis: "análisis",

    // Adjetivos (femenino/plural)
    pequeña: "pequeño",
    pequeñas: "pequeño",
    pequeños: "pequeño",
    grande: "grande",
    grandes: "grande",
    buena: "bueno",
    buenas: "bueno",
    buenos: "bueno",
    inteligente: "inteligente",
    inteligentes: "inteligente",
    fascinante: "fascinante",
    fascinantes: "fascinante",
    avanzada: "avanzado",
    avanzadas: "avanzado",
    avanzados: "avanzado",

    // Adverbios
    rápidamente: "rápido",
    lentamente: "lento",
    fácilmente: "fácil",
    claramente: "claro",
    perfectamente: "perfecto",
    significativamente: "significativo",
    colaborativamente: "colaborativo",

    // Participios
    aprendido: "aprender",
    enseñado: "enseñar",
    desarrollado: "desarrollar",
    mejorado: "mejorar",
    combinado: "combinar",
    procesado: "procesar",
  }

  // Aplicar reglas morfológicas automáticas
  let lemma = lemmaRules[word]

  if (!lemma) {
    // Regla 1: Adverbios terminados en -mente
    if (word.endsWith("mente")) {
      const base = word.slice(0, -5) // Quitar 'mente'
      if (base.endsWith("a")) {
        lemma = base.slice(0, -1) + "o" // rápidamente -> rápido
      } else {
        lemma = base
      }
    }
    // Regla 2: Gerundios
    else if (word.endsWith("ando")) {
      lemma = word.slice(0, -4) + "ar" // hablando -> hablar
    } else if (word.endsWith("iendo")) {
      lemma = word.slice(0, -5) + "er" // comiendo -> comer
    }
    // Regla 3: Participios
    else if (word.endsWith("ado")) {
      lemma = word.slice(0, -3) + "ar" // hablado -> hablar
    } else if (word.endsWith("ido")) {
      lemma = word.slice(0, -3) + "er" // comido -> comer
    }
    // Regla 4: Plurales simples
    else if (word.endsWith("es") && word.length > 3) {
      lemma = word.slice(0, -2) // profesores -> profesor
    } else if (word.endsWith("s") && word.length > 2 && !word.endsWith("ss")) {
      lemma = word.slice(0, -1) // libros -> libro
    }
    // Regla 5: Femeninos a masculinos
    else if (word.endsWith("a") && word.length > 2) {
      const masculine = word.slice(0, -1) + "o"
      // Verificar si es un cambio válido (no para palabras como "casa")
      const feminineSuffixes = ["pequeñ", "buen", "mal", "primer", "tercer"]
      if (feminineSuffixes.some((suffix) => word.startsWith(suffix))) {
        lemma = masculine
      } else {
        lemma = word // Mantener original si no es un adjetivo claro
      }
    }
    // Regla 6: Sustantivos con sufijos típicos (mantener como están)
    else if (word.endsWith("ción") || word.endsWith("sión") || word.endsWith("dad") || word.endsWith("tad")) {
      lemma = word // Estos ya están en forma base
    } else {
      lemma = word // Sin cambio
    }
  }

  return lemma || word
}

function getEnhancedPOSTag(word: string): string {
  const posRules: { [key: string]: string } = {
    // Determinantes
    el: "DET",
    la: "DET",
    los: "DET",
    las: "DET",
    un: "DET",
    una: "DET",
    unos: "DET",
    unas: "DET",
    este: "DET",
    esta: "DET",
    estos: "DET",
    estas: "DET",
    ese: "DET",
    esa: "DET",
    esos: "DET",
    esas: "DET",
    aquel: "DET",
    aquella: "DET",
    aquellos: "DET",
    aquellas: "DET",
    mi: "DET",
    tu: "DET",
    su: "DET",
    nuestro: "DET",
    vuestro: "DET",

    // Sustantivos comunes y técnicos
    casa: "NOUN",
    libro: "NOUN",
    niño: "NOUN",
    niña: "NOUN",
    mujer: "NOUN",
    hombre: "NOUN",
    estudiante: "NOUN",
    profesor: "NOUN",
    profesora: "NOUN",
    universidad: "NOUN",
    escuela: "NOUN",
    parque: "NOUN",
    cocina: "NOUN",
    gato: "NOUN",
    perro: "NOUN",
    ciudad: "NOUN",
    procesamiento: "NOUN",
    lenguaje: "NOUN",
    natural: "ADJ",
    disciplina: "NOUN",
    lingüística: "NOUN",
    computación: "NOUN",
    algoritmo: "NOUN",
    técnica: "NOUN",
    modelo: "NOUN",
    análisis: "NOUN",
    tokenización: "NOUN",
    lematización: "NOUN",
    precisión: "NOUN",
    desarrollo: "NOUN",
    inteligencia: "NOUN",

    // Verbos (diferentes formas)
    es: "VERB",
    está: "VERB",
    son: "VERB",
    están: "VERB",
    tiene: "VERB",
    tienen: "VERB",
    hay: "VERB",
    come: "VERB",
    comen: "VERB",
    estudia: "VERB",
    estudian: "VERB",
    trabaja: "VERB",
    trabajan: "VERB",
    juega: "VERB",
    juegan: "VERB",
    lee: "VERB",
    leen: "VERB",
    escribe: "VERB",
    escriben: "VERB",
    aprende: "VERB",
    aprenden: "VERB",
    enseña: "VERB",
    enseñan: "VERB",
    combina: "VERB",
    combinan: "VERB",
    mejora: "VERB",
    mejoran: "VERB",
    desarrolla: "VERB",
    desarrollan: "VERB",
    procesa: "VERB",
    procesan: "VERB",

    // Adjetivos
    grande: "ADJ",
    pequeño: "ADJ",
    pequeña: "ADJ",
    bueno: "ADJ",
    buena: "ADJ",
    malo: "ADJ",
    mala: "ADJ",
    nuevo: "ADJ",
    nueva: "ADJ",
    viejo: "ADJ",
    vieja: "ADJ",
    rojo: "ADJ",
    azul: "ADJ",
    verde: "ADJ",
    amarillo: "ADJ",
    blanco: "ADJ",
    negro: "ADJ",
    fascinante: "ADJ",
    inteligente: "ADJ",
    avanzado: "ADJ",
    avanzada: "ADJ",
    colaborativo: "ADJ",
    colaborativa: "ADJ",
    significativo: "ADJ",
    significativa: "ADJ",

    // Adverbios
    muy: "ADV",
    más: "ADV",
    menos: "ADV",
    bien: "ADV",
    mal: "ADV",
    aquí: "ADV",
    allí: "ADV",
    ahora: "ADV",
    después: "ADV",
    antes: "ADV",
    siempre: "ADV",
    nunca: "ADV",
    también: "ADV",
    solo: "ADV",
    sólo: "ADV",
    rápidamente: "ADV",
    lentamente: "ADV",
    claramente: "ADV",
    perfectamente: "ADV",
    significativamente: "ADV",
    colaborativamente: "ADV",

    // Pronombres
    yo: "PRON",
    tú: "PRON",
    él: "PRON",
    ella: "PRON",
    nosotros: "PRON",
    nosotras: "PRON",
    vosotros: "PRON",
    vosotras: "PRON",
    ellos: "PRON",
    ellas: "PRON",
    usted: "PRON",
    ustedes: "PRON",
    me: "PRON",
    te: "PRON",
    se: "PRON",
    nos: "PRON",
    os: "PRON",
    les: "PRON",
    los: "PRON",
    que: "PRON",
    quien: "PRON",
    quienes: "PRON",
    cual: "PRON",
    cuales: "PRON",

    // Preposiciones
    de: "PREP",
    en: "PREP",
    con: "PREP",
    por: "PREP",
    para: "PREP",
    sin: "PREP",
    sobre: "PREP",
    bajo: "PREP",
    desde: "PREP",
    hasta: "PREP",
    entre: "PREP",
    durante: "PREP",
    mediante: "PREP",
    según: "PREP",
    contra: "PREP",

    // Conjunciones
    y: "CONJ",
    e: "CONJ",
    o: "CONJ",
    u: "CONJ",
    pero: "CONJ",
    mas: "CONJ",
    aunque: "CONJ",
    porque: "CONJ",
    si: "CONJ",
    cuando: "CONJ",
    donde: "CONJ",
    como: "CONJ",
    mientras: "CONJ",
    antes: "CONJ",
    después: "CONJ",

    // Números
    uno: "NUM",
    dos: "NUM",
    tres: "NUM",
    cuatro: "NUM",
    cinco: "NUM",
    primero: "NUM",
    segundo: "NUM",
    tercero: "NUM",
    último: "NUM",

    // Interrogativos
    qué: "PRON",
    cómo: "ADV",
    cuándo: "ADV",
    dónde: "ADV",
    por: "PREP",
    quién: "PRON",
    cuál: "PRON",
    cuánto: "ADV",
    cuánta: "ADV",
  }

  // Verificar diccionario primero
  if (posRules[word]) {
    return posRules[word]
  }

  // Reglas heurísticas mejoradas

  // Adverbios terminados en -mente
  if (word.endsWith("mente")) {
    return "ADV"
  }

  // Gerundios y participios
  if (word.endsWith("ando") || word.endsWith("iendo")) {
    return "VERB"
  }

  if (word.endsWith("ado") || word.endsWith("ido")) {
    return "VERB" // Participios
  }

  // Sustantivos con sufijos típicos
  if (
    word.endsWith("ción") ||
    word.endsWith("sión") ||
    word.endsWith("dad") ||
    word.endsWith("tad") ||
    word.endsWith("eza") ||
    word.endsWith("ura") ||
    word.endsWith("ismo") ||
    word.endsWith("ista") ||
    word.endsWith("miento") ||
    word.endsWith("aje")
  ) {
    return "NOUN"
  }

  // Adjetivos con sufijos típicos
  if (
    word.endsWith("oso") ||
    word.endsWith("osa") ||
    word.endsWith("ivo") ||
    word.endsWith("iva") ||
    word.endsWith("able") ||
    word.endsWith("ible") ||
    word.endsWith("ante") ||
    word.endsWith("ente")
  ) {
    return "ADJ"
  }

  // Infinitivos
  if (word.endsWith("ar") || word.endsWith("er") || word.endsWith("ir")) {
    return "VERB"
  }

  // Plurales (probablemente sustantivos)
  if (word.endsWith("s") && word.length > 2) {
    return "NOUN"
  }

  // Por defecto, asumir sustantivo (es la categoría más común)
  return "NOUN"
}

function getPOSDescription(pos: string): string {
  const descriptions: { [key: string]: string } = {
    NOUN: "Sustantivo",
    VERB: "Verbo",
    ADJ: "Adjetivo",
    ADV: "Adverbio",
    PRON: "Pronombre",
    DET: "Determinante",
    PREP: "Preposición",
    CONJ: "Conjunción",
    NUM: "Número",
    PUNCT: "Puntuación",
    INTJ: "Interjección",
  }

  return descriptions[pos] || "Desconocido"
}