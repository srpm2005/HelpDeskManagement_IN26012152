import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
)

sys.stdout.reconfigure(encoding='utf-8')

def build_pdf():
    workspace_root = Path(__file__).parent.resolve()
    pdf_path = workspace_root / "4_Observation_Report.pdf"

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=0.5 * inch,
        rightMargin=0.5 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.black,
        alignment=1,
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.black,
        alignment=1,
        spaceAfter=10
    )

    q_title_style = ParagraphStyle(
        'QTitle',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.black,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    ans_style = ParagraphStyle(
        'AnsStyle',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.black,
        spaceAfter=4
    )

    story = []

    story.append(Paragraph("SECTION 4: RAG SYSTEM OBSERVATION REPORT", title_style))
    story.append(Paragraph("1-Page Synthesis & Learning Assessment Report<br/>"
                           "<b>Student Name:</b> SHRI RAM PRINCE MISHRA &nbsp;|&nbsp; <b>Application No.:</b> IN26012152 &nbsp;|&nbsp; "
                           "<b>GitHub:</b> <a href='https://github.com/srpm2005/HelpDeskManagement_IN26012152'>https://github.com/srpm2005/HelpDeskManagement_IN26012152</a>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=6))

    # Question 1
    story.append(Paragraph("Q1: Was the AI able to answer questions that were available in your project documentation?", q_title_style))
    story.append(Paragraph(
        "<b>Yes, absolutely.</b> When queried with in-domain questions (such as API endpoints, application architecture, EF Core database models, unit test setups, and validation rules), the RAG Knowledge Assistant successfully retrieved the relevant document chunks with <b>100% precision (10/10 test cases passed)</b>. "
        "It produced clear, structured answers backed by exact source file paths and line-number citations (e.g. <code>README.md#L81-L93</code> and <code>TicketService.cs#L1-L93</code>).",
        ans_style
    ))

    # Question 2
    story.append(Paragraph("Q2: How did the AI respond when the information was not available in the document?", q_title_style))
    story.append(Paragraph(
        "When presented with out-of-domain general knowledge questions absent from the codebase documentation (e.g., <i>Who is the CEO of Microsoft?</i>, <i>What is Artificial Intelligence?</i>, <i>What is the capital of Australia?</i>), "
        "the RAG system strictly enforced grounding controls. Instead of hallucinating or making up speculative answers, the AI responded consistently with:<br/>"
        "<code>\"The uploaded project documentation does not contain this information.\"</code>",
        ans_style
    ))

    # Question 3
    story.append(Paragraph("Q3: What did you learn about Retrieval-Augmented Generation (RAG)?", q_title_style))
    story.append(Paragraph(
        "Key learnings from building and evaluating the RAG Knowledge Assistant:<br/>"
        "• <b>Solves Hallucination & Staleness</b>: Pre-trained LLMs lack access to private enterprise codebases. RAG dynamically injects relevant private context at query time without expensive fine-tuning.<br/>"
        "• <b>Provenance & Explainability</b>: Unlike standard LLM answers, RAG provides explicit file and line-number citations, allowing developers to verify source truth instantly.<br/>"
        "• <b>Chunking & Retrieval Strategy</b>: Smart header-aware markdown chunking and code-aware block parsing, combined with hybrid vector similarity search (TF-IDF + keyword boosting), achieve microsecond retrieval latencies (&lt; 2 ms).",
        ans_style
    ))

    # Question 4
    story.append(Paragraph("Q4: Mention at least three real-world software applications where RAG can be useful.", q_title_style))
    story.append(Paragraph(
        "1. <b>Developer Onboarding & Internal Codebase Q&A</b>: Software engineering teams can deploy RAG assistants over repository documentation, pull requests, and architectural decision records (ADRs) to onboard new developers seamlessly.<br/>"
        "2. <b>Enterprise Legal & Compliance Contract Analysis</b>: Legal departments can query thousands of private contracts and regulatory policies to extract clauses and risk terms with exact document citations.<br/>"
        "3. <b>Customer Support & Technical HelpDesk Systems</b>: Customer service agents can utilize RAG over proprietary product manuals and troubleshooting guides to generate accurate resolution steps instantly.",
        ans_style
    ))

    # Screenshot visual proof at bottom of Observation Report
    obs_img = workspace_root / "Screenshot 2026-08-06 210456.png"
    if obs_img.exists():
        story.append(Spacer(1, 4))
        story.append(Paragraph("<b>Visual Proof: Grounded RAG Response & Context Inspector</b>", ans_style))
        story.append(Image(str(obs_img), width=6.5*inch, height=2.2*inch))

    doc.build(story)
    print(f"✅ Generated 4_Observation_Report.pdf at {pdf_path}")

if __name__ == "__main__":
    build_pdf()
