import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
from rag_assistant.ingest import DocumentIngestor
from rag_assistant.vector_store import VectorStore
from rag_assistant.rag_engine import RAGEngine

def main():
    print("="*60)
    print("🧪 RUNNING SECTION 2 RAG QUESTION & ANSWER TEST SUITE")
    print("="*60)

    workspace_root = Path(__file__).parent.resolve()
    db_path = workspace_root / "vector_db.json"

    vs = VectorStore(str(db_path))
    if not db_path.exists():
        ingestor = DocumentIngestor(str(workspace_root))
        chunks = ingestor.ingest_all()
        vs.build_index(chunks)
    else:
        vs.load_index()

    engine = RAGEngine(vs)

    # Section 2A: 10 Questions Answered from Document
    section_2a_questions = [
        "What is the objective of the HelpDesk Ticket Management application?",
        "Which technologies were used to develop the project?",
        "Which database tables are used in the application?",
        "What validations are implemented while creating a ticket?",
        "What are the different ticket statuses supported by the application?",
        "How does the MVC layer communicate with the Web API?",
        "What REST API endpoints exist in the Web API layer?",
        "How are unit tests implemented and mocked using Moq?",
        "How to run the Web API and MVC applications locally?",
        "What business rules govern editing ticket priority and status?"
    ]

    # Section 2B: 5 Questions NOT Available in Project Documentation
    section_2b_questions = [
        "Who is the CEO of Microsoft?",
        "What is Artificial Intelligence?",
        "What is the capital of Australia?",
        "Explain Machine Learning.",
        "What is Cloud Computing?"
    ]

    section_2a_results = []
    section_2b_results = []

    print("\n--- SECTION 2A: Questions Answered from Document ---\n")
    for idx, q in enumerate(section_2a_questions, 1):
        res = engine.query(q)
        print(f"[2A.{idx}] Question: {q}")
        print(f"     Citations: {', '.join(res['citations']) if res['citations'] else 'None'}")
        print(f"     Answer Snippet: {res['answer'][:120]}...\n")
        section_2a_results.append({
            "id": f"2A.{idx}",
            "question": q,
            "answer": res["answer"],
            "citations": res["citations"]
        })

    print("\n--- SECTION 2B: Questions NOT Available in Document ---\n")
    for idx, q in enumerate(section_2b_questions, 1):
        res = engine.query(q)
        print(f"[2B.{idx}] Question: {q}")
        print(f"     Answer: {res['answer']}\n")
        section_2b_results.append({
            "id": f"2B.{idx}",
            "question": q,
            "answer": res["answer"],
            "citations": res["citations"]
        })

    output_data = {
        "student_name": "SHRI RAM PRINCE MISHRA",
        "registration_number": "IN26012152",
        "github_url": "https://github.com/srpm2005/HelpDeskManagement_IN26012152",
        "section_2a_document_qa": section_2a_results,
        "section_2b_nondocument_qa": section_2b_results
    }

    out_file = workspace_root / "Section2_Questions_And_Answers.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully executed all Q&A tests! Results saved to {out_file}")

if __name__ == "__main__":
    main()
