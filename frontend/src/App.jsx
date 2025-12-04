import { useState, useRef, useEffect } from "react";
import "./App.css";
import ChatMessage from "./components/ChatMessage";
import TypingIndicator from "./components/TypingIndicator";
import QuickActionButton from "./components/QuickActionButton";

const STORAGE_KEY = "fso_chatbot_messages";

function App() {
  const [inputValue, setInputValue] = useState("");
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState(null);
  const [retryingMessageId, setRetryingMessageId] = useState(null);
  const chatContainerRef = useRef(null);

  const quickActions = [
    "Quelles sont les formations Licence disponibles ?",
    "Comment s'inscrire en Master ?",
    "Quels sont les critères d'admission ?",
    "Informations sur les frais de scolarité",
  ];

  // Load messages from localStorage on mount
  useEffect(() => {
    const savedMessages = localStorage.getItem(STORAGE_KEY);
    if (savedMessages) {
      try {
        const parsed = JSON.parse(savedMessages);
        // Convert timestamp strings back to Date objects
        const messagesWithDates = parsed.map((msg) => ({
          ...msg,
          timestamp: new Date(msg.timestamp),
        }));
        setMessages(messagesWithDates);
      } catch (e) {
        console.error("Error loading messages from localStorage:", e);
      }
    }
  }, []);

  // Save messages to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
  }, [messages]);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  const handleSendMessage = async (text, messageIdToRetry = null) => {
    const messageText = text || inputValue.trim();
    if (!messageText) return;

    setError(null);

    // If retrying, don't add a new user message
    if (!messageIdToRetry) {
      const userMessage = {
        id: Date.now().toString(),
        text: messageText,
        sender: "user",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, userMessage]);
      setInputValue("");
    }

    setIsTyping(true);

    try {
      const response = await fetch("http://127.0.0.1:5000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: messageText }),
      });

      if (!response.ok) {
        throw new Error(`Erreur serveur: ${response.status}`);
      }

      const data = await response.json();

      // Add bot response
      const botMessage = {
        id: (Date.now() + 1).toString(),
        text: data.answer || "Désolé, je n'ai pas pu obtenir de réponse.",
        sender: "bot",
        timestamp: new Date(),
        isError: false,
      };

      setMessages((prev) => [...prev, botMessage]);
      setRetryingMessageId(null);
    } catch (error) {
      console.error("Error asking chatbot:", error);

      // Add error message with retry option
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        text: `Désolé, une erreur est survenue: ${error.message}. Veuillez réessayer.`,
        sender: "bot",
        timestamp: new Date(),
        isError: true,
      };

      setMessages((prev) => [...prev, errorMessage]);
      setError(error.message);
      setRetryingMessageId(messageIdToRetry);
    } finally {
      setIsTyping(false);
    }
  };

  const handleQuickAction = (question) => {
    handleSendMessage(question);
  };

  const handleRetry = (userQuestion) => {
    handleSendMessage(userQuestion);
  };

  const handleClearChat = () => {
    if (
      window.confirm("Êtes-vous sûr de vouloir effacer l'historique du chat ?")
    ) {
      setMessages([]);
      localStorage.removeItem(STORAGE_KEY);
      setError(null);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Get the last user message for retry
  const getLastUserMessage = () => {
    for (let i = messages.length - 1; i >= 0; i--) {
      if (messages[i].sender === "user") {
        return messages[i].text;
      }
    }
    return null;
  };

  return (
    <div className="app-wrapper">
      <div className="app-container">
        {/* Header */}
        <header className="app-header">
          <div className="header-content">
            <h1>Chatbot FSO</h1>
            <p className="subtitle">FACULTÉ DES SCIENCES OUJDA</p>
            <p className="description">
              Posez vos questions sur les formations Licence et Master
            </p>
          </div>
          {messages.length > 0 && (
            <button
              className="clear-button"
              onClick={handleClearChat}
              title="Effacer l'historique"
            >
              🗑️
            </button>
          )}
        </header>

        {/* Chat Container */}
        <div className="chat-container">
          {/* Messages Area */}
          <div ref={chatContainerRef} className="chat-history">
            {messages.length === 0 && !isTyping && (
              <div className="welcome-screen">
                <div className="welcome-content">
                  <div className="welcome-icon">💬</div>
                  <h2 className="welcome-title">Bienvenue au Chatbot FSO</h2>
                  <p className="welcome-text">
                    Commencez la conversation en posant une question ou en
                    sélectionnant une action rapide ci-dessous
                  </p>
                </div>
                <div className="quick-actions-grid">
                  {quickActions.map((action, index) => (
                    <QuickActionButton
                      key={index}
                      text={action}
                      onClick={() => handleQuickAction(action)}
                    />
                  ))}
                </div>
              </div>
            )}

            {messages.map((message) => (
              <ChatMessage
                key={message.id}
                message={message}
                onRetry={
                  message.isError
                    ? () => {
                        const lastUserMsg = getLastUserMessage();
                        if (lastUserMsg) handleRetry(lastUserMsg);
                      }
                    : null
                }
              />
            ))}

            {isTyping && <TypingIndicator />}
          </div>

          {/* Quick Actions (shown when there are messages) */}
          {messages.length > 0 && (
            <div className="quick-actions-bar">
              {quickActions.map((action, index) => (
                <QuickActionButton
                  key={index}
                  text={action}
                  onClick={() => handleQuickAction(action)}
                  disabled={isTyping}
                />
              ))}
            </div>
          )}

          {/* Input Bar */}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
            className="chat-form"
          >
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Tapez votre message..."
              disabled={isTyping}
              className="chat-input"
            />
            <button
              type="submit"
              disabled={isTyping || !inputValue.trim()}
              className="send-button"
              title={isTyping ? "Traitement en cours..." : "Envoyer"}
            >
              {isTyping ? "⏳" : "💬"} Envoyer
            </button>
          </form>
        </div>

        {/* Footer */}
        <footer className="app-footer">
          <p>
            © 2025 Faculté des Sciences Oujda | <a href="#">Contact</a> |{" "}
            <a href="#">À propos</a>
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;
