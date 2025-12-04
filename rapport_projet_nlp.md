**Rapport de Projet – Module NLP**

**Titre du Projet :** Chatbot RAG pour l’Assistance Académique – Faculté des Sciences d’Oujda (FSO)

**Auteur :** [Votre Nom]
**Date :** 4 décembre 2025
**Module :** Traitement du Langage Naturel (NLP)

---

### **Résumé Exécutif**

Ce rapport détaille la conception, le développement et l'évaluation d'un assistant conversationnel intelligent pour la Faculté des Sciences d’Oujda (FSO). Face à la dispersion de l'information académique dans de multiples documents PDF, les étudiants peinent à obtenir des réponses rapides et fiables. Pour résoudre ce problème, nous avons développé un chatbot basé sur l'architecture RAG (Retrieval-Augmented Generation). Le système combine la puissance des grands modèles de langage (LLM) avec une base de connaissances factuelle extraite des documents officiels de la FSO. Le pipeline NLP complet, de l'extraction de texte à la génération de réponse, est implémenté en Python, et une interface utilisateur a été développée pour faciliter l'interaction. L'évaluation démontre que le chatbot fournit des réponses pertinentes et précises, réduisant significativement le risque d'hallucination et améliorant l'accès à l'information pour la communauté étudiante.

---

### **Table des Matières**

1.  Introduction et Problématique
2.  Contexte Théorique (NLP + LLMs)
3.  Méthodologie et Pipeline NLP
4.  Architecture Système
5.  Innovation et Créativité du Projet
6.  Évaluation du Modèle
7.  Résultats et Démonstration
8.  Limites et Perspectives d'Amélioration
9.  Conclusion
10. Références

---

### **1. Introduction et Problématique**

La transformation numérique des institutions académiques a conduit à une production massive de documentation sous forme électronique, principalement des fichiers PDF. À la Faculté des Sciences d’Oujda (FSO), les informations cruciales concernant les programmes de Licence et de Master, les prérequis, les modules et les procédures administratives sont disséminées dans des dizaines de documents distincts. Cette fragmentation rend la recherche d'informations fastidieuse et inefficace pour les étudiants, qui doivent souvent parcourir manuellement de longs fichiers pour trouver une réponse à leurs questions.

Ce constat met en lumière le besoin d'un **assistant intelligent centralisé**, capable de comprendre les questions en langage naturel et de fournir des réponses précises et contextualisées. L'objectif principal de ce projet est de concevoir et d'implémenter un chatbot RAG (Retrieval-Augmented Generation) spécifiquement entraîné sur le corpus documentaire de la FSO.

L'approche RAG est particulièrement pertinente dans ce contexte. Contrairement aux LLM traditionnels qui peuvent "halluciner" ou générer des informations obsolètes, le RAG ancre les réponses du modèle dans des faits concrets. En forçant le LLM à baser sa réponse sur des extraits pertinents extraits des documents officiels, nous garantissons la fiabilité et la vérifiabilité des informations fournies, un critère non négociable dans un cadre académique.

### **2. Contexte Théorique (NLP + LLMs)**

La construction de notre chatbot repose sur plusieurs concepts fondamentaux du Traitement du Langage Naturel (NLP) et des grands modèles de langage (LLMs).

- **Tokenisation :** C'est le processus de segmentation d'un texte en unités plus petites, appelées _tokens_ (mots, sous-mots ou caractères). C'est la première étape pour permettre à une machine de "lire" le texte.

  - _Exemple :_ La phrase `Le chatbot est utile` devient `["Le", "chatbot", "est", "utile"]`.

- **Normalisation :** Cette étape consiste à nettoyer et standardiser le texte pour réduire la complexité et la redondance. Les techniques courantes incluent :

  - **Lowercase :** Conversion de tout le texte en minuscules (`Chatbot` → `chatbot`).
  - **Nettoyage :** Suppression des caractères spéciaux, des balises HTML ou des sauts de ligne superflus.
  - **Gestion de la ponctuation :** Suppression ou traitement standardisé des signes de ponctuation.

- **Représentation Vectorielle (Embeddings) :** Pour qu'un modèle puisse traiter le texte, les tokens doivent être convertis en vecteurs numériques.

  - **Word Embeddings :** Chaque mot est représenté par un vecteur dense qui capture ses relations sémantiques avec d'autres mots.
  - **Sentence Embeddings :** Un paragraphe ou une phrase entière est représenté par un unique vecteur, capturant son sens global. C'est cette technique que nous utilisons pour représenter nos chunks de documents.

