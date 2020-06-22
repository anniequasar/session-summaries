#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MeetUp 066 - Beginners' Python and Machine Learning - Tue 30 Jun 2020 - PDF

https://youtu.be/FM3LEDckQFA

Learning objectives:
- creating PDFs automatically with reportlab and attaching to emails

@author D Tim Cummings

# Refs:

reportlab PDF creation
https://www.reportlab.com/docs/reportlab-userguide.pdf
https://hg.reportlab.com/hg-public/reportlab/

sample data Homer's Odyssey. Call file odyssey.full.text for running demo odyssey.py in reportlab/demos
https://gutenberg.org/files/1727/1727-0.txt

"""

import builtins
import datetime
import io
import unicodedata

# Task 1. Set up Python project
"""
# If not using IDE such as PyCharm Community Edition, type the following on the command line
mkdir bpaml-email-pdf
cd bpaml-email-pdf
# Copy this file and last week's file into that directory
# meetup065_Tim_email.py
# meetup066_Tim_pdf.py
"""
# Task 2. Create virtual environment
r"""
# If not using IDE type the following on the command line
python -m venv venv                         # Windows
python3 -m venv venv                        # Mac or Linux
conda create --name venv-email-pdf python   # Anaconda

# activate virtual environment
source venv/bin/activate                    # Mac or Linux or Windows Git-Bash
conda activate venv-email-pdf               # Anaconda
venv\Scripts\activate.bat                   # Windows command prompt
venv\Scripts\Activate.ps1                   # Windows powershell
"""
# Task 3: Install requirements
"""
# Add the following to requirements.txt in the project directory
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
aiosmtpd
reportlab

