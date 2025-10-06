import { ChatbotInterface } from "@/components/chatbot-interface"

export default function Home() {
  return (
    <main className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-4">Chatbot con GPT-2 en Español</h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Conversa con un modelo GPT-2 entrenado en español y obtén análisis de sentimientos en tiempo real
          </p>
        </div>
        <ChatbotInterface />
      </div>
    </main>
  )
}
