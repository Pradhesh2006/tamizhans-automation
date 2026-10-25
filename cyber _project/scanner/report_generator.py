from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
import os
from datetime import datetime

def generate_pdf_report(data, filename="scan_report.pdf"):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(base_dir, "static")
    os.makedirs(static_dir, exist_ok=True)
    path = os.path.join(static_dir, filename)

    doc = SimpleDocTemplate(path, pagesize=letter,
                            rightMargin=40, leftMargin=40,
                            topMargin=40, bottomMargin=40)
    story = []

    # Colors
    dark_bg   = colors.HexColor('#0D1117')
    card_bg   = colors.HexColor('#161B22')
    border    = colors.HexColor('#30363D')
    green     = colors.HexColor('#00FF8C')
    blue      = colors.HexColor('#00B8FF')
    light     = colors.HexColor('#C9D1D9')
    gray      = colors.HexColor('#8B949E')
    red       = colors.HexColor('#FF4757')
    dark_row  = colors.HexColor('#0D1117')

    W = 7.1 * inch  # full content width

    def section_header(icon_title):
        t = Table([[icon_title]], colWidths=[W])
        t.setStyle(TableStyle([
            ('BACKGROUND',   (0,0), (-1,-1), colors.HexColor('#1F2937')),
            ('TEXTCOLOR',    (0,0), (-1,-1), green),
            ('FONTNAME',     (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE',     (0,0), (-1,-1), 12),
            ('LEFTPADDING',  (0,0), (-1,-1), 14),
            ('TOPPADDING',   (0,0), (-1,-1), 10),
            ('BOTTOMPADDING',(0,0), (-1,-1), 10),
        ]))
        return t

    def two_col_table(rows):
        t = Table(rows, colWidths=[1.9*inch, 5.2*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND',   (0,0), (0,-1), colors.HexColor('#1F2937')),
            ('BACKGROUND',   (1,0), (1,-1), card_bg),
            ('TEXTCOLOR',    (0,0), (0,-1), green),
            ('TEXTCOLOR',    (1,0), (1,-1), light),
            ('FONTNAME',     (0,0), (0,-1), 'Helvetica-Bold'),
            ('FONTNAME',     (1,0), (1,-1), 'Helvetica'),
            ('FONTSIZE',     (0,0), (-1,-1), 10),
            ('GRID',         (0,0), (-1,-1), 0.5, border),
            ('TOPPADDING',   (0,0), (-1,-1), 9),
            ('BOTTOMPADDING',(0,0), (-1,-1), 9),
            ('LEFTPADDING',  (0,0), (-1,-1), 12),
            ('ROWBACKGROUNDS',(1,0),(1,-1),[card_bg, dark_row]),
        ]))
        return t

    # ── HEADER ──────────────────────────────────────────
    title_block = Table(
        [["Tamizhan's Security Automation"],
         ["Automated Vulnerability Assessment & Security Scanning Platform"]],
        colWidths=[W]
    )
    title_block.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), dark_bg),
        ('TEXTCOLOR',     (0,0), (0,0),   green),
        ('TEXTCOLOR',     (0,1), (0,1),   gray),
        ('FONTNAME',      (0,0), (0,0),   'Helvetica-Bold'),
        ('FONTNAME',      (0,1), (0,1),   'Helvetica'),
        ('FONTSIZE',      (0,0), (0,0),   20),
        ('FONTSIZE',      (0,1), (0,1),   10),
        ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING',    (0,0), (0,0),   18),
        ('BOTTOMPADDING', (0,0), (0,0),   4),
        ('TOPPADDING',    (0,1), (0,1),   4),
        ('BOTTOMPADDING', (0,1), (0,1),   18),
    ]))
    story.append(title_block)
    story.append(HRFlowable(width="100%", thickness=2, color=green))
    story.append(Spacer(1, 12))

    # ── SCAN INFO ───────────────────────────────────────
    story.append(two_col_table([
        ['Target URL',  str(data.get('target', 'N/A'))],
        ['Scan Date',   datetime.now().strftime('%Y-%m-%d  %H:%M:%S')],
        ['Report By',   "Tamizhan's Security Automation"],
        ['Scan Type',   'Full Vulnerability Assessment'],
    ]))
    story.append(Spacer(1, 14))

    # ── RISK SCORE ──────────────────────────────────────
    risk = data.get('risk', {})
    score = risk.get('score', 0) if risk else 0
    grade = risk.get('grade', 'N/A') if risk else 'N/A'
    sc = '#00FF8C' if score >= 80 else '#FFD700' if score >= 50 else '#FF4757'

    # FIXED: Replaced overlapping raw table strings with Paragraphs and custom styles to enforce clear line separations
    title_style = ParagraphStyle('RiskTitle', fontName='Helvetica-Bold', fontSize=13, textColor=green, alignment=1)
    score_style = ParagraphStyle('RiskScore', fontName='Helvetica-Bold', fontSize=32, leading=36, textColor=colors.HexColor(sc), alignment=1)
    grade_style = ParagraphStyle('RiskGrade', fontName='Helvetica-Bold', fontSize=15, textColor=colors.HexColor(sc), alignment=1)

    risk_table = Table(
        [[Paragraph('Overall Risk Score', title_style)],
         [Paragraph(f"{score} / 100", score_style)],
         [Paragraph(grade, grade_style)]],
        colWidths=[W]
    )
    risk_table.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), card_bg),
        ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
        ('GRID',          (0,0), (-1,-1), 0.5, border),
        ('TOPPADDING',    (0,0), (0,0),   12),
        ('BOTTOMPADDING', (0,0), (0,0),   6),
        ('TOPPADDING',    (0,1), (0,1),   6),
        ('BOTTOMPADDING', (0,1), (0,1),   4),
        ('TOPPADDING',    (0,2), (0,2),   4),
        ('BOTTOMPADDING', (0,2), (0,2),   14),
    ]))
    story.append(risk_table)
    story.append(Spacer(1, 14))

    # ── PORT SCAN ───────────────────────────────────────
    story.append(section_header('🔌   Port Scan Results'))
    ports = data.get('ports', {})
    ip = ports.get('ip', 'N/A')
    open_ports = ports.get('open_ports', [])

    ip_table = Table([['Target IP', str(ip)]], colWidths=[1.9*inch, 5.2*inch])
    ip_table.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(0,-1), colors.HexColor('#1F2937')),
        ('BACKGROUND',   (1,0),(1,-1), card_bg),
        ('TEXTCOLOR',    (0,0),(0,-1), blue),
        ('TEXTCOLOR',    (1,0),(1,-1), light),
        ('FONTNAME',     (0,0),(0,-1), 'Helvetica-Bold'),
        ('FONTSIZE',     (0,0),(-1,-1),10),
        ('GRID',         (0,0),(-1,-1),0.5, border),
        ('TOPPADDING',   (0,0),(-1,-1),9),
        ('BOTTOMPADDING',(0,0),(-1,-1),9),
        ('LEFTPADDING',  (0,0),(-1,-1),12),
    ]))
    story.append(ip_table)

    if open_ports:
        port_data = [['Port', 'Status', 'Risk Level']]
        for p in open_ports:
            rl = 'Critical' if p['port'] in [3306,3389] else 'High' if p['port']==22 else 'Medium'
            port_data.append([str(p['port']), str(p['status']), rl])
        pt = Table(port_data, colWidths=[2.3*inch, 2.4*inch, 2.4*inch])
        pt.setStyle(TableStyle([
            ('BACKGROUND',    (0,0),(-1,0),  colors.HexColor('#1F2937')),
            ('TEXTCOLOR',     (0,0),(-1,0),  blue),
            ('FONTNAME',      (0,0),(-1,0),  'Helvetica-Bold'),
            ('FONTSIZE',      (0,0),(-1,-1), 10),
            ('ROWBACKGROUNDS',(0,1),(-1,-1), [card_bg, dark_row]),
            ('TEXTCOLOR',     (0,1),(-1,-1), light),
            ('GRID',          (0,0),(-1,-1), 0.5, border),
            ('ALIGN',         (0,0),(-1,-1), 'CENTER'),
            ('TOPPADDING',    (0,0),(-1,-1), 9),
            ('BOTTOMPADDING', (0,0),(-1,-1), 9),
        ]))
        story.append(pt)
    else:
        ok = Table([['✅  No open ports found — Good security!']], colWidths=[W])
        ok.setStyle(TableStyle([
            ('BACKGROUND',   (0,0),(-1,-1), card_bg),
            ('TEXTCOLOR',    (0,0),(-1,-1), green),
            ('FONTNAME',     (0,0),(-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE',     (0,0),(-1,-1), 11),
            ('ALIGN',        (0,0),(-1,-1), 'CENTER'),
            ('TOPPADDING',   (0,0),(-1,-1), 12),
            ('BOTTOMPADDING',(0,0),(-1,-1), 12),
            ('GRID',         (0,0),(-1,-1), 0.5, border),
        ]))
        story.append(ok)
    story.append(Spacer(1, 12))

    # ── VULNERABILITY SUMMARY ───────────────────────────
    story.append(section_header('🔍   Vulnerability Summary'))
    sqli = data.get('sqli', {})
    xss  = data.get('xss',  {})
    ssl  = data.get('ssl',  {})

    def status_color(vuln):
        return colors.HexColor('#FF4757') if vuln else green

    vuln_data = [['Test', 'Result', 'Status']]
    tests = [
        ('💉  SQL Injection',      sqli.get('vulnerable', False), 'VULNERABLE','Safe'),
        ('⚡  XSS Detection',      xss.get('vulnerable', False),  'VULNERABLE','Safe'),
        ('🔏  SSL Certificate',    not ssl.get('valid', True),    'INVALID',   'VALID'),
    ]
    for name, bad, bad_label, good_label in tests:
        vuln_data.append([name, bad_label if bad else good_label,
                          '⚠️  Risk Found' if bad else '✅  Passed'])

    vt = Table(vuln_data, colWidths=[2.6*inch, 2.2*inch, 2.3*inch])
    vt.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,0),  colors.HexColor('#1F2937')),
        ('TEXTCOLOR',     (0,0),(-1,0),  blue),
        ('FONTNAME',      (0,0),(-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0,0),(-1,-1), 10),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [card_bg, dark_row]),
        ('TEXTCOLOR',     (0,1),(-1,-1), light),
        ('GRID',          (0,0),(-1,-1), 0.5, border),
        ('ALIGN',         (0,1),(-1,-1), 'CENTER'),
        ('ALIGN',         (0,0),(-1,0),  'CENTER'),
        ('TOPPADDING',    (0,0),(-1,-1), 9),
        ('BOTTOMPADDING', (0,0),(-1,-1), 9),
        ('LEFTPADDING',   (0,1),(0,-1),  12),
    ]))
    story.append(vt)
    story.append(Spacer(1, 12))

    # ── SECURITY HEADERS ────────────────────────────────
    story.append(section_header('🔒   Security Headers Analysis'))
    hdrs = data.get('headers', {})
    if hdrs.get('results'):
        hdata = [['Header Name', 'Status', 'Protects Against']]
        for h in hdrs['results']:
            hdata.append([str(h['header']), str(h['status']), str(h['purpose'])])
        ht = Table(hdata, colWidths=[2.5*inch, 1.4*inch, 3.2*inch])
        ht.setStyle(TableStyle([
            ('BACKGROUND',    (0,0),(-1,0),  colors.HexColor('#1F2937')),
            ('TEXTCOLOR',     (0,0),(-1,0),  blue),
            ('FONTNAME',      (0,0),(-1,0),  'Helvetica-Bold'),
            ('FONTSIZE',      (0,0),(-1,-1), 9),
            ('ROWBACKGROUNDS',(0,1),(-1,-1), [card_bg, dark_row]),
            ('TEXTCOLOR',     (0,1),(-1,-1), light),
            ('GRID',          (0,0),(-1,-1), 0.5, border),
            ('TOPPADDING',    (0,0),(-1,-1), 8),
            ('BOTTOMPADDING', (0,0),(-1,-1), 8),
            ('LEFTPADDING',   (0,0),(-1,-1), 10),
        ]))
        story.append(ht)
    story.append(Spacer(1, 12))

    # ── SSL DETAILS ─────────────────────────────────────
    story.append(section_header('🔏   SSL / TLS Certificate'))
    if ssl.get('valid'):
        story.append(two_col_table([
            ['Issuer',         str(ssl.get('issuer',    'N/A'))],
            ['Expiry Date',    str(ssl.get('expires',   'N/A'))],
            ['Days Remaining', str(ssl.get('days_left', 'N/A'))],
            ['Status',         '✅  Valid and Active'],
        ]))
    else:
        err = Table([[f"❌  Invalid SSL — {ssl.get('error','Unknown error')}"]], colWidths=[W])
        err.setStyle(TableStyle([
            ('BACKGROUND',   (0,0),(-1,-1), card_bg),
            ('TEXTCOLOR',    (0,0),(-1,-1), red),
            ('FONTNAME',     (0,0),(-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE',     (0,0),(-1,-1), 11),
            ('ALIGN',        (0,0),(-1,-1), 'CENTER'),
            ('TOPPADDING',   (0,0),(-1,-1), 12),
            ('BOTTOMPADDING',(0,0),(-1,-1), 12),
            ('GRID',         (0,0),(-1,-1), 0.5, border),
        ]))
        story.append(err)

    # ── FOOTER ──────────────────────────────────────────
    story.append(Spacer(1, 18))
    story.append(HRFlowable(width="100%", thickness=2, color=green))

    footer = Table(
        [["Generated by Tamizhan's Security Automation  |  For authorized security testing only"]],
        colWidths=[W]
    )
    footer.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), dark_bg),
        ('TEXTCOLOR',     (0,0),(-1,-1), gray),
        ('FONTNAME',      (0,0),(-1,-1), 'Helvetica'),
        ('FONTSIZE',      (0,0),(-1,-1), 9),
        ('ALIGN',         (0,0),(-1,-1), 'CENTER'),
        ('TOPPADDING',    (0,0),(-1,-1), 10),
        ('BOTTOMPADDING', (0,0),(-1,-1), 10),
    ]))
    story.append(footer)

    doc.build(story)
    return path