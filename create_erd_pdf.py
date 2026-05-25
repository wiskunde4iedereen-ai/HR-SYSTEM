from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def create_erd_pdf():
    # Create the PDF document
    doc = SimpleDocTemplate("ERD_Diagram.pdf", pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    story.append(Paragraph("Entity Relationship Diagram (ERD)", title_style))
    story.append(Spacer(1, 20))
    
    # Define table data
    tables_data = [
        ["Table Name", "Columns", "Relationships"],
        [
            "Users",
            "• id (PK) - INTEGER\n• name (VARCHAR(100)) NOT NULL\n• email (VARCHAR(100)) NOT NULL\n• hashed_password (VARCHAR(255)) NOT NULL\n• role (VARCHAR(20)) NOT NULL\n• is_active (BOOLEAN) NOT NULL",
            "Authentication table (no direct relationships)"
        ],
        [
            "Exporters",
            "• id (PK) - INTEGER\n• company_name (VARCHAR(200)) NOT NULL\n• owner_name (VARCHAR(100)) NOT NULL\n• email (VARCHAR(100)) NOT NULL\n• phone (VARCHAR(30))\n• commercial_registry (VARCHAR(50))\n• address (VARCHAR(300))\n• is_active (BOOLEAN) NOT NULL",
            "1:∞ Products (exporter_id)\n1:∞ Licenses (exporter_id)\n1:∞ Finance (exporter_id)"
        ],
        [
            "Markets",
            "• id (PK) - INTEGER\n• country (VARCHAR(100)) NOT NULL\n• city (VARCHAR(100)) NOT NULL\n• requirements (VARCHAR(500)) NOT NULL\n• is_active (BOOLEAN) NOT NULL",
            "1:∞ Licenses (market_id)"
        ],
        [
            "Products",
            "• id (PK) - INTEGER\n• name (VARCHAR(200)) NOT NULL\n• category (VARCHAR(100)) NOT NULL\n• hs_code (VARCHAR(20)) NOT NULL\n• origin (VARCHAR(100)) NOT NULL\n• unit (VARCHAR(20)) NOT NULL\n• exporter_id (INTEGER) NOT NULL\n• is_active (BOOLEAN) NOT NULL",
            "∞:1 Exporters (exporter_id)\n1:∞ Licenses (product_id)"
        ],
        [
            "Licenses",
            "• id (PK) - INTEGER\n• product_id (INTEGER) NOT NULL\n• exporter_id (INTEGER) NOT NULL\n• market_id (INTEGER) NOT NULL\n• status (VARCHAR(20)) NOT NULL\n• notes (TEXT) NOT NULL\n• created_at (DATETIME) NOT NULL\n• approved_at (DATETIME)",
            "∞:1 Products (product_id)\n∞:1 Exporters (exporter_id)\n∞:1 Markets (market_id)\n1:∞ Finance (license_id)\n1:∞ Documents (license_id)"
        ],
        [
            "Finance",
            "• id (PK) - INTEGER\n• license_id (INTEGER) NOT NULL\n• exporter_id (INTEGER) NOT NULL\n• amount (FLOAT) NOT NULL\n• fee_type (VARCHAR(50)) NOT NULL\n• status (VARCHAR(20)) NOT NULL\n• created_at (DATETIME) NOT NULL\n• paid_at (DATETIME)",
            "∞:1 Licenses (license_id)\n∞:1 Exporters (exporter_id)"
        ],
        [
            "Documents",
            "• id (PK) - INTEGER\n• license_id (INTEGER) NOT NULL\n• filename (VARCHAR(255)) NOT NULL\n• filepath (VARCHAR(500)) NOT NULL\n• doc_type (VARCHAR(50)) NOT NULL\n• uploaded_at (DATETIME) NOT NULL",
            "∞:1 Licenses (license_id)"
        ]
    ]
    
    # Create table
    table = Table(tables_data, colWidths=[1.5*inch, 3*inch, 2.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    story.append(table)
    story.append(Spacer(1, 30))
    
    # Add legend
    legend_style = ParagraphStyle(
        'Legend',
        parent=styles['Normal'],
        fontSize=10,
        leftIndent=20
    )
    story.append(Paragraph("<b>Legend:</b>", legend_style))
    story.append(Paragraph("PK = Primary Key", legend_style))
    story.append(Paragraph("FK = Foreign Key", legend_style))
    story.append(Paragraph("1:∞ = One-to-Many relationship", legend_style))
    story.append(Paragraph("∞:1 = Many-to-One relationship", legend_style))
    
    # Build PDF
    doc.build(story)
    print("PDF created successfully: ERD_Diagram.pdf")

if __name__ == "__main__":
    create_erd_pdf()