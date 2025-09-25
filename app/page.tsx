import { ChatbotInterface } from "@/components/chatbot-interface"

export default function Home() {
  return (
    <main className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-4">Chatbot de Procesamiento de Lenguaje Natural</h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          
          </p>
        </div>
        <ChatbotInterface />
      </div>
    </main>
  )
}
