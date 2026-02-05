Ce projet est un chatbot basé sur l’architecture RAG pour répondre aux FAQ e-commerce. Il combine recherche sémantique et génération pour fournir des réponses précises.

Stockage et recherche : ChromaDB (FAQ).

Embeddings : SentenceTransformers.

LLM : Gemini (API).

API : FastAPI.

Le client envoie une requête.

La requête est convertie en vecteur.

On récupère les 5 documents FAQ les plus pertinents.

Gemini génère une réponse basée sur ces documents.

La réponse est renvoyée.

Tech Stack

FastAPI (API)

ChromaDB (Base vecteurs)

SentenceTransformers (Embeddings)

Gemini API (LLM)

Docker (Déploiement)

Fonctionnalités

Recherche sémantique sur FAQ.

Réponses basées sur le contexte récupéré.

API REST exploitable facilement.

Déploiement Docker.

Installation

Clonez le repo.

Créez un environnement virtuel.

Installez les dépendances avec requirements.txt.

Ajoutez la clé API Gemini dans .env.

Placez le dataset dans data/.

Lancer le Chatbot
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


API : http://localhost:8000

Docs : http://localhost:8000/docs

Endpoints

/ : Health check.

/search (POST) : Renvoie les documents pertinents.

/chat (POST) : Renvoie une réponse complète avec documents et réponse générée.

Déploiement Docker

Configurez .env avec la clé API.

docker-compose up --build