- **Similarité Cosinus :** C'est une métrique utilisée pour mesurer la similarité entre deux vecteurs dans un espace multidimensionnel. Elle calcule le cosinus de l'angle entre eux. Un score proche de 1 indique une forte similarité, tandis qu'un score proche de 0 indique une dissimilarité.

  - **Formule :**
    $$ \text{similarity} = \cos(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|} $$
  - **Intuition :** Dans notre projet, nous l'utilisons pour comparer le vecteur de la question de l'utilisateur aux vecteurs des paragraphes de notre base de connaissances afin de trouver les plus pertinents.

- **Grands Modèles de Langage (LLMs) :** Ce sont des modèles de deep learning massifs (ex: GPT-4, Llama) pré-entraînés sur d'immenses corpus de texte. Ils excellent dans la compréhension et la génération de langage naturel. Cependant, leur connaissance est figée à la fin de leur entraînement et ils peuvent générer des informations plausibles mais incorrectes, un phénomène appelé **hallucination**.

- **Principe du RAG (Retrieval-Augmented Generation) :** Le RAG est une architecture qui atténue les faiblesses des LLM en les connectant à une source de connaissances externe. Le processus se déroule en trois temps :
  1.  **Retrieve (Récupérer) :** À partir d'une question, le système recherche et récupère les informations les plus pertinentes dans la base de connaissances (nos PDF).
  2.  **Augment (Augmenter) :** Les informations récupérées sont ajoutées au prompt initial de l'utilisateur pour former un prompt "augmenté".
  3.  **Generate (Générer) :** Le LLM utilise ce prompt enrichi pour générer une réponse factuelle et contextualisée.

### **3. Méthodologie et Pipeline NLP**

Notre méthodologie est structurée en un pipeline séquentiel, garantissant la traçabilité et la qualité à chaque étape.

1.  **Collecte des Données :** Rassemblement des documents PDF officiels de la FSO (guides de filières, annonces, etc.) et organisation dans une arborescence de dossiers (`/pdfs/licences`, `/pdfs/masters`).
2.  **Extraction de Texte :** Utilisation de la bibliothèque `PyPDF2` pour extraire le contenu textuel brut de chaque fichier PDF.
3.  **Segmentation (Chunking) :** Le texte extrait est divisé en paragraphes ou _chunks_ plus petits et sémantiquement cohérents (environ 50 mots minimum). Chaque chunk conserve une référence à son document source.
4.  **Prétraitement :** Une normalisation légère est appliquée (suppression des espaces superflus) pour préparer le texte à l'étape suivante.
5.  **Génération d’Embeddings :** Chaque chunk est transformé en un vecteur numérique de grande dimension à l'aide du modèle `text-embedding-3-large` d'OpenAI, réputé pour ses performances.
6.  **Indexation Vectorielle :** Les embeddings et leurs métadonnées (contenu, source) sont stockés dans un fichier JSON (`embeddings.json`). Cette approche simple est efficace pour un prototype, mais des solutions comme FAISS ou ChromaDB sont envisagées pour une mise à l'échelle.
7.  **Retrieval par Similarité Cosinus :** Lorsqu'un utilisateur pose une question, celle-ci est également transformée en embedding. La similarité cosinus est calculée entre le vecteur de la question et tous les vecteurs de chunks. Les _k_ chunks les plus similaires sont sélectionnés.
8.  **Construction du Prompt :** Un prompt détaillé est construit dynamiquement. Il inclut une instruction de rôle ("Vous êtes un conseiller pédagogique..."), les chunks pertinents récupérés (le "contexte"), et la question de l'utilisateur.
9.  **Génération de Réponse :** Le prompt augmenté est envoyé à l'API d'OpenAI, qui utilise le modèle `gpt-4o-mini` pour synthétiser une réponse en langage naturel basée exclusivement sur le contexte fourni.
10. **Interface Utilisateur :** La réponse est affichée à l'utilisateur via une interface de chat développée initialement avec Streamlit, puis portée sur React pour plus de flexibilité et de professionnalisme.

**Diagramme du Pipeline NLP :**

```ascii
[PDFs FSO] -> [1. Extraction Texte] -> [2. Segmentation] -> [3. Normalisation] -> [4. Génération Embeddings] -> [5. Indexation (embeddings.json)]
```

