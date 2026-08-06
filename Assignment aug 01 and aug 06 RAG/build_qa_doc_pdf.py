import os
import sys
import json
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)

sys.stdout.reconfigure(encoding='utf-8')

def build_pdf():
    workspace_root = Path(__file__).parent.resolve()
    json_path = workspace_root / "Section2_Questions_And_Answers.json"
    pdf_path = workspace_root / "2_Questions_And_Answers_Document.pdf"

    if not json_path.exists():
        print(f"Error: {json_path} not found. Run run_rag_qa_tests.py first.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        qa_data = json.load(f)

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=0.5 * inch,
        rightMargin=0.5 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.black,
        alignment=1,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.black,
        alignment=1,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'H1Style',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.black,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    cell_question_style = ParagraphStyle(
        'CellQStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.black
    )

    cell_answer_style = ParagraphStyle(
        'CellAStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.black
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.black,
        spaceAfter=6
    )

    story = []

    # Title & Student Header
    story.append(Paragraph("SECTION 2: RAG KNOWLEDGE ASSISTANT Q&A REPORT", title_style))
    story.append(Paragraph("Project Evaluation & Out-of-Domain Grounding Verification<br/>"
                           "<b>Student Name:</b> SHRI RAM PRINCE MISHRA &nbsp;|&nbsp; <b>Application No.:</b> IN26012152 &nbsp;|&nbsp; "
                           "<b>GitHub:</b> <a href='https://github.com/srpm2005/HelpDeskManagement_IN26012152'>https://github.com/srpm2005/HelpDeskManagement_IN26012152</a>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=12))

    # Section 2A Header
    story.append(Paragraph("Section 2A - Questions Answered from the Project Documentation", h1_style))
    story.append(Paragraph("Below are 10 meaningful project questions asked to the RAG Knowledge Assistant and the exact AI-generated grounded responses with document provenance citations:", ParagraphStyle('SubHeader', fontName='Helvetica', fontSize=9, leading=12, spaceAfter=8)))

    # Section 2A Table
    table_data_2a = [
        [Paragraph("<b>#</b>", cell_question_style), Paragraph("<b>Question Asked</b>", cell_question_style), Paragraph("<b>AI Generated Response & Citations</b>", cell_question_style)]
    ]

    for item in qa_data.get("section_2a_document_qa", []):
        q_p = Paragraph(f"<b>{item['question']}</b>", cell_question_style)
        cit_str = f"<br/><br/><b>Citations:</b> <i>{', '.join(item['citations'])}</i>" if item['citations'] else ""
        answer_formatted = item['answer'].replace("\n", "<br/>")
        a_p = Paragraph(f"{answer_formatted}{cit_str}", cell_answer_style)
        table_data_2a.append([Paragraph(item['id'], cell_question_style), q_p, a_p])

    t_2a = Table(table_data_2a, colWidths=[0.5*inch, 2.3*inch, 4.2*inch])
    t_2a.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_2a)
    story.append(Spacer(1, 12))

    # Add Screenshot Visual Proof for Section 2A
    doc_qa_img = workspace_root / "Screenshot 2026-08-06 210427.png"
    if doc_qa_img.exists():
        story.append(Paragraph("<b>Visual Screenshot Proof: RAG Answering Document Question with Citations</b>", body_style))
        story.append(Image(str(doc_qa_img), width=6.5*inch, height=2.8*inch))
        story.append(Spacer(1, 10))

    # Page Break for Section 2B
    story.append(PageBreak())
    story.append(Paragraph("SECTION 2B: OUT-OF-DOMAIN NON-DOCUMENT QUESTION TESTING", title_style))
    story.append(Paragraph("<b>Student Name:</b> SHRI RAM PRINCE MISHRA &nbsp;|&nbsp; <b>Application No.:</b> IN26012152", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=12))

    story.append(Paragraph("Section 2B - Questions Not Available in the Project Documentation", h1_style))
    story.append(Paragraph("Below are 5 questions absent from the uploaded project documentation. This test evaluates the RAG system's hallucination prevention and strict grounding enforcement:", ParagraphStyle('SubHeader', fontName='Helvetica', fontSize=9, leading=12, spaceAfter=8)))

    # Section 2B Table
    table_data_2b = [
        [Paragraph("<b>#</b>", cell_question_style), Paragraph("<b>Non-Document Question</b>", cell_question_style), Paragraph("<b>AI Response (Grounded Fallback)</b>", cell_question_style)]
    ]

    for item in qa_data.get("section_2b_nondocument_qa", []):
        q_p = Paragraph(f"<b>{item['question']}</b>", cell_question_style)
        a_p = Paragraph(f"<i>{item['answer']}</i>", cell_answer_style)
        table_data_2b.append([Paragraph(item['id'], cell_question_style), q_p, a_p])

    t_2b = Table(table_data_2b, colWidths=[0.5*inch, 2.5*inch, 4.0*inch])
    t_2b.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_2b)
    story.append(Spacer(1, 12))

    # Add Screenshot Visual Proof for Section 2B
    nondoc_qa_img = workspace_root / "Screenshot 2026-08-06 210451.png"
    if nondoc_qa_img.exists():
        story.append(Paragraph("<b>Visual Screenshot Proof: RAG Fallback Response for Non-Document Question</b>", body_style))
        story.append(Image(str(nondoc_qa_img), width=6.5*inch, height=2.8*inch))

    doc.build(story)
    print(f"✅ Generated 2_Questions_And_Answers_Document.pdf at {pdf_path}")

if __name__ == "__main__":
    build_pdf()
