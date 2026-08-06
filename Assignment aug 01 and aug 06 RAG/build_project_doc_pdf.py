import os
import sys
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
    pdf_path = workspace_root / "1_Project_Documentation.pdf"

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
        fontSize=20,
        leading=24,
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
        fontSize=13,
        leading=16,
        textColor=colors.black,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
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

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.black,
        spaceAfter=4
    )

    story = []

    # Document Header & Student Info Banner
    story.append(Paragraph("HELP DESK TICKET MANAGEMENT SYSTEM", title_style))
    story.append(Paragraph("Complete Project Architecture, Source Code & Technical Documentation Report<br/>"
                           "<b>Student Name:</b> SHRI RAM PRINCE MISHRA &nbsp;|&nbsp; <b>Application No.:</b> IN26012152 &nbsp;|&nbsp; "
                           "<b>GitHub:</b> <a href='https://github.com/srpm2005/HelpDeskManagement_IN26012152'>https://github.com/srpm2005/HelpDeskManagement_IN26012152</a>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=12))

    # 1. Project Overview
    story.append(Paragraph("1. Project Overview", h1_style))
    story.append(Paragraph(
        "The <b>Help Desk Ticket Management System (HelpDeskManagement)</b> is an enterprise-grade web application "
        "engineered for internal employee IT support request lifecycle management. Built using modern <b>ASP.NET Core 10.0 Web API</b>, "
        "<b>Entity Framework Core</b>, <b>SQL Server</b>, <b>ASP.NET Core MVC</b>, and <b>xUnit with Moq</b>, the system enables employees "
        "to raise support tickets while empowering IT administrators to review, prioritize, filter, and resolve issues effectively.",
        body_style
    ))

    # 2. Objective of the Application
    story.append(Paragraph("2. Objective of the Application", h1_style))
    story.append(Paragraph(
        "The primary objectives of the Help Desk Ticket Management application are:<br/>"
        "• <b>Streamline IT Support Operations</b>: Centralize all internal employee technical requests into a structured web portal.<br/>"
        "• <b>Decoupled Tier Architecture</b>: Enforce strict separation of concerns between Web API data service and MVC web UI.<br/>"
        "• <b>Data Integrity & Validation</b>: Implement model validations and strict business rules across ticket creation and updates.<br/>"
        "• <b>Automated Testing Isolation</b>: Verify controller logic with 100% test coverage using Moq and xUnit without database dependency.",
        body_style
    ))

    # 3. Project Features
    story.append(Paragraph("3. Key Project Features", h1_style))
    features_data = [
        ["Feature Area", "Description"],
        ["Dashboard Overview", "Displays metric overview cards for Total, Open, and Closed tickets alongside recent tickets."],
        ["Status Filtering", "Interactive filtering table allowing instant view of Open, In Progress, or Closed support tickets."],
        ["Ticket Creation", "Form to raise new tickets with mandatory Title, Description, RaisedBy, and Priority dropdown."],
        ["Edit & Update", "Interface allowing IT support staff to modify ticket Priority level and update Status."],
        ["Ticket Deletion", "Confirmation view permitting ticket removal by ID via Web API REST service."],
        ["RAG Knowledge Assistant", "Integrated AI Assistant enabling new developers to query codebase documentation interactively."]
    ]
    t_features = Table(features_data, colWidths=[1.8*inch, 5.2*inch])
    t_features.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.white),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_features)
    story.append(Spacer(1, 10))

    # 4. Functional Modules
    story.append(Paragraph("4. Functional Modules", h1_style))
    story.append(Paragraph(
        "The project consists of three primary functional modules:<br/>"
        "1. <b>Web API Layer (`HelpDesk.Api`)</b>: RESTful JSON endpoints exposing CRUD operations. Uses Repository Pattern (`ITicketRepository`, `TicketRepository`) and EF Core DbContext for SQL Server.<br/>"
        "2. <b>MVC Application (`HelpDesk.Mvc`)</b>: ASP.NET Core MVC front-end consuming Web API strictly via `TicketService` (`HttpClient`). Enforces a minimalist monochrome white UI design system.<br/>"
        "3. <b>Unit Testing Project (`HelpDesk.Tests`)</b>: Independent xUnit test project mocking `ITicketRepository` via Moq for controller testing.",
        body_style
    ))

    # 5. Database Tables & Schema Specifications
    story.append(Paragraph("5. Database Tables & Schema Specifications", h1_style))
    db_data = [
        ["Column Name", "Data Type", "Constraint", "Description"],
        ["Id", "int", "PRIMARY KEY, IDENTITY(1,1)", "Unique auto-increment ticket identifier"],
        ["Title", "nvarchar(100)", "NOT NULL", "Short summary of the support issue"],
        ["Description", "nvarchar(1000)", "NOT NULL", "Detailed explanation of technical problem"],
        ["Priority", "nvarchar(20)", "NOT NULL", "Priority level: Low, Medium, High"],
        ["Status", "nvarchar(20)", "NOT NULL", "Current status: Open, In Progress, Closed"],
        ["RaisedBy", "nvarchar(50)", "NOT NULL", "Name of employee submitting request"],
        ["CreatedDate", "datetime2", "NOT NULL", "Timestamp when ticket was raised"]
    ]
    t_db = Table(db_data, colWidths=[1.2*inch, 1.3*inch, 1.8*inch, 2.7*inch])
    t_db.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_db)
    story.append(Spacer(1, 10))

    # Page Break for clean layout
    story.append(PageBreak())

    # Header on Page 2
    story.append(Paragraph("HELP DESK TICKET MANAGEMENT SYSTEM - Technical Specification", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=10))

    # 6. Technologies Used
    story.append(Paragraph("6. Technologies Used", h1_style))
    tech_data = [
        ["Layer / Category", "Technology Adopted", "Purpose & Role"],
        ["Framework & Language", "ASP.NET Core 10.0, C# 12", "Core backend and MVC application framework"],
        ["Database & ORM", "Entity Framework Core, SQL Server", "ORM object mapping and database persistence"],
        ["API Communication", "System.Net.Http.Json (HttpClient)", "Decoupled Web API consumption by MVC Service Layer"],
        ["Unit Testing & Mocking", "xUnit 2.8, Moq 4.20", "Automated controller unit testing in isolation"],
        ["Frontend UI/UX", "Razor Views, Bootstrap 5.3, Bootstrap Icons", "Minimalist monochrome white UI design system"],
        ["AI RAG Assistant", "Python, TF-IDF Vectorizer, Streamlit", "Retrieval-Augmented Generation developer onboarding assistant"]
    ]
    t_tech = Table(tech_data, colWidths=[1.8*inch, 2.4*inch, 2.8*inch])
    t_tech.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 10))

    # 7. Business Rules
    story.append(Paragraph("7. Business Rules", h1_style))
    story.append(Paragraph(
        "1. <b>Initial Status Hardcoding</b>: Every newly created ticket MUST automatically have Status set to <b>`Open`</b>.<br/>"
        "2. <b>Strict Service Decoupling</b>: MVC Controllers must consume Web API endpoints strictly through `TicketService`. Direct database connections from MVC are strictly forbidden.<br/>"
        "3. <b>Zero-Database Testing Rule</b>: Unit tests in `HelpDesk.Tests` must mock `ITicketRepository` using Moq with 100% isolated test runs.<br/>"
        "4. <b>Monochrome Design Rule</b>: All web pages must strictly adhere to the monochrome white UI system (white background, 1px solid black border, 90° square edges).",
        body_style
    ))

    # 8. Validation Rules
    story.append(Paragraph("8. Validation Rules", h1_style))
    story.append(Paragraph(
        "• <b>Title</b>: `[Required]`, `[StringLength(100, MinimumLength = 3)]`<br/>"
        "• <b>Description</b>: `[Required]`, `[StringLength(1000)]`<br/>"
        "• <b>RaisedBy</b>: `[Required]`, `[StringLength(50)]`<br/>"
        "• <b>Priority</b>: Required selection from dropdown (`Low`, `Medium`, `High`). Default is `Low`.<br/>"
        "• <b>Status</b>: Hardcoded to `Open` during creation. Dropdown selection (`Open`, `In Progress`, `Closed`) during editing.",
        body_style
    ))

    # 9. Application Workflow Diagram
    story.append(Paragraph("9. Application Architecture & Workflow Diagram", h1_style))
    workflow_text = (
        "┌─────────────────────────────────────────────────────────────────────────────┐\n"
        "│                          USER / BROWSER INTERFACE                           │\n"
        "└──────────────────────────────────────┬──────────────────────────────────────┘\n"
        "                                       │ HTTP GET/POST Requests\n"
        "                                       ▼\n"
        "┌─────────────────────────────────────────────────────────────────────────────┐\n"
        "│               ASP.NET CORE MVC FRONTEND LAYER (HelpDesk.Mvc)                │\n"
        "│  TicketController -> TicketService (HttpClient via System.Net.Http.Json)    │\n"
        "└──────────────────────────────────────┬──────────────────────────────────────┘\n"
        "                                       │ RESTful HTTP JSON (/api/Ticket)\n"
        "                                       ▼\n"
        "┌─────────────────────────────────────────────────────────────────────────────┐\n"
        "│                WEB API BACKEND LAYER (HelpDesk.Api)                         │\n"
        "│  TicketController -> ITicketRepository -> TicketRepository (EF Core)        │\n"
        "└──────────────────────────────────────┬──────────────────────────────────────┘\n"
        "                                       │ SQL Server Queries\n"
        "                                       ▼\n"
        "┌─────────────────────────────────────────────────────────────────────────────┐\n"
        "│                     DATABASE LAYER (SQL Server SQLEXPRESS)                  │\n"
        "│  Table: Tickets (Id, Title, Description, Priority, Status, RaisedBy, Date)   │\n"
        "└─────────────────────────────────────────────────────────────────────────────┘"
    )
    story.append(Paragraph(f"<pre style='font-family:Courier; font-size:8pt;'>{workflow_text}</pre>", code_style))
    story.append(Spacer(1, 10))

    # Page Break for Screenshots Section
    story.append(PageBreak())
    story.append(Paragraph("HELP DESK TICKET MANAGEMENT SYSTEM - Application Screenshots & AI Proof", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=10))

    # 10. Screenshots of Important Views & AI RAG Proof
    story.append(Paragraph("10. Application Screenshots & RAG Knowledge Assistant Visual Proof", h1_style))

    screenshot_files = [
        ("Figure 1: HelpDesk Web API Execution Logs & Port Binding Verification", workspace_root / "Screenshot 2026-08-03 235507.png"),
        ("Figure 2: Help Desk System Dashboard Overview (Total, Open, Closed Cards)", workspace_root / "Screenshot 2026-08-04 001249.png"),
        ("Figure 3: Support Tickets List Table View with Interactive Status Filters", workspace_root / "Screenshot 2026-08-04 001257.png"),
        ("Figure 4: Detailed View of Individual Support Ticket", workspace_root / "Screenshot 2026-08-04 001303.png"),
        ("Figure 5: Raise New Support Ticket Form", workspace_root / "Screenshot 2026-08-04 001317.png"),
        ("Figure 6: Edit Ticket Form (Updating Priority & Status Drops)", workspace_root / "Screenshot 2026-08-04 001326.png"),
        ("Figure 7: AI Knowledge Assistant - Onboarding Preset Query Gallery", workspace_root / "Screenshot 2026-08-06 210415.png"),
        ("Figure 8: RAG Assistant Answering Document Question with Exact Citations", workspace_root / "Screenshot 2026-08-06 210427.png"),
        ("Figure 9: Inspection of Retrieved Context Snippets & Similarity Scores", workspace_root / "Screenshot 2026-08-06 210436.png"),
        ("Figure 10: RAG Assistant Enforcing Strict Grounding for Non-Document Question", workspace_root / "Screenshot 2026-08-06 210451.png"),
        ("Figure 11: Grounding & Provenance Verification View", workspace_root / "Screenshot 2026-08-06 210456.png")
    ]

    for title, img_path in screenshot_files:
        if img_path.exists():
            try:
                story.append(Paragraph(f"<b>{title}</b>", body_style))
                img = Image(str(img_path), width=5.5*inch, height=1.8*inch)
                story.append(img)
                story.append(Spacer(1, 4))
            except Exception as e:
                print(f"[PDF Warning] Error embedding image {img_path}: {e}")

    # Build Document
    doc.build(story)
    print(f"✅ Generated 1_Project_Documentation.pdf at {pdf_path}")

if __name__ == "__main__":
    build_pdf()
