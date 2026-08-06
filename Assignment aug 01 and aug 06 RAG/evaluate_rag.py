import sys
import json
import time
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
from rag_assistant.ingest import DocumentIngestor
from rag_assistant.vector_store import VectorStore
from rag_assistant.rag_engine import RAGEngine

def run_evaluation():
    print("="*60)
    print("🧪 RAG KNOWLEDGE ASSISTANT EVALUATION & BENCHMARK SUITE")
    print("="*60)

    workspace_root = Path(__file__).parent.resolve()
    db_path = workspace_root / "vector_db.json"

    # Step 1: Ingest & Indexing Verification
    start_time = time.time()
    ingestor = DocumentIngestor(str(workspace_root))
    chunks = ingestor.ingest_all()
    vs = VectorStore(str(db_path))
    vs.build_index(chunks)
    index_time = time.time() - start_time
    print(f"✅ Ingestion & Indexing completed in {index_time:.2f} seconds.")

    engine = RAGEngine(vs)

    # Step 2: Define Benchmark Evaluation Test Suite
    test_cases = [
        {
            "id": "TC-01",
            "category": "API Specs",
            "query": "What REST API endpoints exist and what are their HTTP methods?",
            "expected_sources": ["README.md", "HelpDesk_Assignment_Report.md", "TicketController.cs"],
            "expected_keywords": ["/api/Ticket", "GET", "POST", "PUT", "DELETE"]
        },
        {
            "id": "TC-02",
            "category": "Architecture",
            "query": "Explain the project architecture and multi-tier structure.",
            "expected_sources": ["HelpDesk_Assignment_Report.md", "README.md"],
            "expected_keywords": ["HelpDesk.Api", "HelpDesk.Mvc", "HelpDesk.Tests", "Repository"]
        },
        {
            "id": "TC-03",
            "category": "MVC Integration",
            "query": "How does HelpDesk.Mvc consume the Web API?",
            "expected_sources": ["TicketService.cs", "README.md", "HelpDesk.Mvc"],
            "expected_keywords": ["TicketService", "HttpClient", "GetFromJsonAsync", "PostAsJsonAsync"]
        },
        {
            "id": "TC-04",
            "category": "Unit Testing",
            "query": "How are unit tests set up with Moq and xUnit?",
            "expected_sources": ["TicketControllerTests.cs", "README.md"],
            "expected_keywords": ["Mock", "xUnit", "Moq", "13"]
        },
        {
            "id": "TC-05",
            "category": "Deployment",
            "query": "How to run the Web API and MVC applications locally?",
            "expected_sources": ["README.md", "HelpDesk_Assignment_Report.md", "RAG_KNOWLEDGE_ASSISTANT_REPORT.md"],
            "expected_keywords": ["dotnet run", "5000", "5200"]
        }
    ]

    results = []
    passed_count = 0

    print("\nExecuting Test Queries:\n" + "-"*60)

    for tc in test_cases:
        t0 = time.time()
        res = engine.query(tc["query"], top_k=3)
        query_latency = (time.time() - t0) * 1000

        # Check retrieval precision
        retrieved_files = [c["source_file"] for c in res["retrieved_chunks"]]
        top_retrieved_file = retrieved_files[0] if retrieved_files else ""
        
        source_matched = any(
            any(exp in f for exp in tc["expected_sources"])
            for f in retrieved_files
        )
        
        # Check keyword ground truth hit in answer
        answer_text = res["answer"]
        keyword_hits = sum(1 for kw in tc["expected_keywords"] if kw.lower() in answer_text.lower())
        keyword_precision = keyword_hits / len(tc["expected_keywords"]) if tc["expected_keywords"] else 1.0

        is_passed = source_matched and keyword_precision >= 0.5
        if is_passed:
            passed_count += 1

        eval_record = {
            "test_id": tc["id"],
            "category": tc["category"],
            "query": tc["query"],
            "status": "PASS" if is_passed else "FAIL",
            "latency_ms": round(query_latency, 2),
            "top_source": top_retrieved_file,
            "source_matched": source_matched,
            "keyword_precision": round(keyword_precision, 2),
            "top_score": res["retrieved_chunks"][0]["score"] if res["retrieved_chunks"] else 0.0,
            "citations": res["citations"]
        }
        results.append(eval_record)

        status_str = "✅ PASS" if is_passed else "❌ FAIL"
        print(f"[{tc['id']}] {tc['category']}: {tc['query'][:40]}... -> {status_str} ({query_latency:.1f} ms)")
        print(f"      Top Source: {top_retrieved_file} | Score: {eval_record['top_score']:.4f}")

    print("\n" + "="*60)
    print(f"📊 EVALUATION SUMMARY: {passed_count}/{len(test_cases)} Passed ({(passed_count/len(test_cases))*100:.1f}%)")
    print("="*60)

    output_path = workspace_root / "rag_evaluation_results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"Saved detailed evaluation benchmark report to {output_path}")

if __name__ == "__main__":
    run_evaluation()
