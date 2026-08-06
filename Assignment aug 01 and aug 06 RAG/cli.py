import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
from rag_assistant.ingest import DocumentIngestor
from rag_assistant.vector_store import VectorStore
from rag_assistant.rag_engine import RAGEngine

def main():
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

    # Check for --json flag
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        query = " ".join(sys.argv[2:])
        res = engine.query(query)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(f"\n❓ Question: {query}\n" + "="*50)
        res = engine.query(query)
        print(res["answer"])
        print("\n🔍 Retrieved Context Snippets:")
        for idx, chunk in enumerate(res["retrieved_chunks"], 1):
            print(f"  [{idx}] {chunk['title']} (Score: {chunk['score']})")
        return

    print("🤖 HelpDesk Project RAG Knowledge Assistant CLI")
    print("Type your questions below (or type 'exit' to quit):\n")

    while True:
        try:
            user_input = input("\n💬 Developer Question: ").strip()
            if not user_input or user_input.lower() in ["exit", "quit", "q"]:
                print("Goodbye!")
                break

            print("\n🔍 Searching Knowledge Base...")
            res = engine.query(user_input)
            print("\n" + res["answer"])
            print("\n📌 Sources:")
            for c in res["citations"]:
                print(f"  - {c}")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
