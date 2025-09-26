"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Separator } from "@/components/ui/separator"
import { Send, Bot, User, Brain, Tag, Hash, Gamepad2 } from "lucide-react"

// Importamos funciones del módulo de conocimiento de videojuegos
import { get_gaming_response, is_gaming_related, analyze_gaming_content } from "@/lib/gaming_knowledge"

interface Message {
  id: string
  content: string
  sender: "user" | "bot"
  timestamp: Date
  analysis?: NLPAnalysis
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

type ConversationState = "waiting_greeting" | "active" | "ended"

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
  
  useEffect(() => {
    setMessages([
      {
        id: "1",
        content: "¡Hola! Soy tu asistente virtual. ¿Qué tal estás?",
        sender: "bot",
        timestamp: new Date(),
      },
    ])
  }, [])
  const [inputValue, setInputValue] = useState("")
  const [isProcessing, setIsProcessing] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

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

  const generateConversationalResponse = (userText: string, messageCount: number): string => {
    try {
      // Intentamos usar el módulo de conocimiento de videojuegos para generar respuestas
      return get_gaming_response(userText)
    } catch (error) {
      console.error("Error al generar respuesta de videojuegos:", error)
      
      // Respuestas de fallback relacionadas con videojuegos
      const gamingResponses = [
        `Interesante lo que dices sobre videojuegos: "${userText}". ¿Tienes algún juego favorito?`,
        `Me parece muy bien tu mensaje: "${userText}". ¿Qué género de videojuegos prefieres?`,
        `Gracias por compartir: "${userText}". ¿Qué consola o plataforma usas para jugar?`,
        `Perfecto, has escrito: "${userText}". Los videojuegos han evolucionado mucho en las últimas décadas.`,
        `Excelente ejemplo: "${userText}". ¿Prefieres juegos indie o AAA?`,
        `Muy bien, analizando: "${userText}". ¿Qué opinas de los juegos de mundo abierto?`,
        `Genial tu texto: "${userText}". ¿Has probado algún juego de realidad virtual?`,
        `Fantástico: "${userText}". ¿Sigues algún streamer o creador de contenido de videojuegos?`,
      ]
      
      // Respuestas para mensajes fuera del tema de videojuegos
      const offTopicResponses = [
        "Estamos hablando de videojuegos. Si tienes alguna pregunta o comentario sobre juegos, consolas, o la industria gaming, estaré encantado de seguir la conversación.",
        "Parece que nos estamos desviando del tema de los videojuegos. ¿Te gustaría que volvamos a hablar sobre algún aspecto del mundo gaming?",
        "Como especialista en videojuegos, puedo ofrecerte información sobre juegos, plataformas, géneros y más. ¿Hay algo específico del mundo gaming que te interese?",
        "Mi conocimiento se centra en videojuegos. Si quieres hablar de otro tema, puedo intentar relacionarlo con el mundo de los videojuegos si es posible.",
        "Estoy especializado en conversar sobre videojuegos. ¿Quieres que hablemos sobre algún juego, consola o tendencia reciente en la industria?",
      ]

      // Verificar si el mensaje está relacionado con videojuegos
      const isGamingRelated = userText.toLowerCase().includes('juego') || 
                              userText.toLowerCase().includes('videojuego') || 
                              userText.toLowerCase().includes('consola') ||
                              userText.toLowerCase().includes('gaming') ||
                              userText.toLowerCase().includes('playstation') ||
                              userText.toLowerCase().includes('xbox') ||
                              userText.toLowerCase().includes('nintendo')

      // Respuestas especiales para ciertos números de mensaje
      if (messageCount === 1) {
        return `¡Perfecto! Ahora que hemos iniciado la conversación, puedes escribir sobre videojuegos y te mostraré su análisis completo. Has escrito: "${userText}".`
      } else if (messageCount % 5 === 0) {
        return `¡Llevamos ${messageCount} intercambios! Sigues escribiendo textos interesantes como: "${userText}". ¿Qué juegos has estado jugando últimamente?`
      }

      // Si el mensaje no está relacionado con videojuegos, redirigir la conversación
      if (!isGamingRelated) {
        return offTopicResponses[Math.floor(Math.random() * offTopicResponses.length)]
      }
      
      return gamingResponses[Math.floor(Math.random() * gamingResponses.length)]
    }
  }