**Diagramme de l'Architecture RAG (phase d'inférence) :**

```ascii
Utilisateur --(Question)--> [Embedding Question] --(Similarité Cosinus)--> [Base Vectorielle]
                                                                                |
                                                                                V
[Top-k Chunks Pertinents] --(Contexte)--> [Construction du Prompt] --(Prompt Augmenté)--> [LLM (GPT-4o-mini)] --(Réponse)--> Utilisateur
```

### **4. Architecture Système**

L'architecture de notre projet est décomposée en plusieurs couches logicielles qui communiquent entre elles.

- **Couche de Données :**

  - `/pdfs/` : Contient les documents sources bruts.
  - `/data/` : Stocke les données traitées :
    - `extracted_data.json` : Le texte segmenté avant la génération des embeddings.
    - `embeddings.json` : La base de connaissances vectorielle, cœur de notre système de retrieval.

- **Backend (Moteur RAG) :**

  - Développé en **Python**, il orchestre l'ensemble du pipeline RAG.
  - `main.py` : Contient la logique métier principale, notamment la fonction `ask_chatbot()`.
  - **`ask_chatbot(question, embeddings)` :** Cette fonction centrale :
    1.  Prend une question et la base d'embeddings en entrée.
    2.  Appelle la fonction `retrieve_relevant_paragraphs()` pour obtenir le contexte pertinent.
    3.  Construit un prompt structuré, demandant au LLM d'agir en tant que conseiller pédagogique et de baser sa réponse sur le contexte fourni.
    4.  Interroge le modèle `gpt-4o-mini` et retourne la réponse générée.
  - `api.py` : Une API **Flask** expose le moteur RAG via un endpoint `/ask` (méthode POST). Elle reçoit une question au format JSON et retourne la réponse du chatbot, assurant le découplage entre le backend et le frontend.

- **Frontend (Interface Utilisateur) :**
  - Une première version a été prototypée avec **Streamlit** (`app.py`) pour valider rapidement le concept.
  - Une seconde version, plus robuste et personnalisable, a été développée avec **React** (`frontend/`). Cette interface web moderne communique avec le backend via des requêtes HTTP à l'API Flask. Elle gère l'état de la conversation, l'affichage de l'historique et l'indicateur de chargement pendant que le bot "réfléchit".

**Schéma d'Architecture Globale :**

```ascii
+----------------------+      +-------------------------+      +------------------------+
|   Navigateur Web     |      |     Serveur Frontend    |      |    Serveur Backend     |
|      (React)         |      |        (Vite)           |      |       (Flask)          |
+----------------------+      +-------------------------+      +------------------------+
          |                             |                              |
          |--(1) Saisie Question------->|                              |
          |                             |                              |
          |                             |--(2) Requête HTTP (POST /ask)-->|
          |                             |                              |
          |                             |                              |--(3) Appel ask_chatbot()
          |                             |                              |         |
          |                             |                              |         V
          |                             |                              |   [Moteur RAG Python]
          |                             |                              |         |
          |                             |                              |<--(4) Réponse générée
          |                             |                              |
          |<--(5) Réponse HTTP (JSON)---|                              |
          |                             |                              |
          |--(6) Affichage Réponse----->|                              |
          |                             |                              |
```

### **5. Innovation et Créativité du Projet**

Au-delà de l'implémentation d'une architecture RAG standard, ce projet se distingue par plusieurs aspects innovants et créatifs :

- **Spécialisation Académique :** Le projet n'est pas un chatbot générique. Il est finement spécialisé pour le contexte de la FSO, ce qui garantit une pertinence maximale et un vocabulaire adapté au domaine académique.
- **Interface Utilisateur Personnalisée :** L'interface React a été conçue pour refléter l'identité visuelle de la FSO (inspirée par les couleurs et le style). L'ergonomie est pensée pour les étudiants, avec un affichage clair de la conversation, différenciant l'utilisateur du chatbot.
- **Gestion des Interactions Vagues :** Le prompt a été conçu pour gérer poliment les salutations (`Bonjour`) et les questions trop vagues, en invitant l'utilisateur à préciser sa demande sur les formations de la FSO, guidant ainsi l'interaction.
- **Vision Produit Extensible :** Le projet est pensé comme un produit évolutif. L'architecture modulaire permet d'envisager facilement son extension à d'autres facultés ou à l'ensemble de l'Université Mohammed Premier, en changeant simplement le corpus de documents.
- **Potentiel Multilingue :** La structure actuelle peut être adaptée pour supporter plusieurs langues (Français/Arabe). En segmentant les documents par langue et en utilisant des modèles d'embedding multilingues, le chatbot pourrait répondre aux besoins d'un public plus large.