# If you are not using an IDE, install requirements from command line
pip install -r requirements.txt                                   # Windows, Mac or Linux without Anaconda
conda install --name venv-email-pdf --file requirements.txt       # Anaconda
# or if you don't want to use the requirements.txt file
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib aiosmtpd reportlab
"""

# Task 4: Run demo 4 to create a PDF document and save to a file
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4


# Sec 2.1 Basic concepts of reportlab-userguide.pdf
def pdf_demo_4(filename, text):
    # prepare for drawing
    c = Canvas(filename, pagesize=A4)
    # do the drawing
    c.drawString(100, 300, text)
    # save the pdf file
    c.save()


# pdf_demo_4("pdf_demo_4.pdf", "My first ⅖ PDF")


# Task 5: Attach PDF file to an email
# For emailing details see last week's session
# I don't think emailing will work from online services such as Google colab
# https://docs.python.org/3/library/email.examples.html
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
from meetup065_Tim_email import send_message_via_gmail, message_from_str


def message_with_pdf_file_attachment(filename, subject="Task 5: Attaching a PDF document from a file to an email"):
    email_message = message_from_str(subject)
    # PDF should have been created in same directory as this Python script
    with open(filename, 'rb') as file:
        pdf_data = file.read()
    email_message.add_attachment(pdf_data, maintype="application", subtype="pdf", filename="pdf_report.pdf")
    return email_message


# send_message_via_gmail(message_with_pdf_file_attachment("pdf_demo_4.pdf"))


# Task 6: Create PDF in memory and send as email attachment without saving to file
# https://docs.python.org/3/library/io.html
def demo_pdf_report_as_bytes(text):
    """Draws text on a PDF page and returns the PDF report as a string of bytes"""
    # Create a bytes stream to collect all the bytes from the PDF generation in memory
    with io.BytesIO() as pdf_buffer:
        pdf_demo_4(pdf_buffer, text)
        # Need to get a copy of all the bytes in the buffer before buffer is closed
        report = pdf_buffer.getvalue()
    # pdf_buffer.close()  # buffer automatically closed by "with" construct
    return report


def message_with_pdf_attachment(pdf_buffer_value, subject="Task 6: Attaching a PDF document from memory to an email"):
    email_message = message_from_str(subject)
    email_message.add_attachment(pdf_buffer_value, maintype='application', subtype="pdf", filename="pdf_report.pdf")
    return email_message


# send_message_via_gmail(message_with_pdf_attachment(demo_pdf_report_as_bytes("PDF report from memory")))


# Task 7: drawString at different locations in text to work out (rough) coordinates of corners
# Reportlab provides units other than points making it easier to position on page, eg mm, cm, inch
from reportlab.lib.units import mm


# Sec 2.2 More about the canvas
# Sec 2.3 Drawing operations
def pdf_demo_7(file):
    c = Canvas(file, pagesize=A4)
    # Coordinates are in points. 1 point = 1/72 inch. 0, 0 is bottom left corner of page
    for ptx in range(0, int(A4[0]), 2 * 72):
        for pty in range(0, int(A4[1]), 2 * 72):
            c.drawString(ptx, pty, f"({ptx}pt, {pty}pt)")
            c.line(ptx - 5, pty, ptx + 5, pty)
            c.line(ptx, pty - 5, ptx, pty + 5)
    # save everything on current page and move to next page
    c.showPage()
    for mmx in range(0, int(A4[0] // mm), 50):
        for mmy in range(0, int(A4[1] // mm), 50):
            c.drawString(mmx * mm, mmy * mm, f"({mmx}mm, {mmy}mm)")
            c.line((mmx - 2) * mm, mmy * mm, (mmx + 2) * mm, mmy * mm)
            c.line(mmx * mm, (mmy - 2) * mm, mmx * mm, (mmy + 2) * mm)
    # save both pages to file
    c.save()


# pdf_demo_7("pdf_demo_7.pdf")


# Task 8: showPage() creates and saves the page and starts a new one if required. Create a two page PDF
# Sec 2.4 The tools: the "draw" operations
# Sec 2.5 The toolbox: the "state change" operations
# Sec 2.8 Colors
def pdf_demo_8(file):
    c = Canvas(file, pagesize=A4)
    c.drawString(20 * mm, 250 * mm, "This is a paragraph with twenty sentences. " * 20)
    c.drawCentredString(105 * mm, 10 * mm, "Page 1")
    c.showPage()
    c.setStrokeColorRGB(0, 0.9, 0.5)
    c.drawCentredString(105 * mm, 10 * mm, "Page 2")
    c.line((105 - 2) * mm, 10 * mm, (105 + 2) * mm, 10 * mm)
    c.line(105 * mm, (10 - 2) * mm, 105 * mm, (10 + 2) * mm)
    c.save()


# pdf_demo_8("pdf_demo_8.pdf")


# Task 9: Use some of the 14 standard fonts in a PDF
# Sec 2.11 Standard fonts and text objects
def pdf_demo_9(file):
    c = Canvas(file, pagesize=A4)
    x, y = 50 * mm, 280 * mm
    for font in c.getAvailableFonts():
        c.setFont("Courier", 10)
        c.drawRightString(x-5, y, font)
        c.setFont(font, 12)
        c.drawString(x+5, y, "Quick brown fox jumped over the lazy dog")
        y -= 15  # Drop 15 point for each line
    c.setFont("Times-Italic", 10)
    c.drawCentredString(105 * mm, 10 * mm, "Page 1")
    c.save()


# pdf_demo_9("pdf_demo_9.pdf")


# Task 10: Use a text object for automatic positioning of text
# Sec 2.12 Text object methods
def pdf_demo_10(file):
    c = Canvas(file, pagesize=A4)
    text = c.beginText()
    text.setTextOrigin(20*mm, 277*mm)
    text.setFont(psfontname="Times-Roman", size=12, leading=24)
    text.textOut("Text which stays on same line. ")
    text.textOut("More text. ")
    text.textLine("A line that will drop to next line. ")
    text.textLine("A very long line with several sentences but no newline characters. " * 3)
    text.textLine("A paragraph with several sentences and newline characters.\n" * 3)
    text.textLines("This is text with fifty sentences and newline characters.\n" * 50)
    c.drawText(text)
    c.drawCentredString(105 * mm, 10 * mm, "Page 1")
    c.showPage()
    c.drawCentredString(105 * mm, 10 * mm, "Page 2")
    c.save()


# pdf_demo_10("pdf_demo_10.pdf")


# Task 11: Use Platypus to take flowable text more than one page long.
from reportlab.platypus import SimpleDocTemplate, Paragraph, ListItem, ListFlowable, Preformatted, BalancedColumns, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY


# Sec 5.1, 5.2 Platypus
# Sec 6 Paragraphs
# Sec 9.1 Preformatted
# Sec 9.4 Spacer
# Sec 9.10 ListFlowable, ListItem
# Sec 9.11 BalancedColumns
def number_page(canvas, doc_template):
    """Custom function called on every page when rendering in doc.build() to show page numbers. Optional"""
    canvas.line(10*mm, 20*mm, 200*mm, 20*mm)
    canvas.drawCentredString(105*mm, 10*mm, f"Page {canvas.getPageNumber()}")


def pdf_demo_11(file):
    doc = SimpleDocTemplate(file)
    style_sheet = getSampleStyleSheet()
    para_style = style_sheet['BodyText']
    # see dir(para_style) to see list of attributes which can be changed
    para_style.alignment = TA_JUSTIFY
    para_style.spaceBefore = 18
    head_style = style_sheet['Heading2']
    story = []
    story.append(Paragraph("Paragraphs of text", head_style))
    for i in range(10):
        s = f"This <strong>is</strong> <em>paragraph</em> {i} with ten sentences formatted using &lt;strong&gt; and &lt;em&gt; tags. " * 10
        p = Paragraph(s, para_style)
        story.append(p)
    # Spacers currently leave vertical space even though they have parameters for horizontal and vertical
    story.append(PageBreak())
    story.append(Paragraph("Examples of styles", head_style))
    for style_name, style in style_sheet.byName.items():
        style_description = f"{style_name} - {type(style).__name__}"
        # Using duck typing to try out the sample styles
        try:
            p = Paragraph(style_description, style)
        except AttributeError:
            # ListStyle doesn't have fontName attribute so can't be used with a Paragraph
            p = Paragraph(style_description, para_style)
        story.append(p)
    story.append(Paragraph("Builtin functions and classes listed in two columns", head_style))
    list_style = getSampleStyleSheet()["OrderedList"]
    list_style.bulletFontName = "Courier"
    list_style.bulletFontSize = 10
    list_style.leftIndent = 24
    list_items_builtins = [ListItem(Paragraph(b, getSampleStyleSheet()["Normal"])) for b in dir(builtins)]
    story.append(
        BalancedColumns(
            F=[ListFlowable(list_items_builtins, style=list_style)],
            nCols=2
        ))
    story.append(PageBreak())
    # If whitespace important use Preformatted rather than Paragraph
    story.append(Paragraph("Formatting text using whitespace", head_style))
    story.append(Preformatted("""
  ____             _                           _ 
 |  _ \           (_)                         ( )
 | |_) | ___  __ _ _ _ __  _ __   ___ _ __ ___|/ 
 |  _ < / _ \/ _` | | '_ \| '_ \ / _ \ '__/ __|  
 | |_) |  __/ (_| | | | | | | | |  __/ |  \__ \  
 |____/ \___|\__, |_|_| |_|_| |_|\___|_|  |___/  
              __/ |                              
             |___/                               

  _____       _   _                 
 |  __ \     | | | |                
 | |__) |   _| |_| |__   ___  _ __  
 |  ___/ | | | __| '_ \ / _ \| '_ \ 
 | |   | |_| | |_| | | | (_) | | | |
 |_|    \__, |\__|_| |_|\___/|_| |_|
         __/ |                      
        |___/                       
    """, getSampleStyleSheet()["Code"]))
    doc.build(story, onFirstPage=number_page, onLaterPages=number_page)


# pdf_demo_11("pdf_demo_11.pdf")


# Task 12: Create a table in a PDF that spans more than one page
# Using platypus print a "page x of y" at top right of each page
# Sec 7 Tables and TableStyles
from reportlab.platypus import Table


class NumberedCanvas(Canvas):
    """
    Can be used in doc.build() when need to show total number of pages.

    Modify class for position of "Page x of y"
    https://code.activestate.com/recipes/576832-improved-reportlab-recipe-for-page-x-of-y/
    """
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            Canvas.showPage(self)
        Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 8)
        self.drawRightString(200*mm, 280*mm, f"Page {self.getPageNumber()} of {page_count}")


def invoice_header_first(canvas, doc):
    """First page of invoice has company logo, date, and Invoice"""
    canvas.rect(20 * mm, 250 * mm, 12 * mm, 30 * mm)
    canvas.rect(36 * mm, 250 * mm, 12 * mm, 30 * mm)
    canvas.rect(52 * mm, 250 * mm, 12 * mm, 30 * mm)
    canvas.drawString(160 * mm, 250 * mm, "Invoice")
    canvas.drawString(160 * mm, 240 * mm, datetime.date.today().strftime("%d %b %Y"))


def invoice_header_later(canvas, doc):
    """Later pages of invoice have small version of company logo"""
    canvas.rect(20 * mm, 275 * mm, 6 * mm, 15 * mm)
    canvas.rect(28 * mm, 275 * mm, 6 * mm, 15 * mm)
    canvas.rect(36 * mm, 275 * mm, 6 * mm, 15 * mm)


def invoice_data_unicode_numbers():
    """Returns a table of data (list of lists) for demo invoice selling unicode characters ;)"""
    lst_data = [["Item", "Quantity", "Part number", "Description", "Unit price", "Price"]]
    item = 0
    total = 0
    style = getSampleStyleSheet()["Normal"]
    style.fontName = "Helvetica"
    for i in range(4900, 8542):
        c = chr(i)
        # Find numbers other than digits
        if unicodedata.category(c) == "No":
            item += 1
            quantity = i % 10
            part = f"{i}"
            # print(f"{c} {unicodedata.name(c).lower()}")
            description = Paragraph(f"{c} {unicodedata.name(c).lower()}", style)
            unit_price = round(unicodedata.numeric(c), 2)
            price = quantity * unit_price
            total += price
            row = [item, quantity, part, description, f"${unit_price:10,.2f}",  f"${price:10,.2f}"]
            lst_data.append(row)
    lst_data.append(["", "", "", Paragraph("TOTAL", getSampleStyleSheet()["Normal"]), "", f"${total:10,.2f}"])
    return lst_data


def pdf_demo_12(file):
    doc = SimpleDocTemplate(file)
    doc.topMargin = 30 * mm
    story = [Spacer(1, 70*mm)]
    data = invoice_data_unicode_numbers()
    t = Table(data,
              colWidths=[25*mm, 25*mm, 25*mm, 55*mm, 30*mm, 30*mm],
              repeatRows=1)
    t.setStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 2, (0.5, 0.5, 1.0)),
        ('LINEBELOW', (0, 0), (-1, 0), 2, (0.5, 0.5, 1.0)),
        ('LINEBELOW', (0, -2), (-1, -1), 2, (0.5, 0.5, 1.0)),
        ('BACKGROUND', (0, 0), (-1, 0), (0.9, 0.9, 0.9)),
        ('ALIGN', (0, 0), (2, -1), 'CENTRE'),
        ('ALIGN', (3, 0), (3, -1), 'LEFT'),
        ('ALIGN', (4, 0), (5, -1), 'RIGHT'),
        ('VALIGN', (0, 1), (5, -1), 'TOP'),
        ('FONTNAME', (4, 1), (5, -1), 'Courier'),
    ])
    story.append(t)
    doc.build(story, onFirstPage=invoice_header_first, onLaterPages=invoice_header_later, canvasmaker=NumberedCanvas)


# pdf_demo_12("pdf_demo_12.pdf")

# with io.BytesIO() as pdf_buffer:
#     pdf_demo_12(pdf_buffer)
#     send_message_via_gmail(message_with_pdf_attachment(pdf_buffer.getvalue()))
