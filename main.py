import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
import pytesseract
from pdf2image import convert_from_path
load_dotenv()

def load_pdf_with_ocr(file_path):
    """Load PDF with OCR fallback for image-based PDFs"""
    # Try regular PDF loading first
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # Check if any documents have content
    has_content = any(doc.page_content.strip() for doc in docs)

    if has_content:
        print("✅ Loaded PDF with text extraction")
        return docs
    else:
        print("📷 PDF appears to be image-based, using OCR...")
        # Convert PDF to images and extract text with OCR
        images = convert_from_path(file_path)
        ocr_docs = []

        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image)
            if text.strip():  # Only add if there's actual text
                doc = Document(
                    page_content=text,
                    metadata={"source": file_path, "page": i}
                )
                ocr_docs.append(doc)

        print(f"✅ Extracted text from {len(ocr_docs)} pages using OCR")
        return ocr_docs

file_path = "/home/deepak-walia/Downloads/Deepak walia Resume .pdf"
docs = load_pdf_with_ocr(file_path)

print(f"Loaded {len(docs)} pages")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)
print("Splitting documents into chunks...",splitter)
documents = splitter.split_documents(docs)
print(f"Created {len(documents)} chunks")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Embeddings loaded",embeddings)

DB_PATH = "faiss_index"

if os.path.exists(DB_PATH):
    print("Loading FAISS...")
    vectorstore = FAISS.load_local(
        DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
else:
    print("⚡ Creating FAISS...")
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(DB_PATH)

print("✅ Vector DB ready")
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)

if not os.getenv("GROQ_API_KEY"):
    raise ValueError("❌ Add GROQ_API_KEY in .env")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.9,
    max_tokens=1000,
)

print("LLM connected",llm)

prompt = PromptTemplate(
    input_variables=["context", "input"],
    template="""
You are a helpful AI assistant.

Use ONLY the provided context to answer.
If not found, say "I don't know".

Context:
{context}

Question:
{input}

Give clear answer.
"""
)

template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

qa_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print("\n💬 Ask questions (type 'exit')\n")

while True:
    query = input("👉 You: ")

    if query.lower() == "exit":
        print("👋 Bye bro!")
        break

    docs = retriever.invoke(query)
    print("\n🔍 Retrieved Chunks:")
    for i, d in enumerate(docs):
        print(f"\n--- Chunk {i+1} ---")
        print(d.page_content[:200], "...")

    response = qa_chain.invoke(query)

    print("\n🤖 Answer:", response)
    print("\n" + "="*60)