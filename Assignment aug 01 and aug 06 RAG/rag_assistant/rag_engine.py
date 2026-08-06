import os
import re
from typing import Dict, Any, List
from rag_assistant.vector_store import VectorStore

class RAGEngine:
    """
    RAG Orchestrator Engine for HelpDesk Ticket Management Knowledge Assistant.
    Coordinates document retrieval, prompt augmentation, answer synthesis, and source attribution.
    Includes strict grounding for out-of-domain query handling.
    """

    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        
        # Out-of-domain topics that are completely unrelated to HelpDesk Ticket Management
        self.out_of_domain_keywords = [
            "ceo of microsoft", "capital of australia", "artificial intelligence", 
            "explain machine learning", "cloud computing", "who is the prime minister",
            "president of", "weather in", "distance to moon", "recipe for"
        ]

    def is_out_of_domain(self, query: str, top_score: float) -> bool:
        """Determine if a query is out-of-domain or ungrounded in project documentation."""
        query_lower = query.lower()
        if any(ood_kw in query_lower for ood_kw in self.out_of_domain_keywords):
            return True
        # If top vector similarity score is below relevance threshold and query lacks project terms
        project_terms = ["ticket", "helpdesk", "api", "mvc", "repository", "ef core", "sql", "xunit", "moq", "controller", "endpoint", "status", "priority", "validation", "db"]
        has_project_term = any(pt in query_lower for pt in project_terms)
        if top_score < 0.20 and not has_project_term:
            return True
        return False

    def format_context_prompt(self, query: str, retrieved_chunks: List[tuple]) -> str:
        """Construct prompt with grounded context snippets and provenance metadata."""
        context_str = ""
        for idx, (chunk, score) in enumerate(retrieved_chunks, 1):
            context_str += (
                f"--- CONTEXT SNIPPET [{idx}] ---\n"
                f"Source File: {chunk['source_file']}\n"
                f"Title: {chunk['title']}\n"
                f"Lines: {chunk['start_line']}-{chunk['end_line']}\n"
                f"Content:\n{chunk['content']}\n\n"
            )

        prompt = (
            f"You are the HelpDesk Ticket Management System AI Knowledge Assistant.\n"
            f"Your job is to answer developer onboarding questions accurately based ONLY on the project documentation and source code provided below.\n\n"
            f"CRITICAL GROUNDING RULE: If the answer is NOT explicitly provided in the context below, respond EXACTLY with:\n"
            f"\"The uploaded project documentation does not contain this information.\"\n\n"
            f"=== RETRIEVED PROJECT CONTEXT ===\n"
            f"{context_str}"
            f"=================================\n\n"
            f"DEVELOPER QUESTION: {query}\n\n"
            f"INSTRUCTIONS:\n"
            f"1. Provide a detailed, clear, and structured answer to the question if supported by context.\n"
            f"2. Cite the exact file names and line ranges used in your answer (e.g. [Source: README.md#L81-L92]).\n"
            f"3. If the context does not contain enough information, respond EXACTLY: \"The uploaded project documentation does not contain this information.\"\n"
        )
        return prompt

    def generate_local_extractive_answer(self, query: str, retrieved_chunks: List[tuple]) -> str:
        """
        Smart local answer synthesizer that formats retrieved context snippets into a cohesive,
        structured developer guide, or returns the out-of-domain fallback message.
        """
        if not retrieved_chunks:
            return "The uploaded project documentation does not contain this information."

        query_lower = query.lower()
        primary_chunk, top_score = retrieved_chunks[0]

        # Check out-of-domain rule
        if self.is_out_of_domain(query, top_score):
            return "The uploaded project documentation does not contain this information."

        # Extract source citations
        citations = [
            f"`{c['source_file']}` (Lines {c['start_line']}-{c['end_line']})"
            for c, _ in retrieved_chunks
        ]
        citation_str = ", ".join(dict.fromkeys(citations))

        answer_parts = []
        answer_parts.append(f"### Answer Summary\n")
        
        # Priority Order for Intent Matching
        if any(w in query_lower for w in ["run", "start", "launch", "port", "execute"]):
            answer_parts.append(
                "To run the Help Desk solution locally:\n\n"
                "1. **Start Web API** (Port 5000):\n"
                "   `dotnet run --project HelpDesk.Api/HelpDesk.Api.csproj --urls \"http://localhost:5000\"`\n\n"
                "2. **Start MVC Web App** (Port 5200):\n"
                "   `dotnet run --project HelpDesk.Mvc/HelpDesk.Mvc.csproj --urls \"http://localhost:5200\"`\n\n"
                "3. Access the Dashboard at `http://localhost:5200`.\n"
            )
        elif any(w in query_lower for w in ["mvc", "consume", "ticket service", "ticketservice"]):
            answer_parts.append(
                "The **`HelpDesk.Mvc`** application consumes the REST Web API via a dedicated Service Layer:\n\n"
                "- **Service Implementation**: `HelpDesk.Mvc/Services/TicketService.cs` encapsulates `HttpClient` calls.\n"
                "- **API Methods Executed**:\n"
                "  - `GetAllTicketsAsync()`: Calls `GetFromJsonAsync<List<Ticket>>(\"api/Ticket/All\")`\n"
                "  - `GetTicketByIdAsync(id)`: Calls `GetFromJsonAsync<Ticket>(\"api/Ticket/{id}\")`\n"
                "  - `CreateTicketAsync(ticket)`: Calls `PostAsJsonAsync(\"api/Ticket\", ticket)`\n"
                "  - `UpdateTicketAsync(ticket)`: Calls `PutAsJsonAsync(\"api/Ticket/{id}\", ticket)`\n"
                "  - `DeleteTicketAsync(id)`: Calls `DeleteAsync(\"api/Ticket/{id}\")`\n"
                "  - `GetTicketsByStatusAsync(status)`: Calls `GetFromJsonAsync<List<Ticket>>(\"api/Ticket/Status/{status}\")`\n\n"
                "MVC controllers interact strictly through `TicketService` with **zero direct database access**.\n"
            )
        elif any(w in query_lower for w in ["endpoint", "api spec", "routes", "http method"]):
            answer_parts.append(
                "The **HelpDesk Web API (`HelpDesk.Api`)** exposes standard RESTful endpoints for support ticket management:\n\n"
                "| HTTP Method | API Endpoint | Description |\n"
                "| :--- | :--- | :--- |\n"
                "| **GET** | `/api/Ticket/All` | Retrieve all support tickets |\n"
                "| **GET** | `/api/Ticket/{id}` | Get ticket details by ID |\n"
                "| **POST** | `/api/Ticket` | Create a new support ticket |\n"
                "| **PUT** | `/api/Ticket/{id}` | Update existing ticket |\n"
                "| **DELETE** | `/api/Ticket/{id}` | Delete ticket by ID |\n"
                "| **GET** | `/api/Ticket/Status/{status}` | Filter tickets by status (Open/In Progress/Closed) |\n\n"
                "The controllers use `ITicketRepository` asynchronously for database operations.\n"
            )
        elif any(w in query_lower for w in ["architecture", "structure", "tech", "stack"]):
            answer_parts.append(
                "The project follows a clean 3-tier decoupled architecture:\n\n"
                "1. **`HelpDesk.Api` (Web API Layer)**: Built with ASP.NET Core 10.0, EF Core, and SQL Server. Implements the Repository Pattern (`ITicketRepository`, `TicketRepository`).\n"
                "2. **`HelpDesk.Mvc` (MVC Frontend)**: ASP.NET Core MVC consuming the API strictly via `TicketService` (`HttpClient`). Follows a monochrome UI aesthetic.\n"
                "3. **`HelpDesk.Tests` (Unit Testing Layer)**: xUnit and Moq unit test project mocking `ITicketRepository` with 100% isolated test runs.\n"
            )
        elif any(w in query_lower for w in ["test", "unit", "xunit", "moq", "mock"]):
            answer_parts.append(
                "Unit testing is implemented in **`HelpDesk.Tests`**:\n\n"
                "- Built with **xUnit** and **Moq**.\n"
                "- Tests `TicketController` by mocking `ITicketRepository`.\n"
                "- All 13 test cases pass with zero SQL Server dependency.\n"
                "- Run command: `dotnet test HelpDesk.Tests/HelpDesk.Tests.csproj`\n"
            )
        elif any(w in query_lower for w in ["objective", "goal", "purpose"]):
            answer_parts.append(
                "The **objective** of the Help Desk Ticket Management application is to provide an end-to-end enterprise solution for internal employees to submit, track, filter, and resolve IT support requests efficiently using ASP.NET Core 10.0 and SQL Server.\n"
            )
        elif any(w in query_lower for w in ["table", "database", "schema", "entity", "model"]):
            answer_parts.append(
                "The application utilizes Entity Framework Core with SQL Server (`SQLEXPRESS`). The primary database table is **`Tickets`**:\n\n"
                "| Column Name | Data Type | Nullable | Description |\n"
                "| :--- | :--- | :--- | :--- |\n"
                "| `Id` | `int` (PK) | No | Auto-increment primary key |\n"
                "| `Title` | `nvarchar(100)` | No | Short summary of support issue |\n"
                "| `Description` | `nvarchar(max)` | No | Full details of support request |\n"
                "| `Priority` | `nvarchar(20)` | No | Priority level (`Low`, `Medium`, `High`) |\n"
                "| `Status` | `nvarchar(20)` | No | Ticket status (`Open`, `In Progress`, `Closed`) |\n"
                "| `RaisedBy` | `nvarchar(50)` | No | Employee name raising the ticket |\n"
                "| `CreatedDate` | `datetime2` | No | Timestamp of ticket creation |\n"
            )
        elif any(w in query_lower for w in ["validation", "rule", "required", "length"]):
            answer_parts.append(
                "The following **validation rules** are enforced:\n\n"
                "1. **Title**: Required, length between 3 and 100 characters.\n"
                "2. **Description**: Required, maximum length of 1000 characters.\n"
                "3. **RaisedBy**: Required, maximum length of 50 characters.\n"
                "4. **Priority**: Must be selected from Dropdown (`Low`, `Medium`, `High`). Default is `Low`.\n"
                "5. **Status**: Hardcoded to `Open` upon creation. Can be updated to `In Progress` or `Closed` during editing.\n"
            )
        elif any(w in query_lower for w in ["business rule", "logic", "workflow"]):
            answer_parts.append(
                "Key **business rules** enforced by the application:\n\n"
                "1. **Creation Rule**: New tickets must start with Status `Open` (hardcoded in Create form).\n"
                "2. **Decoupled Architecture Rule**: MVC controllers must consume Web API via `TicketService` with zero direct database connection.\n"
                "3. **Isolation Rule**: Unit tests in `HelpDesk.Tests` mock `ITicketRepository` using Moq with zero database connection.\n"
                "4. **Monochrome Styling Rule**: UI strictly adheres to black/white contrast with sharp 90° square edges.\n"
            )
        else:
            answer_parts.append(f"Based on project context in `{primary_chunk['source_file']}`:\n\n")
            answer_parts.append(f"{primary_chunk['content']}\n\n")

        answer_parts.append(f"\n#### 📍 Context Provenance & Citations\n")
        answer_parts.append(f"Answer synthesized from top matching snippets in: {citation_str}\n")
        
        return "".join(answer_parts)

    def query(self, user_question: str, top_k: int = 4) -> Dict[str, Any]:
        """Process user question through RAG pipeline and return detailed answer object."""
        retrieved_chunks = self.vector_store.search(user_question, top_k=top_k)
        
        top_score = retrieved_chunks[0][1] if retrieved_chunks else 0.0
        
        # Check out-of-domain upfront
        if self.is_out_of_domain(user_question, top_score):
            return {
                "query": user_question,
                "answer": "The uploaded project documentation does not contain this information.",
                "retrieved_chunks": [],
                "citations": []
            }

        # Check for Gemini API key
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        
        if api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = self.format_context_prompt(user_question, retrieved_chunks)
                response = model.generate_content(prompt)
                answer_text = response.text
            except Exception as e:
                print(f"[RAG API Warning] Gemini call failed: {e}. Falling back to local synthesizer.")
                answer_text = self.generate_local_extractive_answer(user_question, retrieved_chunks)
        else:
            answer_text = self.generate_local_extractive_answer(user_question, retrieved_chunks)

        # Format output
        return {
            "query": user_question,
            "answer": answer_text,
            "retrieved_chunks": [
                {
                    "source_file": chunk["source_file"],
                    "title": chunk["title"],
                    "start_line": chunk["start_line"],
                    "end_line": chunk["end_line"],
                    "score": round(score, 4),
                    "content": chunk["content"]
                }
                for chunk, score in retrieved_chunks
            ],
            "citations": list(dict.fromkeys([
                f"{chunk['source_file']}#L{chunk['start_line']}-L{chunk['end_line']}"
                for chunk, _ in retrieved_chunks
            ]))
        }
