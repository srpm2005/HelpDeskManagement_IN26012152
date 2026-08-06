import streamlit as st
import json
from pathlib import Path
from rag_assistant.ingest import DocumentIngestor
from rag_assistant.vector_store import VectorStore
from rag_assistant.rag_engine import RAGEngine

# Page Configuration
st.set_page_config(
    page_title="HelpDesk RAG Knowledge Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Premium Dark/Modern Look
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .citation-badge {
        background-color: #EFF6FF;
        color: #1D4ED8;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid #BFDBFE;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Workspace & RAG Engine
WORKSPACE_ROOT = Path(__file__).parent.resolve()
DB_PATH = WORKSPACE_ROOT / "vector_db.json"

@st.cache_resource
def get_rag_engine():
    vs = VectorStore(str(DB_PATH))
    if not DB_PATH.exists():
        ingestor = DocumentIngestor(str(WORKSPACE_ROOT))
        chunks = ingestor.ingest_all()
        vs.build_index(chunks)
    else:
        vs.load_index()
    return RAGEngine(vs), vs

engine, vector_store = get_rag_engine()

# Sidebar Layout
with st.sidebar:
    st.image("https://img.icons8.com/isometric-folders/100/chatbot.png", width=70)
    st.title("Knowledge Base Control")
    
    st.subheader("📊 System Metrics")
    num_chunks = len(vector_store.chunks)
    unique_files = len(set(c["source_file"] for c in vector_store.chunks))
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Files Indexed", value=unique_files)
    with col2:
        st.metric(label="RAG Chunks", value=num_chunks)
        
    st.divider()
    
    st.subheader("🛠️ Indexing Actions")
    if st.button("🔄 Re-index Project Docs"):
        with st.spinner("Re-ingesting and indexing project documentation..."):
            ingestor = DocumentIngestor(str(WORKSPACE_ROOT))
            chunks = ingestor.ingest_all()
            vector_store.build_index(chunks)
            st.cache_resource.clear()
            st.success("Knowledge Base successfully re-indexed!")
            st.rerun()

    st.divider()
    st.markdown("### 🏢 Tech Stack")
    st.markdown("- **API**: ASP.NET Core 10.0 Web API\n- **DB**: SQL Server / EF Core\n- **UI**: ASP.NET Core MVC\n- **Tests**: xUnit & Moq (13 Tests)")

# Main Content Area
st.markdown('<div class="main-header">🤖 HelpDesk AI Knowledge Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Retrieval-Augmented Generation (RAG) Onboarding Assistant for New Developers</div>', unsafe_allow_html=True)

# Preset Developer Queries Gallery
st.markdown("### 💡 Quick Developer Questions")
preset_cols = st.columns(3)

selected_preset = None
with preset_cols[0]:
    if st.button("🌐 REST API Endpoints"):
        selected_preset = "What REST API endpoints exist and what are their HTTP methods?"
    if st.button("🏗️ Project Architecture"):
        selected_preset = "Explain the project architecture and multi-tier structure."

with preset_cols[1]:
    if st.button("🔄 MVC to Web API Service"):
        selected_preset = "How does HelpDesk.Mvc consume the Web API?"
    if st.button("🧪 Unit Tests & Moq"):
        selected_preset = "How are unit tests set up with Moq and xUnit?"

with preset_cols[2]:
    if st.button("🚀 Run Applications Locally"):
        selected_preset = "How to run the Web API and MVC applications locally?"
    if st.button("📋 Status Filtering Logic"):
        selected_preset = "How is ticket status filtering implemented?"

# User Input Box
query_input = st.text_input(
    "Ask any question about the HelpDesk Ticket Management codebase:",
    value=selected_preset if selected_preset else "",
    placeholder="e.g. How does TicketController handle ticket creation?"
)

if query_input:
    with st.spinner("🔍 Querying Vector Database & Synthesizing RAG Answer..."):
        response = engine.query(query_input)
        
    st.markdown("---")
    st.markdown("### 🎯 RAG Assistant Answer")
    st.markdown(response["answer"])
    
    st.markdown("#### 🔖 Source Citations & Line Provenance")
    citation_html = " &nbsp; ".join([
        f'<span class="citation-badge">📄 {c}</span>'
        for c in response["citations"]
    ])
    st.markdown(citation_html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🔍 Inspect Retrieved Context Snippets & Similarity Scores"):
        for idx, chunk in enumerate(response["retrieved_chunks"], 1):
            st.markdown(f"**[{idx}] {chunk['title']}** (Relevance Score: `{chunk['score']:.4f}`)")
            st.markdown(f"Lines `{chunk['start_line']}-{chunk['end_line']}` in `{chunk['source_file']}`")
            st.code(chunk["content"], language="markdown" if "md" in chunk["source_file"] else "csharp")
            st.divider()
