"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Separator } from "@/components/ui/separator"
import { Slider } from "@/components/ui/slider"
import { Send, Bot, User, Brain, Settings, Heart, Smile, Frown, Hash, Tag, Gamepad2 } from "lucide-react"

interface Message {
  id: string
  content: string
  sender: "user" | "bot"
  timestamp: Date
  gpt2Response?: GPT2Response
  sentimentAnalysis?: SentimentAnalysis
  nlpAnalysis?: NLPAnalysis
}

interface NLPAnalysis {
  tokens: string[]
  lemmas: { word: string; lemma: string; context?: string }[]
  posTags: { 
    word: string
    pos: string
    description: string
    relationship?: string
  }[]
  gamingAnalysis?: {
    is_gaming_related: boolean
    keywords: Array<{word: string, category: string}>
    games_mentioned: string[]
    categories: Record<string, number>
    semantic_analysis?: {
      gaming_words_found: string[]
      total_similarities: number
      similarities: Array<{
        word1: string
        word2: string
        similarity: number
        similarity_percentage: number
      }>
      most_similar_pairs: Array<{
        word1: string
        word2: string
        similarity: number
        similarity_percentage: number
      }>
      average_similarity: number
    }
    similar_terms?: Array<{
      rank: number
      word: string
      similarity: number
      similarity_percentage: number
    }>
  }
}

interface GPT2Response {
  response: string
  model: string
  parameters: {
    max_length: number
    temperature: number
    top_p: number
  }
  prompt: string
  timestamp: string
}

interface SentimentAnalysis {
  text: string
  sentiment: "POS" | "NEG" | "NEU"
  confidence: number
  probabilities: {
    POS: number
    NEG: number
    NEU: number
  }
  model: string
  timestamp: string
}

type ConversationState = "waiting_greeting" | "active" | "ended"

const SENTIMENT_COLORS = {
  POS: "bg-green-200 text-green-900",
  NEG: "bg-red-200 text-red-900", 
  NEU: "bg-gray-200 text-gray-900"
}

const SENTIMENT_ICONS = {
  POS: Smile,
  NEG: Frown,
  NEU: Heart
}

const POS_COLORS: { [key: string]: string } = {
  NOUN: "bg-blue-200 text-blue-900 font-medium",
  VERB: "bg-red-200 text-red-900 font-medium",
  ADJ: "bg-green-200 text-green-900 font-medium",
  ADV: "bg-yellow-200 text-yellow-900 font-medium",
  PRON: "bg-purple-200 text-purple-900 font-medium",
  DET: "bg-pink-200 text-pink-900 font-medium",
  ADP: "bg-indigo-200 text-indigo-900 font-medium",
  CCONJ: "bg-gray-200 text-gray-900 font-medium",
  SCONJ: "bg-gray-200 text-gray-900 font-medium",
  NUM: "bg-orange-200 text-orange-900 font-medium",
  PUNCT: "bg-slate-200 text-slate-900 font-medium",
  PROPN: "bg-emerald-200 text-emerald-900 font-medium",
  AUX: "bg-rose-200 text-rose-900 font-medium",
  PART: "bg-amber-200 text-amber-900 font-medium",
  INTJ: "bg-violet-200 text-violet-900 font-medium",
  SYM: "bg-neutral-200 text-neutral-900 font-medium",
  X: "bg-stone-200 text-stone-900 font-medium"
}

