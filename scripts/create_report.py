from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
import re
ROOT=Path(__file__).resolve().parents[1]
text=(ROOT/'docs'/'report_uz.md').read_text(encoding='utf-8')
# DOCX
D=Document(); sec=D.sections[0]; sec.top_margin=Inches(.7); sec.bottom_margin=Inches(.7)
styles=D.styles
styles['Normal'].font.name='Arial'; styles['Normal'].font.size=Pt(10)
styles['Title'].font.name='Arial'; styles['Title'].font.size=Pt(22); styles['Title'].font.bold=True
p=D.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run('PUBLIC TRANSPORT PASSENGER ANALYTICS SYSTEM'); r.bold=True; r.font.size=Pt(20); r.font.color.rgb=RGBColor(31,78,121)
p=D.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run('Jamoat transporti yo‘lovchilarini tahlil qilish tizimi'); r.italic=True; r.font.size=Pt(14)
D.add_paragraph('Universitet joriy nazorat loyihasi', style='Subtitle')
D.add_page_break()
lines=text.splitlines()
for line in lines:
    if not line.strip() or line.startswith('# PUBLIC') or line.startswith('## Jamoat'):
        continue
    if line.startswith('### '): D.add_heading(line[4:], level=2)
    elif line.startswith('## '): D.add_heading(line[3:], level=1)
    elif line.startswith('- '): D.add_paragraph(line[2:], style='List Bullet')
    elif line.startswith('```'):
        continue
    elif line.startswith('|'):
        # Keep Markdown tables readable as monospaced text in this compact report.
        p=D.add_paragraph(line); p.paragraph_format.space_after=Pt(0)
        for rr in p.runs: rr.font.name='Consolas'; rr.font.size=Pt(8)
    else:
        p=D.add_paragraph(line)
        p.paragraph_format.space_after=Pt(4)
        for rr in p.runs:
            if '**' in rr.text: rr.text=rr.text.replace('**','')
D.add_paragraph('\nDataset manbasi: https://zenodo.org/records/3758777')
D.save(ROOT/'docs'/'Loyiha_hisoboti_uz.docx')
# PDF from report markdown with headings and bullet paragraphs
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Cover',parent=styles['Title'],fontName='Helvetica-Bold',fontSize=19,leading=24,alignment=TA_CENTER,textColor=colors.HexColor('#1F4E79'),spaceAfter=12))
styles.add(ParagraphStyle(name='H2x',parent=styles['Heading2'],fontSize=12,leading=15,textColor=colors.HexColor('#1F4E79'),spaceBefore=10,spaceAfter=5))
styles.add(ParagraphStyle(name='Bodyx',parent=styles['BodyText'],fontSize=9,leading=13,spaceAfter=5))
story=[Spacer(1,35*mm),Paragraph('PUBLIC TRANSPORT PASSENGER ANALYTICS SYSTEM',styles['Cover']),Paragraph('Jamoat transporti yo‘lovchilarini tahlil qilish tizimi',styles['Heading2']),Spacer(1,10*mm),Paragraph('Universitet joriy nazorat loyihasi',styles['Bodyx']),PageBreak()]
for line in lines:
    if not line.strip() or line.startswith('# PUBLIC') or line.startswith('## Jamoat'): continue
    if line.startswith('### '): story.append(Paragraph(line[4:],styles['H2x']))
    elif line.startswith('## '): story.append(Paragraph(line[3:],styles['Heading1']))
    elif line.startswith('- '): story.append(Paragraph('• '+line[2:],styles['Bodyx']))
    elif line.startswith('|'):
        story.append(Paragraph(line.replace('|',' &nbsp; | &nbsp;').replace('`',''),styles['Code']))
    elif line.startswith('```'): continue
    else:
        clean=line.replace('**','').replace('`','')
        story.append(Paragraph(clean,styles['Bodyx']))
SimpleDocTemplate(str(ROOT/'docs'/'Loyiha_hisoboti_uz.pdf'),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=16*mm,bottomMargin=16*mm).build(story)
print('Hisobot DOCX va PDF yaratildi.')
