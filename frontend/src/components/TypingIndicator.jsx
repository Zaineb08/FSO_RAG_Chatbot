function TypingIndicator() {
  return (
    <div className="typing-indicator">
      <div className="typing-bubble">
        <span className="typing-text">En train de réfléchir</span>
        <div className="typing-dots">
          <span className="typing-dot">.</span>
          <span className="typing-dot">.</span>
          <span className="typing-dot">.</span>
        </div>
      </div>
    </div>
  );
}

export default TypingIndicator;
