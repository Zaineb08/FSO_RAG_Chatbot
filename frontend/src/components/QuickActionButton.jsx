function QuickActionButton({ text, onClick, disabled = false }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className="quick-action-button"
    >
      {text}
    </button>
  );
}

export default QuickActionButton;
