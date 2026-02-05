# Examen-Chatbot-Intelligent


## Project Description

Traditional generative chatbots may produce hallucinated or inconsistent responses, which is problematic in an e-commerce environment where correctness and reliability are essential.  
To overcome these limitations, this project adopts a RAG-based approach, where relevant documents are retrieved and injected as context before generating an answer.

Rather than relying solely on a language model, the chatbot grounds its responses in real FAQ data stored in a vector database.

---

## System Architecture and Workflow

The system follows a clear and deterministic processing pipeline:

- A user sends a question through a REST API
- The question is converted into a vector embedding
- A similarity search is performed on a vector database
- The top 5 most relevant FAQ documents are retrieved
- These documents are provided as contextual input to the language model
- The language model generates a response strictly based on this context
- The final answer is returned to the user

This workflow significantly reduces hallucinations and improves response relevance.

---

## Technology Stack

The application is built using the following technologies:

- **FastAPI** – REST API framework
- **ChromaDB** – Vector database for FAQ storage and retrieval
- **SentenceTransformers** – Semantic embedding generation
- **Gemini API** – Large Language Model for response generation
- **Docker** – Containerized deployment

---

## Functionalities

The main functionalities implemented in this project include:

- Semantic search over e-commerce FAQ data
- Context-aware response generation using RAG
- RESTful API easily consumable by external clients
- Docker-based deployment for consistent environments

---

## Installation and Configuration

To set up the project, follow these steps:

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install all required dependencies using `requirements.txt`.

---

## Gemini API Key Configuration (MANDATORY)

You must **use your own Gemini API key** to run this project.

Steps to follow:

- Open the `.env` file
- Generate a Gemini API key from your Google account
- Insert **your personal Gemini API key** into the `.env` file
- Make sure the key is valid and active

---

## Dataset Preparation

The FAQ dataset must be placed in the following directory before running the application:


This dataset is indexed into the vector database during application initialization.

---

## Running the Application


Once running, the application is accessible through:

- **API Base URL**: http://localhost:8000  
- **Swagger Documentation**: http://localhost:8000/docs  

---

## API Endpoints

- **GET /**  
  Health check endpoint to verify that the API is running correctly.

- **POST /search**  
  Performs semantic search and returns the most relevant FAQ documents.

- **POST /chat**  
  Returns a complete response including retrieved documents and the generated answer.

---

## Docker Deployment

Before deploying with Docker, ensure that the `.env` file contains **only the provided Gemini API key**.

To build and run the application using Docker:


---


