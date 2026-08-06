import os
import re
import json
from pathlib import Path
from typing import List, Dict, Any

class DocumentIngestor:
    """
    Document Ingestor & Chunker for HelpDesk Ticket Management Project.
    Parses Markdown documentation, C# source code, and configuration files
    into semantically chunked context snippets with rich provenance metadata.
    """
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root).resolve()
        
    def get_target_files(self) -> List[Path]:
        """Collect all relevant project documentation and code files."""
        target_extensions = {".md", ".cs", ".json", ".sln"}
        excluded_dirs = {".git", ".vs", "bin", "obj", "__pycache__", ".pytest_cache", "rag_assistant"}
        
        target_files = []
        for root, dirs, files in os.walk(self.workspace_root):
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in target_extensions:
                    # Ignore generated json files like vector_db.json
                    if file.endswith(".json") and file not in {"appsettings.json", "appsettings.Development.json"}:
                        continue
                    target_files.append(file_path)
                    
        return sorted(target_files)

    def chunk_markdown(self, file_path: Path, content: str) -> List[Dict[Any, Any]]:
        """Chunk markdown files by headers and logical sections."""
        rel_path = str(file_path.relative_to(self.workspace_root)).replace("\\", "/")
        lines = content.splitlines()
        chunks = []
        
        current_header = "General Documentation"
        current_lines = []
        start_line = 1
        
        for idx, line in enumerate(lines, 1):
            if line.startswith("#"):
                if current_lines:
                    chunk_text = "\n".join(current_lines).strip()
                    if len(chunk_text) > 30:
                        chunks.append({
                            "source_file": rel_path,
                            "title": f"{rel_path} - {current_header}",
                            "section": current_header,
                            "start_line": start_line,
                            "end_line": idx - 1,
                            "content": chunk_text,
                            "chunk_type": "markdown"
                        })
                    current_lines = []
                current_header = line.lstrip("#").strip()
                start_line = idx
            
            current_lines.append(line)
            
            # Sub-chunk large sections if over 40 lines
            if len(current_lines) >= 45:
                chunk_text = "\n".join(current_lines).strip()
                if len(chunk_text) > 30:
                    chunks.append({
                        "source_file": rel_path,
                        "title": f"{rel_path} - {current_header} (Part {len(chunks)+1})",
                        "section": current_header,
                        "start_line": start_line,
                        "end_line": idx,
                        "content": chunk_text,
                        "chunk_type": "markdown"
                    })
                current_lines = []
                start_line = idx + 1

        if current_lines:
            chunk_text = "\n".join(current_lines).strip()
            if len(chunk_text) > 30:
                chunks.append({
                    "source_file": rel_path,
                    "title": f"{rel_path} - {current_header}",
                    "section": current_header,
                    "start_line": start_line,
                    "end_line": len(lines),
                    "content": chunk_text,
                    "chunk_type": "markdown"
                })

        return chunks

    def chunk_csharp_code(self, file_path: Path, content: str) -> List[Dict[Any, Any]]:
        """Chunk C# source code files by methods, classes, or line blocks."""
        rel_path = str(file_path.relative_to(self.workspace_root)).replace("\\", "/")
        lines = content.splitlines()
        chunks = []
        
        # Detect primary class/interface name
        class_match = re.search(r'(class|interface|record|enum)\s+([A-Za-z0-9_]+)', content)
        type_name = class_match.group(2) if class_match else file_path.stem
        
        # Chunk into logical blocks of ~30-40 lines or by method signatures
        block_size = 35
        for i in range(0, len(lines), block_size - 10): # 10 line overlap
            block_lines = lines[i:i + block_size]
            chunk_text = "\n".join(block_lines).strip()
            start_line = i + 1
            end_line = min(i + block_size, len(lines))
            
            if len(chunk_text) > 30:
                chunks.append({
                    "source_file": rel_path,
                    "title": f"{rel_path} - {type_name} (Lines {start_line}-{end_line})",
                    "section": f"{type_name} Code",
                    "start_line": start_line,
                    "end_line": end_line,
                    "content": f"File: {rel_path} (Lines {start_line}-{end_line})\n```csharp\n{chunk_text}\n```",
                    "chunk_type": "csharp_code"
                })
                
        return chunks

    def chunk_generic(self, file_path: Path, content: str) -> List[Dict[Any, Any]]:
        """Chunk JSON or solution files."""
        rel_path = str(file_path.relative_to(self.workspace_root)).replace("\\", "/")
        lines = content.splitlines()
        
        return [{
            "source_file": rel_path,
            "title": f"{rel_path} - Configuration & Project Settings",
            "section": "Project Config",
            "start_line": 1,
            "end_line": len(lines),
            "content": f"File: {rel_path}\n```\n{content.strip()}\n```",
            "chunk_type": "config"
        }]

    def ingest_all(self) -> List[Dict[Any, Any]]:
        """Ingest and chunk all project files."""
        all_chunks = []
        files = self.get_target_files()
        
        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    
                if file_path.suffix.lower() == ".md":
                    chunks = self.chunk_markdown(file_path, content)
                elif file_path.suffix.lower() == ".cs":
                    chunks = self.chunk_csharp_code(file_path, content)
                else:
                    chunks = self.chunk_generic(file_path, content)
                    
                all_chunks.extend(chunks)
            except Exception as e:
                print(f"[Ingest Error] Failed processing {file_path}: {e}")
                
        # Assign unique chunk IDs
        for idx, chunk in enumerate(all_chunks, 1):
            chunk["id"] = f"chunk_{idx:03d}"
            
        print(f"[Ingest Complete] Indexed {len(files)} files into {len(all_chunks)} chunks.")
        return all_chunks


if __name__ == "__main__":
    ingestor = DocumentIngestor("c:/MP Online/Assignment aug 01")
    chunks = ingestor.ingest_all()
    print("Sample chunk:", json.dumps(chunks[0], indent=2))
