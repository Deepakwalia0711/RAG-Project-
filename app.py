import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="🚀 AI Document Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# SIDEBAR
# -------------------------------
with st.sidebar:
    st.markdown("## 🎯 About")
    st.markdown("**AI Document Assistant** helps you chat with your PDF documents using advanced AI technology.")

    st.markdown("### ✨ Features")
    st.markdown("• 📄 Multi-PDF support")
    st.markdown("• 🔍 OCR for scanned documents")
    st.markdown("• 🧠 AI-powered answers")
    st.markdown("• 💬 Contextual conversations")

    st.markdown("### 🛠️ Tech Stack")
    st.markdown("• **AI Model:** Groq Llama-3.3-70B")
    st.markdown("• **Embeddings:** Sentence Transformers")
    st.markdown("• **Vector DB:** FAISS")
    st.markdown("• **OCR:** Tesseract")

    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit & LangChain")

    # Clear chat button
    if st.button("🗑️ Clear Chat", type="secondary"):
        st.session_state.messages = []
        st.rerun()

# -------------------------------
# CUSTOM CSS STYLING
# -------------------------------
st.markdown("""
<style>
    /* Main background with animated gradient */
    .main {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #f5576c, #4ecdc4);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        color: white;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Title styling with glow effect */
    .title {
        font-size: 3.5rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #ffeaa7, #dda0dd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.5);
        animation: titleGlow 2s ease-in-out infinite alternate;
    }

    @keyframes titleGlow {
        from { text-shadow: 0 0 30px rgba(255, 255, 255, 0.5); }
        to { text-shadow: 0 0 40px rgba(255, 255, 255, 0.8), 0 0 60px rgba(255, 107, 107, 0.4); }
    }

    /* Subtitle with typing effect */
    .subtitle {
        text-align: center;
        font-size: 1.3rem;
        color: #e8f4f8;
        margin-bottom: 2rem;
        font-style: italic;
        border-bottom: 2px solid rgba(255, 255, 255, 0.3);
        padding-bottom: 1rem;
    }

    /* Feature cards with hover effects */
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(15px);
        transition: all 0.3s ease;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }

    .feature-card:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
        background: rgba(255, 255, 255, 0.15);
    }

    /* Upload section with pulse animation */
    .upload-section {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        border: 2px dashed rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(15px);
        animation: pulse 3s ease-in-out infinite;
        text-align: center;
    }

    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 20px rgba(255, 255, 255, 0.1); }
        50% { box-shadow: 0 0 40px rgba(255, 255, 255, 0.3), 0 0 60px rgba(78, 205, 196, 0.2); }
    }

    /* Chat messages with slide-in animation */
    .user-message {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1.2rem;
        border-radius: 20px 20px 20px 5px;
        margin: 0.8rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        animation: slideInLeft 0.5s ease-out;
        border-left: 5px solid #4ecdc4;
    }

    .assistant-message {
        background: linear-gradient(135deg, #f093fb, #f5576c);
        color: white;
        padding: 1.2rem;
        border-radius: 20px 20px 5px 20px;
        margin: 0.8rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        animation: slideInRight 0.5s ease-out;
        border-right: 5px solid #ff6b6b;
    }

    @keyframes slideInLeft {
        from { transform: translateX(-50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }

    @keyframes slideInRight {
        from { transform: translateX(50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }

    /* Status messages with icons */
    .status-info {
        background: linear-gradient(135deg, rgba(76, 237, 196, 0.2), rgba(69, 183, 209, 0.2));
        border: 1px solid #4ecdc4;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #e8f4f8;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .status-success {
        background: linear-gradient(135deg, rgba(76, 237, 196, 0.3), rgba(150, 206, 180, 0.3));
        border: 1px solid #4ecdc4;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #e8f4f8;
        display: flex;
        align-items: center;
        gap: 10px;
        animation: successPulse 0.6s ease-out;
    }

    @keyframes successPulse {
        0% { transform: scale(0.95); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    /* Enhanced file uploader */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        border: 2px dashed rgba(255, 255, 255, 0.4);
        transition: all 0.3s ease;
    }

    .stFileUploader:hover {
        border-color: #4ecdc4;
        background: rgba(255, 255, 255, 0.15);
    }

    /* Chat input with focus effects */
    .stChatInput {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 30px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }

    .stChatInput:focus {
        border-color: #4ecdc4;
        box-shadow: 0 0 20px rgba(78, 205, 196, 0.3);
        background: rgba(255, 255, 255, 0.15);
    }

    /* Enhanced buttons */
    .stButton>button {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 0.8rem 2.5rem;
        font-weight: bold;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }

    .stButton>button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }

    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1);
        border-radius: 10px;
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Loading spinner */
    .stSpinner > div {
        border-color: #4ecdc4 transparent #4ecdc4 transparent;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER SECTION
# -------------------------------
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown('<h1 class="title">🚀 AI Document Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Multi-PDF RAG Chatbot with OCR Support</p>', unsafe_allow_html=True)

# -------------------------------
# FEATURES SHOWCASE
# -------------------------------
st.markdown("---")

# Create animated feature cards
features = [
    {"icon": "📄", "title": "Multi-PDF", "desc": "Upload multiple documents", "color": "#ff6b6b"},
    {"icon": "🔍", "title": "OCR Support", "desc": "Extract text from images", "color": "#4ecdc4"},
    {"icon": "🧠", "title": "AI Powered", "desc": "Groq LLM integration", "color": "#45b7d1"},
    {"icon": "💬", "title": "Smart Chat", "desc": "Contextual conversations", "color": "#96ceb4"}
]

cols = st.columns(4)
for i, feature in enumerate(features):
    with cols[i]:
        st.markdown(f"""
        <div class="feature-card" style="border-left: 4px solid {feature['color']};">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{feature['icon']}</div>
            <div style="font-weight: bold; font-size: 1.1rem; margin-bottom: 0.3rem;">{feature['title']}</div>
            <div style="font-size: 0.9rem; opacity: 0.8;">{feature['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# -------------------------------
# OCR FUNCTION
# -------------------------------
def extract_text_ocr(pdf_path):
    from pdf2image import convert_from_path
    import pytesseract

    images = convert_from_path(pdf_path)
    text = ""

    for img in images:
        text += pytesseract.image_to_string(img)

    return text

# -------------------------------
# LOAD PIPELINE
# -------------------------------
@st.cache_resource
def load_pipeline(file_paths):
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain_groq import ChatGroq
    from langchain_core.prompts import PromptTemplate
    from langchain_core.runnables import RunnablePassthrough
    from langchain_core.output_parsers import StrOutputParser
    from langchain.schema import Document
    from langchain_core.prompts import PromptTemplate
    from langchain_core.runnables import RunnablePassthrough

    all_docs = []

    for file_path in file_paths:
        try:
            from langchain_community.document_loaders import PyPDFLoader
            loader = PyPDFLoader(file_path)
            docs = loader.load()

            # Check if docs have actual content, not just empty pages
            has_content = any(doc.page_content.strip() for doc in docs)

            if not has_content:
                raise Exception("Empty content")

        except:
            text = extract_text_ocr(file_path)
            if text.strip():
                docs = [Document(page_content=text)]
            else:
                st.error(f"❌ Could not extract text from {file_path}")
                docs = []

        all_docs.extend(docs)

    # Split
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    documents = splitter.split_documents(all_docs)

    if len(documents) == 0:
        st.error("❌ No text extracted from PDFs")
        st.stop()

    # Embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # FAISS
    vectorstore = FAISS.from_documents(documents, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # LLM
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.1,
        max_tokens=1000,
    )

    # Prompt
    prompt = PromptTemplate(
        input_variables=["context", "input"],
        template="""
Answer based only on context.

Context:
{context}

Question:
{input}
"""
    )

    # Create RAG chain using LCEL
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    qa_chain = (
        {
            "context": retriever | format_docs,
            "input": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return qa_chain


# -------------------------------
# FILE UPLOAD SECTION
# -------------------------------
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.markdown("### � Upload Your Documents")

uploaded_files = st.file_uploader(
    "Choose PDF files",
    type="pdf",
    accept_multiple_files=True,
    help="Select one or more PDF files to analyze",
    label_visibility="collapsed"
)

if uploaded_files:
    # Show uploaded files with nice formatting
    st.markdown(f"**📊 {len(uploaded_files)} file(s) uploaded successfully!** 🎉")

    file_cols = st.columns(min(len(uploaded_files), 3))
    for i, file in enumerate(uploaded_files):
        with file_cols[i % 3]:
            # Calculate file size in KB/MB
            size_kb = file.size / 1024
            if size_kb > 1024:
                size_display = f"{size_kb/1024:.1f} MB"
            else:
                size_display = f"{size_kb:.0f} KB"

            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #4ecdc4;">
                <div style="font-weight: bold;">📄 {file.name}</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">{size_display}</div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">📤</div>
        <div style="font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5rem;">Drop your PDF files here</div>
        <div style="opacity: 0.8;">or click to browse your computer</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# PROCESSING SECTION
# -------------------------------
if uploaded_files:
    file_paths = []

    for file in uploaded_files:
        path = f"temp_{file.name}"
        with open(path, "wb") as f:
            f.write(file.read())
        file_paths.append(path)

    # Enhanced processing with progress
    progress_bar = st.progress(0)
    status_text = st.empty()

    status_text.markdown('<div class="status-info">🔄 Analyzing documents...</div>', unsafe_allow_html=True)
    progress_bar.progress(25)

    status_text.markdown('<div class="status-info">📝 Extracting text content...</div>', unsafe_allow_html=True)
    progress_bar.progress(50)

    status_text.markdown('<div class="status-info">🧠 Creating AI embeddings...</div>', unsafe_allow_html=True)
    progress_bar.progress(75)

    with st.spinner("🚀 Initializing AI assistant..."):
        qa_chain = load_pipeline(tuple(file_paths))

    progress_bar.progress(100)
    progress_bar.empty()
    status_text.empty()

    st.markdown('<div class="status-success">🎉 Documents processed successfully! Ready to chat with your AI assistant.</div>', unsafe_allow_html=True)

    # Chat memory
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chat header
    st.markdown("---")
    st.markdown("### 💬 Chat with Your Documents")
    st.markdown("Ask questions about your uploaded PDFs. The AI will search through all documents to provide accurate answers.")

    # Show chat
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-message">👤 **You:** {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message">🤖 **AI Assistant:** {msg["content"]}</div>', unsafe_allow_html=True)

    # Input
    st.markdown("---")
    query = st.chat_input("💭 Ask me anything about your documents...")

    if query:
        st.session_state.messages.append({"role": "user", "content": query})

        # Show user message
        with chat_container:
            st.markdown(f'<div class="user-message">👤 **You:** {query}</div>', unsafe_allow_html=True)

        # Show assistant thinking
        with st.spinner("🧠 Analyzing documents..."):
            answer = qa_chain.invoke(query)

        # Show assistant response
        with chat_container:
            st.markdown(f'<div class="assistant-message">🤖 **AI Assistant:** {answer}</div>', unsafe_allow_html=True)

        st.session_state.messages.append({"role": "assistant", "content": answer})

        # Auto scroll to bottom
        st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)

else:
    # Welcome message when no files uploaded
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: rgba(255,255,255,0.1); border-radius: 15px; margin: 2rem 0;">
        <h2 style="color: #4ecdc4;">🎯 Welcome to AI Document Assistant!</h2>
        <p style="color: #dfe6e9; font-size: 1.1rem;">Upload your PDF documents above to start chatting with them using advanced AI.</p>
        <p style="color: #ffeaa7;">✨ Features: Multi-PDF support, OCR for images, contextual answers</p>
    </div>
    """, unsafe_allow_html=True)