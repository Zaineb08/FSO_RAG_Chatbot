import streamlit as st
import json
from main import ask_chatbot

# 🔹 Embeddings
DATA_FOLDER = "data"
EMBEDDINGS_FILE = f"{DATA_FOLDER}/embeddings.json"

with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
    embeddings = json.load(f)

# Config page
st.set_page_config(page_title="FSO Chatbot", page_icon="🎓")
st.markdown("<h2 style='text-align:center; color:#2F4F4F;'>🎓 Bienvenue sur le Chatbot FSO !</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#555;'>Posez votre question sur les formations Licence ou Master et obtenez des réponses précises.</p>", unsafe_allow_html=True)
st.write("---")

# Historique
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Menu déroulant pour filtrer
filter_option = st.selectbox(
    "Filtrer par type de formation :",
    ["Toutes", "Licence", "Master"]
)

# Formulaire pour la question
with st.form(key="chat_form", clear_on_submit=True):
    question = st.text_input("Votre question :", key="input")
    submit_button = st.form_submit_button("💬 Envoyer")

if submit_button and question:
    # Ici tu pourrais filtrer les embeddings selon filter_option si tu veux plus tard
    answer = ask_chatbot(question, embeddings)
    st.session_state.chat_history.append(("Vous", question))
    st.session_state.chat_history.append(("Chatbot", answer))

# Affichage du chat
for user, msg in st.session_state.chat_history:
    if user == "Vous":
        st.markdown(
            f"<div style='background-color:#A9D6E5; color:#000; padding:10px; border-radius:12px; margin:5px 0 5px 40%; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);'><b>{user}:</b> {msg}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='background-color:#B8E0D2; color:#000; padding:10px; border-radius:12px; margin:5px 40% 5px 0; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);'><b>{user}:</b> {msg}</div>",
            unsafe_allow_html=True
        )

# Bouton pour télécharger l'historique
if st.session_state.chat_history:
    history_json = json.dumps(st.session_state.chat_history, ensure_ascii=False, indent=2)
    st.download_button(
        "📥 Télécharger l'historique",
        data=history_json,
        file_name="chat_history.json",
        mime="application/json"
    )
