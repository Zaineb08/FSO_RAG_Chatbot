import os
import json
import pandas as pd
from PyPDF2 import PdfReader
from openai import OpenAI, api_key
from numpy import dot, linalg

# 🔹 Clé OpenAI depuis l'environnement
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("La clé API OpenAI n'est pas définie. Veuillez la définir dans un fichier .env")

client = OpenAI(api_key=api_key)

# 🔹 Dossiers
PDF_FOLDER = "pdfs"
DATA_FOLDER = "data"
EMBEDDINGS_FILE = f"{DATA_FOLDER}/embeddings.json"
EXTRACTED_FILE_JSON = f"{DATA_FOLDER}/extracted_data.json"
EXTRACTED_FILE_CSV = f"{DATA_FOLDER}/extracted_data.csv"

# 1️⃣ Extraire les PDFs
def extract_text_from_pdfs(pdf_folder=PDF_FOLDER):
    pdf_texts = []
    for root, dirs, files in os.walk(pdf_folder):
        for filename in files:
            if filename.endswith(".pdf"):
                path = os.path.join(root, filename)
                reader = PdfReader(path)
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                pdf_texts.append({"filename": os.path.relpath(path, pdf_folder), "text": text})
    return pdf_texts

# 2️⃣ Segmenter en paragraphes
def segment_documents(pdf_texts):
    documents = []
    for pdf in pdf_texts:
        paragraphs = pdf["text"].split("\n\n")
        for para in paragraphs:
            para = para.strip()
            if len(para) > 50:
                documents.append({"content": para, "source": pdf["filename"]})
    return documents

# 3️⃣ Export des données extraites
def save_extracted_data(documents):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    # JSON
    with open(EXTRACTED_FILE_JSON, "w", encoding="utf-8") as f:
        json.dump(documents, f, indent=2, ensure_ascii=False)
    # CSV
    df = pd.DataFrame(documents)
    df.to_csv(EXTRACTED_FILE_CSV, index=False)
    print(f"✅ Données extraites sauvegardées : {EXTRACTED_FILE_JSON} et {EXTRACTED_FILE_CSV}")

# 4️⃣ Génération embeddings
def generate_embeddings(documents):
    embeddings = []
    for doc in documents:
        response = client.embeddings.create(
            model="text-embedding-3-large",
            input=doc["content"]
        )
        embeddings.append({
            "content": doc["content"],
            "embedding": response.data[0].embedding,
            "source": doc["source"]
        })
    # Sauvegarde
    os.makedirs(DATA_FOLDER, exist_ok=True)
    with open(EMBEDDINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(embeddings, f)
    print(f"✅ Embeddings sauvegardés dans {EMBEDDINGS_FILE}")
    return embeddings

# 5️⃣ Cosine similarity et récupération
def cosine_similarity(a, b):
    return dot(a, b) / (linalg.norm(a) * linalg.norm(b))

def retrieve_relevant_paragraphs(question, embeddings, top_k=5):
    q_emb = client.embeddings.create(
        model="text-embedding-3-large",
        input=question
    ).data[0].embedding
    similarities = [(doc, cosine_similarity(q_emb, doc["embedding"])) for doc in embeddings]
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [doc[0]["content"] for doc in similarities[:top_k]]

# 6️⃣ Chatbot
def ask_chatbot(question, embeddings):
    relevant_paragraphs = retrieve_relevant_paragraphs(question, embeddings)
    context = "\n".join(relevant_paragraphs)
    prompt = f"""
Tu es un chatbot académique intelligent conçu pour répondre aux questions 
concernant les formations de la Faculté des Sciences d'Oujda (FSO).

RÈGLES DE COMPORTEMENT :
1. Si la question est une salutation ("bonjour", "salam", "bonsoir", etc.), réponds simplement par une salutation naturelle, sans présenter les filières.
2. Si la question est vague, demande poliment une précision.
3. Si la question est claire, utilise uniquement le CONTEXTE donné ci-dessous pour répondre.
4. Ne jamais inventer des informations qui ne figurent pas dans le contexte.
5. Réponds de manière courte, claire et structurée.
6. Si tu ne trouves pas la réponse dans le contexte, réponds : 
   "Je n'ai pas trouvé cette information dans les documents officiels."

FORMAT DE RÉPONSE :
- Utilise systématiquement des retours à la ligne.
- Sépare les idées par des paragraphes courts.
- Liste les éléments sous forme de points :
  • Puces simples (•)
  • Ou numérotation (1., 2., 3.)
- Aère bien la réponse pour une meilleure lisibilité.
CONTEXTE :
{context}

QUESTION :
{question}

RÉPONSE :
"""
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content

# 🔹 Main
if __name__ == "__main__":
    # 1️⃣ Charger ou générer embeddings
    if os.path.exists(EMBEDDINGS_FILE):
        print("📂 Chargement des embeddings existants...")
        with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
            embeddings = json.load(f)
    else:
        print("📄 Extraction des PDFs...")
        pdf_texts = extract_text_from_pdfs()
        documents = segment_documents(pdf_texts)
        print(f"✅ {len(documents)} paragraphes extraits.")
        
        # Export des données extraites
        save_extracted_data(documents)
        
        # Génération des embeddings
        print("⚡ Génération des embeddings (cela peut prendre quelques minutes)...")
        embeddings = generate_embeddings(documents)

    # 2️⃣ Boucle interactive console
    print("\n💬 Chatbot prêt ! Tape 'exit' pour quitter.")
    while True:
        question = input("\nQuestion: ")
        if question.lower() in ["exit", "quit"]:
            break
        answer = ask_chatbot(question, embeddings)
        print("\nAnswer:", answer)
