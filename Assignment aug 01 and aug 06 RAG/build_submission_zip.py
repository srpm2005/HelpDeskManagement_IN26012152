import os
import sys
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

def create_submission_zip():
    workspace_root = Path(__file__).parent.resolve()
    zip_path = workspace_root / "HelpDesk_RAG_Assignment_Submission.zip"

    print("📦 Creating Final Submission ZIP Package with All Recent Screenshots...")

    # Ensure Screenshots directory exists with required figures
    screenshots_dir = workspace_root / "3_Screenshots"
    screenshots_dir.mkdir(exist_ok=True)

    screenshot_source_files = [
        "Screenshot 2026-08-03 235507.png",
        "Screenshot 2026-08-04 001249.png",
        "Screenshot 2026-08-04 001257.png",
        "Screenshot 2026-08-04 001303.png",
        "Screenshot 2026-08-04 001317.png",
        "Screenshot 2026-08-04 001326.png",
        "Screenshot 2026-08-04 001339.png",
        "Screenshot 2026-08-06 210415.png",
        "Screenshot 2026-08-06 210427.png",
        "Screenshot 2026-08-06 210436.png",
        "Screenshot 2026-08-06 210451.png",
        "Screenshot 2026-08-06 210456.png"
    ]

    for f in screenshot_source_files:
        src = workspace_root / f
        if src.exists():
            dest = screenshots_dir / f
            with open(src, "rb") as s, open(dest, "wb") as d:
                d.write(s.read())

    # Map requirement screenshots using recent RAG screenshots
    if (workspace_root / "Screenshot 2026-08-06 210415.png").exists():
        with open(workspace_root / "Screenshot 2026-08-06 210415.png", "rb") as s, open(screenshots_dir / "1_Uploaded_Documentation.png", "wb") as d:
            d.write(s.read())
    if (workspace_root / "Screenshot 2026-08-06 210427.png").exists():
        with open(workspace_root / "Screenshot 2026-08-06 210427.png", "rb") as s, open(screenshots_dir / "2_AI_Answering_Document_Question.png", "wb") as d:
            d.write(s.read())
    if (workspace_root / "Screenshot 2026-08-06 210451.png").exists():
        with open(workspace_root / "Screenshot 2026-08-06 210451.png", "rb") as s, open(screenshots_dir / "3_AI_Responding_NonDocument_Question.png", "wb") as d:
            d.write(s.read())

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        # 1. Main PDF Deliverables
        zipf.write(workspace_root / "1_Project_Documentation.pdf", arcname="1_Project_Documentation.pdf")
        zipf.write(workspace_root / "2_Questions_And_Answers_Document.pdf", arcname="2_Questions_And_Answers_Document.pdf")
        zipf.write(workspace_root / "4_Observation_Report.pdf", arcname="4_Observation_Report.pdf")
        zipf.write(workspace_root / "Section2_Questions_And_Answers.json", arcname="Section2_Questions_And_Answers.json")

        # 2. Screenshots Folder
        for sc in screenshots_dir.glob("*.png"):
            zipf.write(sc, arcname=f"3_Screenshots/{sc.name}")

        # 3. Complete Source Code & Project Files
        excluded_dirs = {".git", ".vs", "bin", "obj", "__pycache__", ".pytest_cache"}
        excluded_extensions = {".zip", ".user"}

        for root, dirs, files in os.walk(workspace_root):
            dirs[:] = [d for d in dirs if d not in excluded_dirs and d != "3_Screenshots"]
            for file in files:
                file_path = Path(root) / file
                if file_path == zip_path or file_path.suffix in excluded_extensions:
                    continue
                if file_path.name.startswith("1_Project") or file_path.name.startswith("2_Questions") or file_path.name.startswith("4_Observation"):
                    continue
                
                rel_path = file_path.relative_to(workspace_root)
                zipf.write(file_path, arcname=f"Source_Code/{rel_path}")

    print(f"🎉 Successfully created updated submission archive at {zip_path}")
    print(f"Archive Size: {zip_path.stat().st_size / (1024*1024):.2f} MB")

if __name__ == "__main__":
    create_submission_zip()
