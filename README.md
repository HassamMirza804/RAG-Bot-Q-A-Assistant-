# 🛡️ RAG-Powered AI Assistant for PDFs

This is a powerful and efficient Retrieval-Augmented Generation (RAG) application that acts as an AI assistant for your documents. It allows you to get instant, accurate answers from any PDF file you provide by building a private knowledge base.

---

### 🎥 Demo Video

Here is a quick demo of the application in action.



https://github.com/user-attachments/assets/4fb82bca-3a82-432d-a3b9-148107f0b69d


### ✨ Features

* **PDF-based Q&A**:  Get answers to specific questions directly from a PDF document.
* **Context-Aware Answers**: Utilizes RAG to ensure the AI's responses are grounded in the provided context, preventing hallucination.
* **Lightning-Fast Performance**: The application provides near-instantaneous responses.
* **Flexible Knowledge Base**: Easily switch between different PDF documents to create new, specialized knowledge bases.
* **Flexible Knowledge Base**: Configured for easy deployment on platforms like Render.
  
---

### ⚙️ Tech Stack

* **Python**: The core programming language.
* **Flask**: The web framework for the backend.
* **LangChain**: The framework that orchestrates the RAG pipeline.
* **Groq**: The fast and powerful Large Language Model (LLM) backend (Llama3-8B).
* **Ollama Embeddings**: Used to create text embeddings for document processing.
* **ChromaDB**: The vector store for storing and retrieving document embeddings.

---

### 🚀 Getting Started

To run this application locally, follow these steps:

1.  **Clone the repository**:
    ```sh
    git clone https://github.com/HassamMirza804/RAG-Powered-AI-Assistant-for-PDFs.git
    cd RAG-Powered-AI-Assistant-for-PDFs
    ```

2.  **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3.  **Prepare the PDF File**:
    ```sh
    Place the PDF file you want to use inside the project's root directory and rename it to document.pdf
    ```

4.  **Run the Application**:
    ```sh
    python app.py
    flask run
    ```

    The application will be accessible at `http://localhost:5000`.