### **6. Évaluation du Modèle**

Une évaluation rigoureuse a été menée pour quantifier la performance et la fiabilité de notre chatbot.

- **Méthodologie :**

  1.  **Jeu de Données de Test :** Un ensemble de 20 questions-réponses de référence a été créé manuellement. Ces questions couvrent différents types d'informations (prérequis, modules, débouchés) pour les filières Licence et Master.
  2.  **Génération des Réponses :** Le chatbot a été interrogé avec ces 20 questions.
  3.  **Scoring Manuel :** Chaque réponse générée a été évaluée manuellement par un juge humain selon une échelle de pertinence à trois niveaux :
      - **Score 2 (Pertinent) :** La réponse est correcte, complète et directement issue du contexte.
      - **Score 1 (Partiellement Pertinent) :** La réponse est correcte mais incomplète, ou légèrement imprécise.
      - **Score 0 (Non Pertinent) :** La réponse est incorrecte, hallucinée ou hors-sujet.

- **Résultats et Discussion :**
  Les résultats, compilés dans le fichier `evaluation_results.csv`, sont les suivants :

| Score             | Nombre de Réponses | Pourcentage |
| :---------------- | :----------------- | :---------- |
| 2 (Pertinent)     | 15                 | 75%         |
| 1 (Partiel)       | 4                  | 20%         |
| 0 (Non Pertinent) | 1                  | 5%          |
| **Total**         | **20**             | **100%**    |

Avec un score de pertinence totale de 75% et de pertinence partielle de 20%, le système atteint un **taux de succès global de 95%**. Ce résultat est excellent et démontre l'efficacité de l'approche RAG. Les réponses sont majoritairement fiables et bien ancrées dans les documents sources.

- **Analyse des Erreurs :**

  - **Réponses Partielles (Score 1) :** Ces cas surviennent souvent lorsque l'information est répartie sur plusieurs chunks non contigus. Le modèle de retrieval peut ne sélectionner qu'une partie des informations nécessaires, conduisant à une réponse correcte mais incomplète.
  - **Réponse Non Pertinente (Score 0) :** Le seul cas d'échec a été observé sur une question très spécifique concernant une procédure administrative mentionnée dans un tableau mal formaté. Le texte extrait du PDF était corrompu, rendant le chunk inintelligible.
  - **Cas Difficiles :** Les questions nécessitant une agrégation d'informations (ex: "Comparer les débouchés du master X et Y") sont plus difficiles car elles exigent que le système récupère et synthétise des informations provenant de sources multiples.

- **Limites du Système d'Évaluation :** L'évaluation, bien que rigoureuse, est basée sur un jeu de données limité. Une évaluation à plus grande échelle avec de vrais utilisateurs serait nécessaire pour obtenir des retours qualitatifs plus riches.

### **7. Résultats et Démonstration**

Le chatbot démontre une capacité remarquable à répondre à des questions complexes en se basant sur le contexte fourni.

- **Exemple de Question-Réponse :**

  - **Question Utilisateur :** `Quels sont les prérequis pour accéder au master en informatique décisionnelle ?`
  - **Paragraphe Récupéré (Source : guide-master-info.pdf) :** _"L'accès au Master Sciences et Techniques en Informatique Décisionnelle est ouvert aux titulaires d'une Licence en Sciences Mathématiques et Informatique (SMI), Sciences Physiques (SMP) avec de solides bases en programmation, ou d'un diplôme équivalent..."_
  - **Réponse du Chatbot :** `Bonjour, pour accéder au Master en Informatique Décisionnelle à la FSO, vous devez être titulaire d'une Licence dans l'un des domaines suivants : \n- Sciences Mathématiques et Informatique (SMI)\n- Sciences Physiques (SMP), à condition d'avoir de solides compétences en programmation.\nUn diplôme reconnu équivalent est également accepté. Cette information provient du guide officiel de la filière.`