export function ChatbotInterface() {
  const [conversationState, setConversationState] = useState<ConversationState>("waiting_greeting")
  const [messageCount, setMessageCount] = useState(0)
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState("")
  const [isProcessing, setIsProcessing] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Configuración de parámetros GPT-2
  const [gpt2Config, setGpt2Config] = useState({
    max_length: 120,
    temperature: 0.1,
    top_p: 0.9
  })
  
  useEffect(() => {
    setMessages([
      {
        id: "1",
        content: "¡Hola! Soy tu asistente virtual con GPT-2 en español. ¿Qué tal estás?",
        sender: "bot",
        timestamp: new Date(),
      },
    ])
  }, [])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const detectGreeting = (text: string): boolean => {
    const greetings = ["hola", "hello", "hi", "buenos días", "buenas tardes", "buenas noches", "saludos"]
    return greetings.some((greeting) => text.toLowerCase().includes(greeting))
  }

  const detectFarewell = (text: string): boolean => {
    const farewells = ["adiós", "adios", "bye", "hasta luego", "nos vemos", "chao", "goodbye"]
    return farewells.some((farewell) => text.toLowerCase().includes(farewell))
  }

  const processGPT2 = async (text: string): Promise<GPT2Response> => {
    try {
      const response = await fetch("/api/gpt2-chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ 
          text,
          max_length: gpt2Config.max_length,
          temperature: gpt2Config.temperature,
          top_p: gpt2Config.top_p
        }),
      })

      if (response.ok) {
        const result = await response.json()
        return result
      } else {
        throw new Error("Error en la API GPT-2")
      }
    } catch (error) {
      console.log("Error con GPT-2, usando respuesta de fallback")
      return {
        response: `He recibido tu mensaje: "${text}". Este es un ejemplo de respuesta generada por GPT-2 en español.`,
        model: "gpt2-small-spanish-fallback",
        parameters: gpt2Config,
        prompt: text,
        timestamp: new Date().toISOString()
      }
    }
  }

  const processNLP = async (text: string): Promise<NLPAnalysis> => {
    try {
      const response = await fetch("/api/nlp-process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      })

      if (response.ok) {
        const analysis = await response.json()
        return analysis
      } else {
        return simulateNLPAnalysis(text)
      }
    } catch (error) {
      console.log("[v0] API NLP no disponible, usando análisis simulado")
      return simulateNLPAnalysis(text)
    }
  }

  const simulateNLPAnalysis = (text: string): NLPAnalysis => {
    // Tokenización mejorada que maneja puntuación
    const tokens = text.toLowerCase().match(/\b\w+\b/g) || []

    // Lematización mejorada con más reglas
    const lemmas = tokens.map((token) => ({
      word: token,
      lemma: getLemmaImproved(token),
    }))

    // POS Tagging mejorado
    const posTags = tokens.map((token) => ({
      word: token,
      pos: getPOSTagImproved(token),
      description: getPOSDescription(getPOSTagImproved(token)),
    }))
    
    // Análisis de contenido de videojuegos básico
    const isGamingRelated = text.toLowerCase().includes('juego') || 
                            text.toLowerCase().includes('videojuego') || 
                            text.toLowerCase().includes('consola') ||
                            text.toLowerCase().includes('gaming') ||
                            text.toLowerCase().includes('playstation') ||
                            text.toLowerCase().includes('xbox') ||
                            text.toLowerCase().includes('nintendo')
    
    const gamingAnalysis = {
      is_gaming_related: isGamingRelated,
      keywords: [],
      games_mentioned: [],
      categories: {},
      semantic_analysis: undefined,
      similar_terms: []
    }

    return { tokens, lemmas, posTags, gamingAnalysis }
  }

  const getLemmaImproved = (word: string): string => {
    const lemmaRules: { [key: string]: string } = {
      // Verbos en gerundio
      corriendo: "correr",
      comiendo: "comer",
      hablando: "hablar",
      estudiando: "estudiar",
      trabajando: "trabajar",
      jugando: "jugar",
      leyendo: "leer",
      escribiendo: "escribir",

      // Verbos conjugados
      corro: "correr",
      comes: "comer",
      habla: "hablar",
      estudias: "estudiar",
      trabajo: "trabajar",
      juegan: "jugar",
      lee: "leer",
      escribes: "escribir",

      // Sustantivos plurales
      casas: "casa",
      libros: "libro",
      niños: "niño",
      niñas: "niña",
      mujeres: "mujer",
      hombres: "hombre",
      estudiantes: "estudiante",
      profesores: "profesor",
      universidades: "universidad",
      escuelas: "escuela",

      // Adjetivos femeninos/plurales
      pequeña: "pequeño",
      pequeñas: "pequeño",
      pequeños: "pequeño",
      grande: "grande",
      grandes: "grande",
      buena: "bueno",
      buenas: "bueno",
      buenos: "bueno",

      // Adverbios
      rápidamente: "rápido",
      lentamente: "lento",
      fácilmente: "fácil",
      claramente: "claro",
      perfectamente: "perfecto",
    }

    // Reglas morfológicas básicas
    if (word.endsWith("mente")) {
      return word.replace("mente", "").replace("a$", "o")
    }
    if (word.endsWith("ando") || word.endsWith("iendo")) {
      return word.replace(/(ando|iendo)$/, "ar").replace("ier", "er")
    }
    if (word.endsWith("s") && word.length > 3) {
      return word.slice(0, -1)
    }

    return lemmaRules[word] || word
  }

  const getPOSTagImproved = (word: string): string => {
    const posRules: { [key: string]: string } = {
      // Determinantes
      el: "DET",
      la: "DET",
      los: "DET",
      las: "DET",
      un: "DET",
      una: "DET",
      este: "DET",
      esta: "DET",
      estos: "DET",
      estas: "DET",
      mi: "DET",
      tu: "DET",

      // Sustantivos comunes
      casa: "NOUN",
      libro: "NOUN",
      niño: "NOUN",
      mujer: "NOUN",
      hombre: "NOUN",
      estudiante: "NOUN",
      profesor: "NOUN",
      universidad: "NOUN",
      escuela: "NOUN",
      parque: "NOUN",
      cocina: "NOUN",
      gato: "NOUN",
      perro: "NOUN",
      ciudad: "NOUN",

      // Verbos
      es: "VERB",
      está: "VERB",
      son: "VERB",
      están: "VERB",
      tiene: "VERB",
      come: "VERB",
      estudia: "VERB",
      trabaja: "VERB",
      juega: "VERB",
      lee: "VERB",

      // Adjetivos
      grande: "ADJ",
      pequeño: "ADJ",
      bueno: "ADJ",
      malo: "ADJ",
      nuevo: "ADJ",
      viejo: "ADJ",
      rojo: "ADJ",
      azul: "ADJ",
      verde: "ADJ",
      amarillo: "ADJ",

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

      // Pronombres
      yo: "PRON",
      tú: "PRON",
      él: "PRON",
      ella: "PRON",
      nosotros: "PRON",
      me: "PRON",
      te: "PRON",
      se: "PRON",
      nos: "PRON",
      les: "PRON",

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

      // Conjunciones
      y: "CONJ",
      o: "CONJ",
      pero: "CONJ",
      aunque: "CONJ",
      porque: "CONJ",
      si: "CONJ",
      cuando: "CONJ",
      donde: "CONJ",
      como: "CONJ",
    }

    // Reglas heurísticas mejoradas
    if (word.endsWith("mente")) return "ADV"
    if (word.endsWith("ando") || word.endsWith("iendo")) return "VERB"
    if (word.endsWith("ción") || word.endsWith("sión")) return "NOUN"
    if (word.endsWith("dad") || word.endsWith("tad")) return "NOUN"

    return posRules[word] || "NOUN"
  }

  const getPOSDescription = (pos: string): string => {
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
    }

    return descriptions[pos] || "Desconocido"
  }

  const processSentiment = async (text: string): Promise<SentimentAnalysis> => {
    try {
      const response = await fetch("/api/sentiment-analysis", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      })

      if (response.ok) {
        const result = await response.json()
        return result
      } else {
        throw new Error("Error en la API de sentimientos")
      }
    } catch (error) {
      console.log("Error con análisis de sentimientos, usando análisis básico")
      // Análisis básico de fallback
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
      
      let sentiment: "POS" | "NEG" | "NEU" = "NEU"
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
  }

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: "user",
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    const currentInput = inputValue
    setInputValue("")
    setIsProcessing(true)

    if (conversationState === "waiting_greeting") {
      if (detectGreeting(currentInput)) {
        setConversationState("active")
        setMessageCount(1)

        // Procesar con GPT-2 y análisis de sentimientos
        const [gpt2Response, sentimentAnalysis, nlpAnalysis] = await Promise.all([
          processGPT2(currentInput),
          processSentiment(currentInput),
          processNLP(currentInput)
        ])

        const botMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: gpt2Response.response,
          sender: "bot",
          timestamp: new Date(),
          gpt2Response,
          sentimentAnalysis,
          nlpAnalysis,
        }

        setMessages((prev) => [...prev, botMessage])
      } else {
        const botMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: "Para iniciar nuestra conversación, necesito que me saludes primero diciendo 'hola'. Una vez que lo hagas, podremos conversar usando GPT-2.",
          sender: "bot",
          timestamp: new Date(),
        }

        setMessages((prev) => [...prev, botMessage])
      }
      setIsProcessing(false)
      return
    }

    if (conversationState === "active") {
      if (detectFarewell(currentInput)) {
        setConversationState("ended")

        // Procesar despedida
        const [gpt2Response, sentimentAnalysis, nlpAnalysis] = await Promise.all([
          processGPT2(currentInput),
          processSentiment(currentInput),
          processNLP(currentInput)
        ])

        const botMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: gpt2Response.response,
          sender: "bot",
          timestamp: new Date(),
          gpt2Response,
          sentimentAnalysis,
          nlpAnalysis,
        }

        setMessages((prev) => [...prev, botMessage])
      } else {
        const newMessageCount = messageCount + 1
        setMessageCount(newMessageCount)

        // Procesar con GPT-2 y análisis de sentimientos
        const [gpt2Response, sentimentAnalysis, nlpAnalysis] = await Promise.all([
          processGPT2(currentInput),
          processSentiment(currentInput),
          processNLP(currentInput)
        ])

        const botMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: gpt2Response.response,
          sender: "bot",
          timestamp: new Date(),
          gpt2Response,
          sentimentAnalysis,
          nlpAnalysis,
        }

        setMessages((prev) => [...prev, botMessage])
      }
      setIsProcessing(false)
      return
    }

    if (conversationState === "ended") {
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: "Nuestra conversación ya ha terminado. Si quieres iniciar una nueva conversación, recarga la página y salúdame nuevamente con 'hola'.",
        sender: "bot",
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, botMessage])
      setIsProcessing(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 max-w-7xl mx-auto">
      {/* Chat Interface */}
      <div className="lg:col-span-3">
        <Card className="h-[600px] flex flex-col">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Bot className="h-5 w-5 text-primary" />
              Chat con GPT-2 en Español
              <Badge
                variant={
                  conversationState === "active"
                    ? "default"
                    : conversationState === "ended"
                      ? "destructive"
                      : "secondary"
                }
              >
                {conversationState === "waiting_greeting" && "Esperando saludo"}
                {conversationState === "active" && `Activo (${messageCount} mensajes)`}
                {conversationState === "ended" && "Conversación terminada"}
              </Badge>
            </CardTitle>
          </CardHeader>
          <CardContent className="flex-1 flex flex-col">
            <ScrollArea className="flex-1 pr-4">
              <div className="space-y-4">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex gap-3 ${message.sender === "user" ? "justify-end" : "justify-start"}`}
                  >
                    <div
                      className={`flex gap-3 max-w-[80%] ${
                        message.sender === "user" ? "flex-row-reverse" : "flex-row"
                      }`}
                    >
                      <div className="flex-shrink-0">
                        {message.sender === "user" ? (
                          <div className="w-8 h-8 bg-secondary rounded-full flex items-center justify-center">
                            <User className="h-4 w-4 text-secondary-foreground" />
                          </div>
                        ) : (
                          <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
                            <Bot className="h-4 w-4 text-primary-foreground" />
                          </div>
                        )}
                      </div>
                      <div
                        className={`rounded-lg px-4 py-2 ${
                          message.sender === "user"
                            ? "bg-secondary text-secondary-foreground"
                            : "bg-card text-card-foreground border"
                        }`}
                      >
                        <p className="text-sm">{message.content}</p>
                        <p className="text-xs text-muted-foreground mt-1">
                          {message.timestamp.toLocaleTimeString()}
                        </p>
                        {message.sentimentAnalysis && (
                          <div className="mt-2 flex items-center gap-2">
                            <Badge variant="outline" className={`text-xs ${SENTIMENT_COLORS[message.sentimentAnalysis.sentiment]}`}>
                              {(() => {
                                const Icon = SENTIMENT_ICONS[message.sentimentAnalysis.sentiment]
                                return <Icon className="h-3 w-3 mr-1" />
                              })()}
                              {message.sentimentAnalysis.sentiment === "POS" ? "Positivo" : 
                               message.sentimentAnalysis.sentiment === "NEG" ? "Negativo" : "Neutral"}
                      </Badge>
                            <span className="text-xs text-muted-foreground">
                              {(message.sentimentAnalysis.confidence * 100).toFixed(0)}%
                            </span>
                    </div>
                  )}
                      </div>
                    </div>
                  </div>
                ))}
                {isProcessing && (
                  <div className="flex gap-3 justify-start">
                    <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
                      <Bot className="h-4 w-4 text-primary-foreground animate-pulse" />
                    </div>
                    <div className="bg-card text-card-foreground border rounded-lg px-4 py-2">
                      <p className="text-sm">Procesando con GPT-2...</p>
                    </div>
                  </div>
                )}
              </div>
              <div ref={messagesEndRef} />
            </ScrollArea>

            <Separator className="my-4" />

            <div className="flex gap-2">
              <Input
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={
                  conversationState === "waiting_greeting"
                    ? "Escribe 'hola' para comenzar..."
                    : conversationState === "ended"
                      ? "Conversación terminada. Recarga para empezar de nuevo."
                      : "Escribe tu mensaje aquí..."
                }
                className="flex-1"
                disabled={isProcessing || conversationState === "ended"}
              />
              <Button
                onClick={handleSendMessage}
                disabled={!inputValue.trim() || isProcessing || conversationState === "ended"}
                size="icon"
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Configuration and Analysis Panel */}
      <div className="space-y-4">
        {/* GPT-2 Configuration */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-lg">
              <Settings className="h-5 w-5 text-primary" />
              Configuración GPT-2
                  </CardTitle>
                </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium mb-2 block">
                Longitud máxima: {gpt2Config.max_length}
              </label>
              <Slider
                value={[gpt2Config.max_length]}
                onValueChange={(value) => setGpt2Config(prev => ({ ...prev, max_length: value[0] }))}
                max={200}
                min={50}
                step={10}
                className="w-full"
              />
            </div>
            
            <div>
              <label className="text-sm font-medium mb-2 block">
                Temperatura: {gpt2Config.temperature}
              </label>
              <Slider
                value={[gpt2Config.temperature]}
                onValueChange={(value) => setGpt2Config(prev => ({ ...prev, temperature: value[0] }))}
                max={1.0}
                min={0.1}
                step={0.1}
                className="w-full"
              />
            </div>
            
            <div>
              <label className="text-sm font-medium mb-2 block">
                Top-p: {gpt2Config.top_p}
              </label>
              <Slider
                value={[gpt2Config.top_p]}
                onValueChange={(value) => setGpt2Config(prev => ({ ...prev, top_p: value[0] }))}
                max={1.0}
                min={0.1}
                step={0.1}
                className="w-full"
              />
                  </div>
                </CardContent>
              </Card>

        {/* Last Message Analysis */}
        {messages
          .filter((m) => m.gpt2Response || m.sentimentAnalysis)
          .slice(-1)
          .map((message) => (
            <div key={`analysis-${message.id}`} className="space-y-4">
              {/* GPT-2 Response Info */}
              {message.gpt2Response && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-lg">
                    <Brain className="h-5 w-5 text-primary" />
                      Respuesta GPT-2
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="p-3 bg-blue-50 rounded-lg border border-blue-200">
                        <h4 className="text-sm font-medium text-blue-800 mb-2">Modelo</h4>
                        <Badge variant="outline" className="bg-blue-100 text-blue-800">
                          {message.gpt2Response.model}
                      </Badge>
                    </div>
                      
                      <div className="p-3 bg-green-50 rounded-lg border border-green-200">
                        <h4 className="text-sm font-medium text-green-800 mb-2">Parámetros</h4>
                        <div className="space-y-1 text-sm">
                          <div className="flex justify-between">
                            <span>Max Length:</span>
                            <span className="font-medium">{message.gpt2Response.parameters.max_length}</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Temperatura:</span>
                            <span className="font-medium">{message.gpt2Response.parameters.temperature}</span>
                        </div>
                          <div className="flex justify-between">
                            <span>Top-p:</span>
                            <span className="font-medium">{message.gpt2Response.parameters.top_p}</span>
                              </div>
                          </div>
                        </div>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Sentiment Analysis */}
              {message.sentimentAnalysis && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-lg">
                      <Heart className="h-5 w-5 text-primary" />
                      Análisis de Sentimientos
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="p-3 bg-purple-50 rounded-lg border border-purple-200">
                        <h4 className="text-sm font-medium text-purple-800 mb-2">Sentimiento Detectado</h4>
                        <div className="flex items-center gap-2">
                          <Badge className={`${SENTIMENT_COLORS[message.sentimentAnalysis.sentiment]}`}>
                            {(() => {
                              const Icon = SENTIMENT_ICONS[message.sentimentAnalysis.sentiment]
                              return <Icon className="h-3 w-3 mr-1" />
                            })()}
                            {message.sentimentAnalysis.sentiment === "POS" ? "Positivo" : 
                             message.sentimentAnalysis.sentiment === "NEG" ? "Negativo" : "Neutral"}
                            </Badge>
                          <span className="text-sm font-medium">
                            {(message.sentimentAnalysis.confidence * 100).toFixed(1)}%
                          </span>
                        </div>
                      </div>

                      <div className="p-3 bg-gray-50 rounded-lg border border-gray-200">
                        <h4 className="text-sm font-medium text-gray-800 mb-2">Probabilidades</h4>
                          <div className="space-y-2">
                          <div className="flex justify-between items-center">
                            <span className="text-sm">Positivo:</span>
                            <div className="flex items-center gap-2">
                              <div className="w-16 bg-gray-200 rounded-full h-2">
                                <div 
                                  className="bg-green-500 h-2 rounded-full" 
                                  style={{ width: `${message.sentimentAnalysis.probabilities.POS * 100}%` }}
                                ></div>
                              </div>
                              <span className="text-xs font-medium">
                                {(message.sentimentAnalysis.probabilities.POS * 100).toFixed(0)}%
                                </span>
                          </div>
                        </div>
                          <div className="flex justify-between items-center">
                            <span className="text-sm">Negativo:</span>
                            <div className="flex items-center gap-2">
                              <div className="w-16 bg-gray-200 rounded-full h-2">
                                <div 
                                  className="bg-red-500 h-2 rounded-full" 
                                  style={{ width: `${message.sentimentAnalysis.probabilities.NEG * 100}%` }}
                                ></div>
                              </div>
                              <span className="text-xs font-medium">
                                {(message.sentimentAnalysis.probabilities.NEG * 100).toFixed(0)}%
                                </span>
                          </div>
                        </div>
                          <div className="flex justify-between items-center">
                            <span className="text-sm">Neutral:</span>
                            <div className="flex items-center gap-2">
                              <div className="w-16 bg-gray-200 rounded-full h-2">
                                <div 
                                  className="bg-gray-500 h-2 rounded-full" 
                                  style={{ width: `${message.sentimentAnalysis.probabilities.NEU * 100}%` }}
                                ></div>
                          </div>
                              <span className="text-xs font-medium">
                                {(message.sentimentAnalysis.probabilities.NEU * 100).toFixed(0)}%
                              </span>
                          </div>
                        </div>
                        </div>
                      </div>
                      
                      <div className="p-3 bg-yellow-50 rounded-lg border border-yellow-200">
                        <h4 className="text-sm font-medium text-yellow-800 mb-2">Modelo</h4>
                        <Badge variant="outline" className="bg-yellow-100 text-yellow-800">
                          {message.sentimentAnalysis.model}
                        </Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* NLP Analysis */}
              {message.nlpAnalysis && (
                <div className="space-y-4">
                  {/* Tokenización */}
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2 text-lg">
                        <Hash className="h-5 w-5 text-primary" />
                        Tokenización
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-sm text-muted-foreground mb-3">
                        División del texto en unidades básicas (tokens). Total: {message.nlpAnalysis.tokens.length} tokens
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {message.nlpAnalysis.tokens?.map((token, index) => (
                          <Badge key={index} variant="outline" className="text-xs">
                            {index + 1}. {token}
                          </Badge>
                        ))}
                      </div>
                    </CardContent>
                  </Card>

                  {/* Lematización */}
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2 text-lg">
                        <Brain className="h-5 w-5 text-primary" />
                        Lematización
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-sm text-muted-foreground mb-3">
                        Forma base (lema) de cada palabra para análisis morfológico:
                      </p>
                      <div className="space-y-2">
                        {message.nlpAnalysis.lemmas?.map((lemma, index) => (
                          <div key={index} className="flex flex-col gap-1 p-3 bg-muted/50 rounded-lg hover:bg-muted/70 transition-colors">
                            <div className="flex justify-between items-center">
                              <span className="font-medium text-base">{lemma.word}</span>
                              <span className="text-lg text-primary">→</span>
                              <span className="italic text-primary font-semibold text-base">{lemma.lemma}</span>
                            </div>
                            {lemma.context && (
                              <span className="text-xs text-muted-foreground mt-1">
                                Contexto: {lemma.context}
                              </span>
                            )}
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>

                  {/* POS Tagging */}
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2 text-lg">
                        <Tag className="h-5 w-5 text-primary" />
                        Etiquetado POS
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-sm text-muted-foreground mb-3">
                        Categoría gramatical (Part-of-Speech) de cada palabra:
                      </p>
                      <div className="space-y-2">
                        {message.nlpAnalysis.posTags?.map((tag, index) => (
                          <div key={index} className="flex flex-col gap-2 p-3 bg-muted/50 rounded-lg hover:bg-muted/70 transition-colors">
                            <div className="flex items-center justify-between">
                              <span className="font-semibold text-base">{tag.word}</span>
                              <Badge className={`text-xs ${POS_COLORS[tag.pos] || "bg-gray-100 text-gray-800"}`}>
                                {tag.pos}
                              </Badge>
                            </div>
                            <div className="flex flex-col gap-1">
                              <span className="text-sm text-muted-foreground">
                                {tag.description}
                              </span>
                              {tag.relationship && (
                                <span className="text-xs text-muted-foreground/80 italic">
                                  Relación: {tag.relationship}
                                </span>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>

                  {/* Análisis de Videojuegos */}
                  {message.nlpAnalysis.gamingAnalysis && (
                    <Card>
                      <CardHeader>
                        <CardTitle className="flex items-center gap-2 text-lg">
                          <Gamepad2 className="h-5 w-5 text-primary" />
                          Análisis de Videojuegos
                        </CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-3">
                          <div className="flex items-center">
                            <span className="text-sm font-medium mr-2">Relacionado con videojuegos:</span>
                            <Badge variant={message.nlpAnalysis.gamingAnalysis.is_gaming_related ? "default" : "secondary"}>
                              {message.nlpAnalysis.gamingAnalysis.is_gaming_related ? "Sí" : "No"}
                            </Badge>
                          </div>
                          
                          {message.nlpAnalysis.gamingAnalysis.games_mentioned && message.nlpAnalysis.gamingAnalysis.games_mentioned.length > 0 && (
                            <div>
                              <span className="text-sm font-medium text-blue-700">Juegos mencionados:</span>
                              <div className="flex flex-wrap gap-1 mt-1">
                                {message.nlpAnalysis.gamingAnalysis.games_mentioned?.map((game, idx) => (
                                  <Badge key={idx} variant="outline" className="bg-blue-100 text-blue-800">{game}</Badge>
                                ))}
                              </div>
                            </div>
                          )}
                          
                          {message.nlpAnalysis.gamingAnalysis.keywords && message.nlpAnalysis.gamingAnalysis.keywords.length > 0 && (
                            <div>
                              <span className="text-sm font-medium text-blue-700">Palabras clave:</span>
                              <div className="flex flex-wrap gap-1 mt-1">
                                {message.nlpAnalysis.gamingAnalysis.keywords?.map((keyword, idx) => (
                                  <div key={idx} className="flex items-center">
                                    <Badge variant="outline" className="bg-blue-50">{keyword.word}</Badge>
                                    <span className="text-xs text-muted-foreground ml-1">({keyword.category})</span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      </CardContent>
                    </Card>
                  )}

                  {/* Embeddings Semánticos */}
                  {message.nlpAnalysis.gamingAnalysis?.semantic_analysis && (
                    <Card>
                      <CardHeader>
                        <CardTitle className="flex items-center gap-2 text-lg">
                          <Brain className="h-5 w-5 text-primary" />
                          Embeddings Semánticos
                        </CardTitle>
                      </CardHeader>
                      <CardContent>
                        <p className="text-sm text-muted-foreground mb-3">
                          Análisis de similitudes semánticas usando Word2Vec:
                        </p>
                        
                        <div className="space-y-4">
                          {/* Palabras gaming encontradas */}
                          <div className="p-3 bg-blue-50 rounded-lg border border-blue-200">
                            <h4 className="text-sm font-medium text-blue-800 mb-2">
                              Palabras Gaming Encontradas
                            </h4>
                            <div className="flex flex-wrap gap-1">
                              {message.nlpAnalysis.gamingAnalysis.semantic_analysis.gaming_words_found?.map((word, idx) => (
                                <Badge key={idx} variant="outline" className="bg-blue-100 text-blue-800">
                                  {word}
                                </Badge>
                              ))}
                            </div>
                          </div>

                          {/* Pares más similares */}
                          {message.nlpAnalysis.gamingAnalysis.semantic_analysis.most_similar_pairs && 
                           message.nlpAnalysis.gamingAnalysis.semantic_analysis.most_similar_pairs.length > 0 && (
                              <div className="p-3 bg-green-50 rounded-lg border border-green-200">
                                <h4 className="text-sm font-medium text-green-800 mb-2">
                                  Pares Más Similares
                                </h4>
                                <div className="space-y-2">
                                  {message.nlpAnalysis.gamingAnalysis.semantic_analysis.most_similar_pairs?.map((pair, idx) => (
                                    <div key={idx} className="flex items-center justify-between p-2 bg-white rounded border">
                                      <span className="text-sm">
                                        <span className="font-medium">{pair.word1}</span> ↔ <span className="font-medium">{pair.word2}</span>
                                      </span>
                                      <Badge variant="outline" className="bg-green-100 text-green-800">
                                        {pair.similarity_percentage}%
                                      </Badge>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}

                          {/* Términos similares */}
                          {message.nlpAnalysis.gamingAnalysis.similar_terms && 
                           message.nlpAnalysis.gamingAnalysis.similar_terms.length > 0 && (
                              <div className="p-3 bg-purple-50 rounded-lg border border-purple-200">
                                <h4 className="text-sm font-medium text-purple-800 mb-2">
                                  Términos Similares
                                </h4>
                                <div className="space-y-2">
                                  {message.nlpAnalysis.gamingAnalysis.similar_terms?.slice(0, 5).map((term, idx) => (
                                    <div key={idx} className="flex items-center justify-between p-2 bg-white rounded border">
                                      <span className="text-sm">
                                        {term.rank}. <span className="font-medium">{term.word}</span>
                                      </span>
                                      <Badge variant="outline" className="bg-purple-100 text-purple-800">
                                        {term.similarity_percentage}%
                                      </Badge>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}

                          {/* Estadísticas generales */}
                          <div className="p-3 bg-gray-50 rounded-lg border border-gray-200">
                            <h4 className="text-sm font-medium text-gray-800 mb-2">
                              Estadísticas Semánticas
                            </h4>
                            <div className="grid grid-cols-2 gap-2 text-sm">
                              <div className="flex justify-between">
                                <span>Total similitudes:</span>
                                <span className="font-medium">{message.nlpAnalysis.gamingAnalysis.semantic_analysis.total_similarities}</span>
                              </div>
                              <div className="flex justify-between">
                                <span>Similitud promedio:</span>
                                <span className="font-medium">{message.nlpAnalysis.gamingAnalysis.semantic_analysis.average_similarity?.toFixed(3)}</span>
                              </div>
                            </div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  )}
                </div>
              )}
            </div>
          ))}

        {messages.filter((m) => m.gpt2Response || m.sentimentAnalysis || m.nlpAnalysis).length === 0 && (
          <Card>
            <CardContent className="pt-6">
              <div className="text-center text-muted-foreground">
            <div className="flex justify-center items-center gap-2">
              <Brain className="h-12 w-12 opacity-50" />
                  <Heart className="h-12 w-12 opacity-50" />
            </div>
            <p className="text-sm mt-4">
              {conversationState === "waiting_greeting"
                    ? "Saluda con 'hola' para comenzar a conversar con GPT-2"
                    : "Envía un mensaje para ver la respuesta de GPT-2 y análisis de sentimientos"}
            </p>
          </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}