import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

# Set up some constants for clarity
PERSIST_DIRECTORY = "./chroma_db"
PDF_PATH = "document.pdf"

# Initialize the Flask app
app = Flask(__name__)
qa_chain = None

# A simple function to set up the LLM and the RetrievalQA chain
def setup_llm_and_chain():
    global qa_chain
    print("Setting up LLM and RetrievalQA chain...")

    # NEW: A more aggressive prompt template
    prompt_template = """
You are a helpful assistant.
Answer the question based ONLY on the following context.
Do not use any prior knowledge.

If the answer is not contained within the provided context,
say "I cannot provide an answer based on the information I was given."

Context: {context}

Question: {question}

Answer:"""
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    llm = ChatGroq(model="llama3-8b-8192", groq_api_key=os.environ.get("GROQ_API_KEY"))

    if not os.path.exists(PERSIST_DIRECTORY):
        print("Creating new vector store from documents...")
        loader = PyPDFLoader(PDF_PATH)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vectordb = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=PERSIST_DIRECTORY
        )
    else:
        print("Loading existing vector store...")
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vectordb = Chroma(
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=embeddings
        )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectordb.as_retriever(),
        chain_type_kwargs={"prompt": PROMPT},
        # NEW: Return the source documents for debugging
        return_source_documents=True
    )
    print("LLM and chain setup complete.")

@app.route("/")
def home():
    global qa_chain
    if qa_chain is None:
        setup_llm_and_chain()
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    user_prompt = data.get("prompt")
    if not user_prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        if qa_chain is None:
            setup_llm_and_chain()
        
        # We now use invoke and handle the returned source documents
        result = qa_chain.invoke({"query": user_prompt})
        
        # Extract the answer and a string representing the sources
        answer = result["result"]
        source_docs = result.get("source_documents", [])
        
        # This will help you debug and see what information the model was given
        print("Sources:", source_docs)
        
        return jsonify({"answer": answer})
    except Exception as e:
        print(f"ERROR in app: {e}")
        return jsonify({"error": str(e)}), 500

    if _name_ == "_main_":
     setup_llm_and_chain()
     app.run()