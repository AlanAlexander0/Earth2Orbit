"""
Earth2Orbit — Formal PDF Report Generator
Generates publication-grade scientific PDF dossiers using ReportLab.
"""

import io
from datetime import datetime, timezone
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def generate_dossier_pdf(results: dict, earth_analog: dict, planetary_target: dict, planetary_body: dict) -> bytes:
    """
    Builds a clean, publication-style PDF dossier in memory and returns raw bytes.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    # Custom Scientific Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#142B45'),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=12
    )
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#142B45'),
        spaceBefore=10,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#182B3A'),
        spaceAfter=6
    )
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#182B3A')
    )
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#142B45')
    )

    story = []

    # Header Bar
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    report_id = f"E2O-{results.get('earth_id', '').upper()}-{results.get('target_id', '').upper()}"

    story.append(Paragraph("EARTH2ORBIT — PLANETARY ANALOG EXPLORER", subtitle_style))
    story.append(Paragraph("Planetary Analog Compatibility Evaluation Report", title_style))
    story.append(Paragraph(
        f"Pairing: <b>{earth_analog.get('name')} ({earth_analog.get('country')})</b> ⟷ "
        f"<b>{planetary_target.get('name')} ({planetary_body.get('body_name')})</b><br/>"
        f"Report ID: {report_id} | Date Generated: {timestamp} | Team: QuantumBoyzz",
        subtitle_style
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2864A5'), spaceAfter=12))

    # Executive Summary & Metrics
    story.append(Paragraph("1. Executive Summary & Compatibility Metrics", heading_style))
    story.append(Paragraph(results.get("scientific_interpretation", ""), body_style))
    story.append(Spacer(1, 6))

    # Summary Metrics Table
    aci_val = results.get("aci_score_pct", results.get("fidelity_index_pct", 0.0))
    cov_val = results.get("measurement_coverage_pct", results.get("data_coverage_pct", 0.0))
    evi_val = results.get("evidence_availability_pct", results.get("confidence_score_pct", 0.0))

    metrics_data = [
        [
            Paragraph("<b>Analog Compatibility Index (ACI)</b>", table_header),
            Paragraph("<b>Measurement Coverage</b>", table_header),
            Paragraph("<b>Evidence Availability</b>", table_header)
        ],
        [
            Paragraph(f"<b>{aci_val:.1f}%</b>", title_style),
            Paragraph(f"<b>{cov_val:.1f}%</b> ({results.get('available_count')}/{results.get('total_potential_count')} params)", heading_style),
            Paragraph(f"<b>{evi_val:.1f}%</b> (Verified Sensors)", heading_style)
        ]
    ]
    t_metrics = Table(metrics_data, colWidths=[180, 180, 170])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#E3E9EF')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E3E9EF')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_metrics)
    story.append(Spacer(1, 10))

    # Quantitative Parameter Breakdown
    story.append(Paragraph("2. Physical & Geochemical Parameter Breakdown", heading_style))
    table_rows = [
        [
            Paragraph("Parameter Domain", table_header),
            Paragraph("Earth Analog Value", table_header),
            Paragraph("Planetary Target Value", table_header),
            Paragraph("Distance (d_j)", table_header),
            Paragraph("Score (%)", table_header),
            Paragraph("Status", table_header)
        ]
    ]

    for key, feat in results.get("features", {}).items():
        table_rows.append([
            Paragraph(feat.get("name", ""), table_cell),
            Paragraph(str(feat.get("earth_val", "")), table_cell),
            Paragraph(str(feat.get("target_val", "")), table_cell),
            Paragraph(f"{feat.get('norm_distance', 0.0):.2f}", table_cell),
            Paragraph(f"{feat.get('similarity', 0.0)*100:.1f}%", table_cell),
            Paragraph("Included", table_cell)
        ])

    for ex in results.get("excluded_features", []):
        table_rows.append([
            Paragraph(ex.get("name", ""), table_cell),
            Paragraph(str(earth_analog.get(ex.get("key"), "N/A")), table_cell),
            Paragraph("Not Available (Excluded)", table_cell),
            Paragraph("N/A", table_cell),
            Paragraph("Excluded", table_cell),
            Paragraph("Missing/Vacuum", table_cell)
        ])

    t_params = Table(table_rows, colWidths=[130, 95, 125, 60, 55, 65])
    t_params.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EEF4FA')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#E3E9EF')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#EDF2F7')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_params)
    story.append(Spacer(1, 10))

    # Methodology & Exclusions
    story.append(Paragraph("3. Scientific Methodology & Exclusions", heading_style))
    story.append(Paragraph(
        "The Analog Compatibility Index (ACI) evaluates multi-dimensional similarity using normalized distance:<br/>"
        "<b>d_j = min(1, |x_Earth,j - x_Target,j| / R_j)</b><br/>"
        "<b>ACI = 100 * (1 - Σ(w_j * d_j) / Σ(w_j))</b><br/>"
        "Parameters with missing data or physically absent regimes (such as barometric pressure on the airless lunar surface) "
        "are strictly omitted from the denominator to avoid artificial mathematical distortion. "
        "ACI is an academic exploratory index and not an official NASA ranking.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # Limitations
    story.append(Paragraph("4. Physical & Environmental Limitations", heading_style))
    for lim in results.get("limitations", []):
        story.append(Paragraph(f"• {lim}", body_style))
    story.append(Spacer(1, 6))

    # Verified References
    story.append(Paragraph("5. Verified Field & Planetary References", heading_style))
    for ref in earth_analog.get("references", []):
        story.append(Paragraph(f"• {ref.get('citation')}", body_style))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
