function ChatMessage({ message, onRetry }) {
  const isUser = message.sender === "user";
  const isError = message.isError || false;

  const formatTime = (date) => {
    return date.toLocaleTimeString("fr-FR", {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <div className={`message-wrapper ${isUser ? "user" : "bot"}`}>
      <div
        className={`message-bubble ${isUser ? "user" : "bot"} ${
          isError ? "error" : ""
        }`}
      >
        <p className="message-text">{message.text}</p>
        <div className="message-footer">
          <span className="message-timestamp">
            {formatTime(message.timestamp)}
          </span>
          {isError && onRetry && (
            <button
              className="retry-button"
              onClick={onRetry}
              title="Réessayer"
            >
              🔄 Réessayer
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default ChatMessage;