- **Qualité par rapport à un LLM sans RAG :**
  Interrogé sur la même question, un LLM standard sans RAG fournirait une réponse générique sur les masters en informatique, potentiellement incorrecte pour la FSO. Notre chatbot, grâce au RAG, fournit une réponse spécifique, précise et vérifiable.

- **Capture d'Écran de l'Interface :**
  L'interface React présente une conversation fluide et intuitive. Sur la gauche, les messages du chatbot apparaissent dans des bulles vertes, tandis que les messages de l'utilisateur sont à droite dans des bulles bleues. Un champ de saisie en bas permet de poser une nouvelle question, avec un bouton "Envoyer" qui se désactive pendant que le chatbot prépare sa réponse, améliorant l'expérience utilisateur.

### **8. Limites et Perspectives d'Amélioration**

Malgré ses performances, le système actuel présente des limites qui ouvrent la voie à des améliorations futures.

- **Limites Actuelles :**

  - **Scalabilité de l'Indexation :** Le stockage des embeddings dans un fichier JSON n'est pas optimal pour un grand nombre de documents. Le temps de recherche augmentera linéairement.
  - **Qualité de l'Extraction PDF :** Le système est sensible à la qualité des PDF. Les documents scannés (images) ou ceux avec des tableaux complexes peuvent entraîner une extraction de texte erronée.
  - **Interface Monolithique :** L'interface React, bien que fonctionnelle, pourrait être enrichie avec plus de fonctionnalités.

- **Perspectives d'Amélioration :**
  1.  **Passage à une Base de Données Vectorielle :** Migrer l'indexation vers une solution spécialisée comme **FAISS** (pour la performance) ou **ChromaDB/Pinecone** (pour la facilité de gestion) afin de garantir une scalabilité et des temps de réponse rapides.
  2.  **Amélioration de l'Interface :** Développer une interface React plus professionnelle avec des fonctionnalités avancées : historique de conversation persistant, suggestions de questions (FAQ intelligente), et possibilité de donner un feedback (pouce haut/bas) sur les réponses.
  3.  **Déploiement Cloud :** Pour une disponibilité continue, le projet pourrait être déployé sur le cloud. Le backend **FastAPI** (plus performant que Flask pour les applications asynchrones) pourrait être hébergé sur un service comme Render ou Heroku, et le frontend React sur **Vercel**.
  4.  **Ajout de Documents :** Intégrer un pipeline automatisé pour mettre à jour la base de connaissances dès que de nouveaux documents officiels sont publiés par la FSO.

### **9. Conclusion**

Ce projet a permis de démontrer avec succès l'immense potentiel de l'architecture RAG pour résoudre des problématiques concrètes dans le secteur de l'enseignement supérieur. En développant un pipeline NLP robuste et en le couplant à un grand modèle de langage, nous avons créé un assistant académique capable de fournir des informations fiables et précises aux étudiants de la FSO, directement à partir des sources officielles.

Le chatbot RAG ne se contente pas de répondre à des questions ; il centralise la connaissance, réduit la charge de travail du personnel administratif et améliore l'autonomie des étudiants. Les résultats de l'évaluation confirment la haute pertinence des réponses et la viabilité de la solution.

Ce projet constitue une base solide pour le développement futur d'un assistant académique officiel, plus intelligent, plus scalable et intégré de manière transparente dans l'écosystème numérique de la Faculté des Sciences d'Oujda et, potentiellement, de toute l'université.

### **10. Références**

- **Modèles OpenAI :**

  - OpenAI. (2024). _Text embedding models Documentation_. [https://platform.openai.com/docs/guides/embeddings](https://platform.openai.com/docs/guides/embeddings)
  - OpenAI. (2024). _GPT-4o Mini Model Documentation_. [https://platform.openai.com/docs/models/gpt-4o-mini](https://platform.openai.com/docs/models/gpt-4o-mini)

- **Concepts NLP et RAG :**

  - Lewis, P., et al. (2020). _Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks_. arXiv:2005.11401.
  - Jurafsky, D., & Martin, J. H. (2023). _Speech and Language Processing_. 3rd Edition.
  - Manning, C. D., Raghavan, P., & Schütze, H. (2008). _Introduction to Information Retrieval_. Cambridge University Press.

- **Outils et Bibliothèques :**
  - Streamlit Documentation. [https://docs.streamlit.io/](https://docs.streamlit.io/)
  - React Documentation. [https://react.dev/](https://react.dev/)
  - Flask Documentation. [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
  - FastAPI Documentation. [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