  const processNLP = async (text: string): Promise<NLPAnalysis> => {
    setIsProcessing(true)

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
      console.log("[v0] API no disponible, usando análisis simulado")
      return simulateNLPAnalysis(text)
    } finally {
      setIsProcessing(false)
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
      semantic_analysis: null,
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

    if (conversationState === "waiting_greeting") {
      if (detectGreeting(currentInput)) {
        setConversationState("active")
        setMessageCount(1)

        const botMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: `¡Excelente! Ahora que nos hemos saludado, nuestra conversación ha comenzado. Puedes escribir cualquier texto y te mostraré su análisis completo de PLN. Has escrito: "${currentInput}".`,
          sender: "bot",
          timestamp: new Date(),
          analysis: await processNLP(currentInput),
        }

        setMessages((prev) => [...prev, botMessage])
      } else {
        const botMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: `Para iniciar nuestra conversación, necesito que me saludes primero diciendo 'hola'. Una vez que lo hagas, podremos conversar y analizar cualquier texto que escribas.`,
          sender: "bot",
          timestamp: new Date(),
        }

        setMessages((prev) => [...prev, botMessage])
      }
      return
    }

    if (conversationState === "active") {
      if (detectFarewell(currentInput)) {
        setConversationState("ended")

        const botMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: `¡Ha sido un placer conversar contigo! Espero que hayas aprendido mucho sobre el procesamiento de lenguaje natural. Analizamos tu despedida: "${currentInput}". ¡Hasta la próxima!`,
          sender: "bot",
          timestamp: new Date(),
          analysis: await processNLP(currentInput),
        }

        setMessages((prev) => [...prev, botMessage])
      } else {
        const newMessageCount = messageCount + 1
        setMessageCount(newMessageCount)

        // Procesar PLN
        const analysis = await processNLP(currentInput)

        const botMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: generateConversationalResponse(currentInput, newMessageCount),
          sender: "bot",
          timestamp: new Date(),
          analysis,
        }

        setMessages((prev) => [...prev, botMessage])
      }
      return
    }

    if (conversationState === "ended") {
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: `Nuestra conversación ya ha terminado. Si quieres iniciar una nueva conversación, recarga la página y salúdame nuevamente con 'hola'.`,
        sender: "bot",
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, botMessage])
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 max-w-7xl mx-auto">
      {/* Chat Interface */}
      <div className="lg:col-span-2">
        <Card className="h-[600px] flex flex-col">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Bot className="h-5 w-5 text-primary" />
              <Gamepad2 className="h-5 w-5 text-primary" />
              Chat de Videojuegos con PLN 
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
                  <p className="text-xs text-muted-foreground mt-1">{message.timestamp.toLocaleTimeString()}</p>
                  {message.analysis?.gamingAnalysis?.is_gaming_related && (
                    <div className="mt-1">
                      <Badge variant="outline" className="bg-green-100 text-green-800 text-xs">
                        <Gamepad2 className="h-3 w-3 mr-1" /> Gaming
                      </Badge>
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
                      <p className="text-sm">Procesando análisis de PLN...</p>
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

      {/* Analysis Panel */}
      <div className="space-y-4">
        {messages
          .filter((m) => m.analysis)
          .slice(-1)
          .map((message) => (
            <div key={`analysis-${message.id}`} className="space-y-4">
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
                    División del texto en unidades básicas (tokens). Total: {message.analysis?.tokens.length} tokens
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {message.analysis?.tokens?.map((token, index) => (
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
                    {message.analysis?.lemmas?.map((lemma, index) => (
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
                    {message.analysis?.pos_tags?.map((tag, index) => (
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
              {message.analysis?.gaming_analysis && (
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
                      <Badge variant={message.analysis.gaming_analysis.is_gaming_related ? "default" : "secondary"}>
                        {message.analysis.gaming_analysis.is_gaming_related ? "Sí" : "No"}
                      </Badge>
                    </div>
                      
                      {message.analysis.gaming_analysis.games_mentioned && message.analysis.gaming_analysis.games_mentioned.length > 0 && (
                        <div>
                          <span className="text-sm font-medium text-blue-700">Juegos mencionados:</span>
                          <div className="flex flex-wrap gap-1 mt-1">
                            {message.analysis.gaming_analysis.games_mentioned?.map((game, idx) => (
                              <Badge key={idx} variant="outline" className="bg-blue-100 text-blue-800">{game}</Badge>
                            ))}
                          </div>
                        </div>
                      )}
                      
                      {message.analysis.gaming_analysis.keywords && message.analysis.gaming_analysis.keywords.length > 0 && (
                        <div>
                          <span className="text-sm font-medium text-blue-700">Palabras clave:</span>
                          <div className="flex flex-wrap gap-1 mt-1">
                            {message.analysis.gaming_analysis.keywords?.map((keyword, idx) => (
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
              {message.analysis?.gaming_analysis?.semantic_analysis && (
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
                          {message.analysis.gaming_analysis.semantic_analysis.gaming_words_found?.map((word, idx) => (
                            <Badge key={idx} variant="outline" className="bg-blue-100 text-blue-800">
                              {word}
                            </Badge>
                          ))}
                        </div>
                      </div>

                      {/* Pares más similares */}
                    {message.analysis.gaming_analysis.semantic_analysis.most_similar_pairs && 
                     message.analysis.gaming_analysis.semantic_analysis.most_similar_pairs.length > 0 && (
                        <div className="p-3 bg-green-50 rounded-lg border border-green-200">
                          <h4 className="text-sm font-medium text-green-800 mb-2">
                            Pares Más Similares
                          </h4>
                          <div className="space-y-2">
                            {message.analysis.gaming_analysis.semantic_analysis.most_similar_pairs?.map((pair, idx) => (
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
                    {message.analysis.gaming_analysis.similar_terms && 
                     message.analysis.gaming_analysis.similar_terms.length > 0 && (
                        <div className="p-3 bg-purple-50 rounded-lg border border-purple-200">
                          <h4 className="text-sm font-medium text-purple-800 mb-2">
                            Términos Similares
                          </h4>
                          <div className="space-y-2">
                            {message.analysis.gaming_analysis.similar_terms?.slice(0, 5).map((term, idx) => (
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
                            <span className="font-medium">{message.analysis.gaming_analysis.semantic_analysis.total_similarities}</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Similitud promedio:</span>
                            <span className="font-medium">{message.analysis.gaming_analysis.semantic_analysis.average_similarity?.toFixed(3)}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>
          ))}

        {messages.filter((m) => m.analysis).length === 0 && (
          <Card>
            <CardContent className="pt-6">
              <div className="text-center text-muted-foreground">
            <div className="flex justify-center items-center gap-2">
              <Brain className="h-12 w-12 opacity-50" />
              <Gamepad2 className="h-12 w-12 opacity-50" />
            </div>
            <p className="text-sm mt-4">
              {conversationState === "waiting_greeting"
                ? "Saluda con 'hola' para comenzar a hablar de videojuegos y ver el análisis de PLN"
                : "Envía un mensaje sobre videojuegos para ver el análisis de PLN en tiempo real"}
            </p>
          </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}
