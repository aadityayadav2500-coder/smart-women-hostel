"""
Generator for SafeStay Project Report DOCX
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_safestay_report():
    doc = Document()
    
    # Page setup - 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styling helpers
    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'''
            <w:tcMar {nsdecls("w")}>
                <w:top w:w="{top}" w:type="dxa"/>
                <w:bottom w:w="{bottom}" w:type="dxa"/>
                <w:left w:w="{left}" w:type="dxa"/>
                <w:right w:w="{right}" w:type="dxa"/>
            </w:tcMar>
        ''')
        tcPr.append(tcMar)

    def set_table_borders(table, color="CCCCCC"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(f'''
            <w:tblBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="6" w:space="0" w:color="{color}"/>
                <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color}"/>
                <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>
                <w:insideV w:val="single" w:sz="4" w:space="0" w:color="{color}"/>
                <w:left w:val="single" w:sz="6" w:space="0" w:color="{color}"/>
                <w:right w:val="single" w:sz="6" w:space="0" w:color="{color}"/>
            </w:tblBorders>
        ''')
        tblPr.append(borders)

    def format_table(col_widths, headers, data, header_bg="2A1F3D", header_fg="FFFFFF"):
        table = doc.add_table(rows=1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(table, "CCCCCC")
        
        # Header row
        hdr_cells = table.rows[0].cells
        for i, h in enumerate(headers):
            hdr_cells[i].text = h
            set_cell_background(hdr_cells[i], header_bg)
            set_cell_margins(hdr_cells[i], top=120, bottom=120, left=130, right=130)
            p = hdr_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(10)
                run.font.bold = True
                run.font.color.rgb = RGBColor.from_string(header_fg)
                
        # Data rows
        for r_idx, row_data in enumerate(data):
            row_cells = table.add_row().cells
            bg_color = "F9F7F4" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, val in enumerate(row_data):
                row_cells[c_idx].text = str(val)
                set_cell_background(row_cells[c_idx], bg_color)
                set_cell_margins(row_cells[c_idx], top=90, bottom=90, left=130, right=130)
                p = row_cells[c_idx].paragraphs[0]
                if c_idx == 0 or val in ["Pass", "5", "4", "3", "Active", "In", "Paid", "Due", "Overdue"]:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for run in p.runs:
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(9.5)
                    if val == "Pass":
                        run.font.bold = True
                        run.font.color.rgb = RGBColor(42, 131, 87)
                        
        for row in table.rows:
            for i, w in enumerate(col_widths):
                row.cells[i].width = Inches(w)
                
        doc.add_paragraph().paragraph_format.space_after = Pt(6)
        return table

    def add_callout(title, text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, "FBF9F6")
        set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:left w:val="single" w:sz="20" w:space="0" w:color="E89B27"/>
                <w:top w:val="none"/>
                <w:right w:val="none"/>
                <w:bottom w:val="none"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        run_t = p.add_run(f"📌 {title}\n")
        run_t.font.name = "Times New Roman"
        run_t.font.size = Pt(10.5)
        run_t.font.bold = True
        run_t.font.color.rgb = RGBColor(42, 31, 61)
        
        run_b = p.add_run(text)
        run_b.font.name = "Times New Roman"
        run_b.font.size = Pt(10)
        run_b.font.color.rgb = RGBColor(70, 60, 85)
        
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_p(text="", bold_prefix="", italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Times New Roman"
            r_pre.font.size = Pt(11)
            r_pre.font.bold = True
            r_pre.font.color.rgb = RGBColor(28, 21, 43)
        if text:
            r_text = p.add_run(text)
            r_text.font.name = "Times New Roman"
            r_text.font.size = Pt(11)
            r_text.font.italic = italic
            r_text.font.color.rgb = RGBColor(30, 30, 30)
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Times New Roman"
            r_pre.font.size = Pt(11)
            r_pre.font.bold = True
            r_pre.font.color.rgb = RGBColor(28, 21, 43)
        r_text = p.add_run(text)
        r_text.font.name = "Times New Roman"
        r_text.font.size = Pt(11)
        r_text.font.color.rgb = RGBColor(30, 30, 30)
        return p

    def add_h1(title):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(12)
        r = p.add_run(title)
        r.font.name = "Times New Roman"
        r.font.size = Pt(18)
        r.font.bold = True
        r.font.color.rgb = RGBColor(42, 31, 61)
        return p

    def add_h2(title):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(title)
        r.font.name = "Times New Roman"
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = RGBColor(42, 31, 61)
        return p

    def add_h3(title):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(title)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = RGBColor(70, 50, 90)
        return p

    def add_code(code_str):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, "F5F2EB")
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        set_table_borders(tbl, "DCD5CC")
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(code_str)
        r.font.name = "Consolas"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(30, 25, 45)
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ==========================================
    # PAGE 1: TITLE / COVER PAGE
    # ==========================================
    p_t = doc.add_paragraph()
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t.paragraph_format.space_before = Pt(20)
    p_t.paragraph_format.space_after = Pt(12)
    r = p_t.add_run("SafeStay\nSmart Women Hostel Management System")
    r.font.name = "Times New Roman"
    r.font.size = Pt(24)
    r.font.bold = True
    r.font.color.rgb = RGBColor(42, 31, 61)
    
    add_p("A Project Report\nSubmitted in partial fulfillment of the\nRequirements for the award of the Degree of", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
    
    p_deg = doc.add_paragraph()
    p_deg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_deg.paragraph_format.space_after = Pt(14)
    r_deg = p_deg.add_run("BACHELOR OF SCIENCE\n(INFORMATION TECHNOLOGY)")
    r_deg.font.name = "Times New Roman"
    r_deg.font.size = Pt(14)
    r_deg.font.bold = True
    
    add_p("By", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    
    p_team = doc.add_paragraph()
    p_team.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_team.paragraph_format.space_after = Pt(14)
    r_team = p_team.add_run("Aaditya Mangesh Yadav (6420)\n&\nSanskruti Amol Malkar (6452)")
    r_team.font.name = "Times New Roman"
    r_team.font.size = Pt(13)
    r_team.font.bold = True
    
    add_p("Under the esteemed guidance of", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    
    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide.paragraph_format.space_after = Pt(24)
    r_guide = p_guide.add_run("Ms. Aditi Prajapati\n(Asst. Professor)")
    r_guide.font.name = "Times New Roman"
    r_guide.font.size = Pt(12)
    r_guide.font.bold = True
    
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_after = Pt(6)
    r_inst = p_inst.add_run("DEPARTMENT OF INFORMATION TECHNOLOGY\nHindi Vidya Prachar Samiti’s\nRAMNIRANJAN JHUNJHUNWALA COLLEGE OF ARTS, SCIENCE &\nCOMMERCE (EMPOWERED AUTONOMOUS)\n(Affiliated to University of Mumbai)\nGHATKOPAR (West), MUMBAI 400086\n\n2026 - 2027")
    r_inst.font.name = "Times New Roman"
    r_inst.font.size = Pt(11)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(40, 40, 40)
    
    doc.add_page_break()

    # ==========================================
    # PAGE 2: CERTIFICATE
    # ==========================================
    p_cert_head = doc.add_paragraph()
    p_cert_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_head.paragraph_format.space_before = Pt(10)
    p_cert_head.paragraph_format.space_after = Pt(14)
    r = p_cert_head.add_run("Hindi Vidya Prachar Samiti’s\nRAMNIRANJAN JHUNJHUNWALA COLLEGE OF ARTS, SCIENCE &\nCOMMERCE (EMPOWERED AUTONOMOUS)\nGHATKOPAR (West), MUMBAI 400086\nAffiliated to University of Mumbai\n\nDEPARTMENT OF INFORMATION TECHNOLOGY\n\nCERTIFICATE")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True
    
    add_p("This is to certify that project entitled, “SafeStay — Smart Women Hostel Management System” is a bonafide work of Aaditya Mangesh Yadav & Sanskruti Amol Malkar, bearing Roll No. 6420 & 6452 respectively, submitted in partial fulfillment of the requirements for the award of the degree of BACHELOR OF SCIENCE in INFORMATION TECHNOLOGY.", space_after=40)
    
    # Signatures Table
    sig_table = doc.add_table(rows=2, cols=3)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r in sig_table.rows:
        for c in r.cells:
            c.width = Inches(2.1)
    sig_table.rows[0].cells[0].text = "______________________\nInternal Guide\n(Ms. Aditi Prajapati)"
    sig_table.rows[0].cells[1].text = "______________________\nExternal Examiner"
    sig_table.rows[0].cells[2].text = "______________________\nCoordinator\n(Mrs. Archana Bhide)"
    for cell in sig_table.rows[0].cells:
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in cell.paragraphs[0].runs:
            run.font.name = "Times New Roman"
            run.font.size = Pt(10.5)
            run.font.bold = True
            
    p_seal = doc.add_paragraph()
    p_seal.paragraph_format.space_before = Pt(50)
    p_seal.add_run("Date: _____________\t\t\t\t\t\tCollege Seal")
    for r in p_seal.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        r.font.bold = True
        
    doc.add_page_break()

    # ==========================================
    # PAGE 3: ACKNOWLEDGEMENT
    # ==========================================
    add_h1("ACKNOWLEDGEMENT")
    
    add_p("The successful completion of our project “SafeStay — Smart Women Hostel Management System” would not have been possible without the invaluable guidance, encouragement, and support of several individuals. We feel deeply grateful to all those who have contributed to the success of this endeavor.")
    
    add_p("We express our heartfelt gratitude to our respected Head of Department, Mrs. Archana Bhide, for granting us the opportunity to undertake this project and for her continuous support, motivation, and leadership throughout its development. Her valuable guidance has been instrumental in helping us complete our work successfully.")
    
    add_p("We are profoundly thankful to our project guide, Ms. Aditi Prajapati, for her constant encouragement, insightful feedback, and patient guidance at every stage of the project. Her valuable suggestions and technical expertise greatly helped us in shaping the direction, architecture, database design, and execution of our project.")
    
    add_p("Lastly, we also extend our sincere appreciation to our college management, faculty members, and technical staff for providing the necessary resources, computer laboratory facilities, and a supportive environment that enabled the smooth progress of our project work.")
    
    add_p("With sincere appreciation, we acknowledge the contribution of every individual who supported, guided, and inspired us, making this project a truly enriching and successful learning experience.")
    
    p_by = doc.add_paragraph()
    p_by.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_by.paragraph_format.space_before = Pt(24)
    r = p_by.add_run("- by Aaditya Mangesh Yadav (6420) & Sanskruti Amol Malkar (6452)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True
    
    doc.add_page_break()

    # ==========================================
    # PAGE 4: DECLARATION
    # ==========================================
    add_h1("DECLARATION")
    
    add_p("We hereby declare that the project entitled, “SafeStay — Smart Women Hostel Management System”, has been carried out by us independently and has not, in any form, been duplicated, copied, or submitted to any other university or institution for the award of any degree. To the best of our knowledge, no one other than us has submitted this project elsewhere.")
    
    add_p("This project has been completed through our own efforts and under proper guidance, in partial fulfillment of the requirements for the award of the degree of BACHELOR OF SCIENCE (INFORMATION TECHNOLOGY). It is being submitted as our major project as part of the curriculum. We sincerely hope that the work presented herein meets the academic standards and expectations of our institution.")
    
    p_by = doc.add_paragraph()
    p_by.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_by.paragraph_format.space_before = Pt(36)
    r = p_by.add_run("- by Aaditya Mangesh Yadav (6420) & Sanskruti Amol Malkar (6452)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True
    
    doc.add_page_break()

    # ==========================================
    # PAGE 5: ABSTRACT
    # ==========================================
    add_h1("ABSTRACT")
    
    add_p("SafeStay is an intelligent, full-stack web application engineered to solve critical safety, administrative, and operational bottlenecks in modern collegiate women's hostels. Traditional hostel administration relies heavily on fragmented paper registers, physical logbooks, unmonitored gate entries, and manual fee receipts. These legacy methods introduce severe security risks, lack verifiable curfew monitoring, cause delays in resolving student grievances, and fail to provide wardens and guardians with real-time accountability.")
    
    add_p("The SafeStay platform introduces a unified digital ecosystem powered by a Python (Flask) REST backend, a high-concurrency SQLite database operating in Write-Ahead Logging (WAL) mode, and a responsive React 18 frontend. To ensure absolute data privacy and security, the system enforces strict Role-Based Access Control (RBAC) across three completely isolated portals: Resident Student Portal, Floor Warden Portal, and Central Administration Portal. Students cannot access staff operations, wardens cannot modify central financial settings, and administrative controls remain strictly isolated.")
    
    add_p("Core functional innovations include an interactive Digital QR Gate Pass system with dynamic Safe Return Curfew rings, real-time curfew countdowns, and a 1-click Warden gate check-in/out simulator. The platform automates fee invoicing with instant receipt generation, daily student attendance roll-call with floor-level filtering, grievance tracking across maintenance and safety categories, weekly mess menu scheduling with interactive 5-star resident meal feedback, broadcast notice dissemination, and automated CSV ledger exports.")
    
    add_p("SafeStay was developed and validated against a test suite of 20 comprehensive unit, integration, and security test cases. By eliminating paper workflows and providing verifiable digital accountability, SafeStay demonstrates a practical, scalable, and secure solution for institutional hostel management and resident safety.")
    
    doc.add_page_break()

    # ==========================================
    # PAGES 6-7: TABLE OF CONTENTS
    # ==========================================
    add_h1("Table Of Contents")
    
    toc_data = [
        ["1.", "", "Introduction", "1 - 5"],
        ["", "1.1", "Background", "1"],
        ["", "1.2", "Objectives", "1"],
        ["", "1.3", "Purpose & Scope", "2"],
        ["", "1.4", "Achievement", "4"],
        ["", "1.5", "Organization of the Report", "5"],
        ["2.", "", "Survey Of Technologies", "6 - 8"],
        ["", "2.1", "Available Technologies for the project", "6"],
        ["", "2.2", "Selected Technologies & Justification", "7"],
        ["", "2.3", "Advantages & Limitations", "8"],
        ["3.", "", "Requirements & Analysis", "9 - 18"],
        ["", "3.1", "Problem Definition & Sub-problems", "9"],
        ["", "3.2", "Requirement Specification", "10"],
        ["", "3.3", "Planning & Scheduling", "13"],
        ["", "3.4", "Software & Hardware Requirements", "16"],
        ["", "3.5", "Preliminary Product Description", "18"],
        ["4.", "", "Conceptual Models", "19 - 46"],
        ["", "4.1", "DFD / Context Level Diagram", "19"],
        ["", "4.2", "System Flowchart", "23"],
        ["", "4.3", "Database Schema (SQLite Relational Model)", "26"],
        ["", "4.4", "UML Diagrams: Class, Sequence, Use Case", "30"],
        ["5.", "", "System Design", "47 - 77"],
        ["", "5.1", "Data Design", "47"],
        ["", "5.2", "Procedural Design", "48"],
        ["", "5.3", "UI Design", "52"],
        ["6.", "", "Security Issues", "78 - 82"],
        ["", "6.1", "Real-time considerations", "78"],
        ["", "6.2", "Security problems and proposed solutions", "79"],
        ["", "6.3", "Security protocols and policies", "81"],
        ["7.", "", "Testing", "83 - 87"],
        ["", "7.1", "Test Approaches", "83"],
        ["", "7.2", "Test Case Design", "84"],
        ["", "7.3", "Test Plans and Results", "86"],
        ["8.", "", "Conclusion & Future Scope", "88 - 89"],
        ["", "8.1", "Summary of Achievements & Limitations", "88"],
        ["", "8.2", "Suggestions for improvement", "89"],
        ["9.", "", "References", "90"],
        ["", "9.1", "Books, Websites, Tools, APIs used", "90"]
    ]
    
    format_table([0.6, 0.7, 4.3, 0.9], ["Sr. No.", "Sub No.", "Topic", "Page No."], toc_data, header_bg="2A1F3D")
    
    doc.add_page_break()

    # ==========================================
    # CHAPTER 1: INTRODUCTION
    # ==========================================
    add_h1("Chapter 1: Introduction")
    
    add_h2("1.1 Background")
    add_p("In educational institutions and university campuses, providing secure, reliable, and well-managed residential accommodation for female students is a top priority. However, the majority of women's hostels still operate using legacy manual systems. Key daily procedures—such as attendance recording, student leave pass approvals, curfew tracking, complaint redressal, mess meal feedback, and monthly rent collection—are managed through physical paper registers, unverified sign-out notebooks, and manual cash or ledger receipts.")
    
    add_p("These traditional manual methods suffer from severe operational limitations. Physical sign-out sheets can easily be forged, misplaced, or tampered with. There is no reliable mechanism for wardens to immediately know which students are currently outside the hostel premises and who has violated late-night curfew timings. Furthermore, communication between students, floor wardens, and central administration is slow and uncoordinated, leading to unattended maintenance complaints, delayed fee verification, and parent anxiety regarding resident safety.")
    
    add_p("Recognizing these critical challenges, SafeStay is developed as a comprehensive, web-based Smart Women Hostel Management System. SafeStay combines role-isolated portal authentication, digital QR gate pass clearance, real-time curfew countdown monitoring, automated fee tracking, daily roll-call attendance, and structured grievance management into a single unified platform. By digitizing hostel operations, SafeStay establishes transparent accountability, improves resident safety, and streamlines daily administrative overhead.")

    add_h2("1.2 Objectives")
    add_bullet("Strict Role Isolation: ", "To establish separate, dedicated portals for Students, Wardens, and Administrators with zero cross-access or data leakage.")
    add_bullet("Digital Gate Clearance & Curfew Monitoring: ", "To implement an automated exit/leave pass approval system paired with QR code verification and real-time curfew countdown tracking.")
    add_bullet("Real-Time Roll-Call Attendance: ", "To provide wardens with a digital daily attendance register supporting floor filters, individual status toggles, and instant database submission.")
    add_bullet("Automated Fee & Ledger Management: ", "To digitize monthly rent records, simulate online payment settlement, generate authentic receipts, and produce downloadable financial CSV ledgers.")
    add_bullet("Grievance Redressal & Maintenance Tracking: ", "To allow students to lodge categorized maintenance complaints and enable wardens to track, update, and resolve issues systematically.")
    add_bullet("Smart Dining & Mess Accountability: ", "To display weekly meal menus and capture resident star ratings and feedback to monitor hostel dining quality.")

    add_h2("1.3 Purpose & Scope")
    add_h3("I. Purpose")
    add_p("The purpose of SafeStay is to deliver a secure, reliable, and user-friendly web platform that protects resident students, empowers hostel wardens with real-time operational visibility, and provides administrators with comprehensive operational analytics.")
    add_p("By developing this application, we aim to:")
    add_bullet("Protect Resident Safety: ", "Ensure every entry and exit from the hostel is digitally verified and logged against an approved curfew window.")
    add_bullet("Enforce Complete Accountability: ", "Maintain an auditable log of gate movements, fee receipts, leave approvals, and maintenance actions.")
    add_bullet("Eliminate Manual Paperwork: ", "Replace prone-to-damage paper registers with a centralized, queryable relational database.")
    add_bullet("Ensure Multi-Profile Support: ", "Support distinct resident accounts with personalized room allocations, billing histories, and active leave records.")
    add_bullet("Streamline Administrative Decisions: ", "Provide live occupancy metrics (e.g., 184/200 beds, 92%), revenue aging summaries, and instant CSV reports.")

    add_h3("II. Scope")
    add_p("The functional scope of the SafeStay project encompasses three core operational domains:")
    add_bullet("Resident Safety & Gate Management: ", "Digital leave requests (reasons, departure times, expected return times), warden approval/rejection workflows, dynamic Safe Return Rings with overdue curfew detection, and a Gate Scanner simulator supporting manual or QR code lookups.")
    add_bullet("Hostel Amenities & Governance: ", "Categorized complaint filing (Maintenance, Mess, Internet, Safety), status progression (Pending, In Progress, Solved), broadcast notice board with priority flags and resident acknowledgments, and weekly 7-day mess menus with 5-star rating analytics.")
    add_bullet("Financial & Staff Administration: ", "Monthly fee billing ledgers, instant receipt number generation (REC-XXXX), payment reminder broadcasting, new student enrollment, room allocation, warden staff records, and database backup generation.")
    
    add_p("Future Expansion Scope includes integrating physical turnstile RFID card readers, biometric facial recognition scanners at the main entrance, automated SMS/WhatsApp gateways to notify parents upon curfew delays, and live payment gateway hooks (Razorpay/Stripe).")

    add_h2("1.4 Achievements")
    add_p("The SafeStay application successfully establishes a high-performance, full-stack management platform tailored specifically for women's hostel environments. Key technical and practical achievements include:")
    add_bullet("Robust Full-Stack Architecture: ", "Seamlessly integrated a Python (Flask) REST API backend with an optimized SQLite database (WAL mode) and a responsive React 18 frontend.")
    add_bullet("Zero-Leakage Portal Separation: ", "Engineered three distinct portals (Student, Warden, Admin) where credentials, navigation bars, and administrative views are strictly isolated.")
    add_bullet("Multi-Student Ecosystem: ", "Pre-seeded and verified 9 unique resident student profiles (Sanskruti Patil, Aarushi Patel, Diya Shah, Isha Nair, Kavya Singh, Meera Joshi, Nandini Rao, Priya Verma, Riya Das), each exhibiting distinct fee dues, active leave passes, and room details.")
    add_bullet("Real-Time Gate & Curfew Automation: ", "Built dynamic countdown rings that visually indicate on-time clearance (Sage green) or past-curfew alerts (Crimson red) along with 1-click Warden gate check-in/out simulation.")
    add_bullet("Verified Quality & Testing: ", "Successfully executed a 20-case test suite covering unit functionality, API routing, database transactions, and role isolation security with a 100% pass rate.")

    add_h2("1.5 Organization of the Report")
    add_p("This project report is structured into nine comprehensive chapters:")
    add_bullet("Chapter 2 – Survey of Technologies: ", "Evaluates available backend, database, and frontend technologies, justifying the selected stack.")
    add_bullet("Chapter 3 – Requirements and Analysis: ", "Defines the core problem, functional/non-functional requirements, Gantt schedule, work breakdown, and hardware/software prerequisites.")
    add_bullet("Chapter 4 – Conceptual Models: ", "Details the Data Flow Diagrams (DFD), System Flowchart, relational SQLite database schema, Class Diagram, Sequence Diagram, and 11 detailed Use Case specifications.")
    add_bullet("Chapter 5 – System Design: ", "Outlines modular data design, step-by-step procedural operations for all functional modules, and complete UI screen walkthroughs.")
    add_bullet("Chapter 6 – Security Issues: ", "Examines real-time security challenges, mitigations, role-based policies, and database backup procedures.")
    add_bullet("Chapter 7 – Testing: ", "Presents testing methodologies, a comprehensive 20-case test matrix, test plans, and verification results.")
    add_bullet("Chapter 8 – Conclusion and Future Work: ", "Summarizes achievements, acknowledged limitations, and technical avenues for future enhancement.")
    add_bullet("Chapter 9 – References: ", "Lists academic books, official documentation, libraries, and web resources utilized during development.")

    doc.add_page_break()

    # ==========================================
    # CHAPTER 2: SURVEY OF TECHNOLOGIES
    # ==========================================
    add_h1("Chapter 2: Survey of Technologies")
    
    add_h2("2.1 Available Technologies for the Project")
    add_p("During the architecture planning phase of SafeStay, several technology combinations were systematically evaluated across backend frameworks, database management systems, frontend libraries, and styling engines:")
    add_bullet("Backend Frameworks: ", "Python (Flask / FastAPI / Django), Node.js (Express.js), Java (Spring Boot), PHP (Laravel).")
    add_bullet("Database Management Systems: ", "SQLite (Embedded Relational with WAL), PostgreSQL / MySQL (Client-Server Relational), MongoDB (Document NoSQL).")
    add_bullet("Frontend Frameworks: ", "React.js (Component-based Virtual DOM), Vue.js, Angular, Vanilla JavaScript.")
    add_bullet("Styling & UI Engines: ", "Modern CSS3 Custom Properties with CSS Grid / Flexbox, Tailwind CSS, Bootstrap.")
    add_bullet("Report Generation: ", "Native Python CSV engine, ReportLab PDF, Pandas.")
    
    add_p("Each option was assessed based on deployment simplicity on target host machines, ACID transactional consistency, real-time responsiveness, modularity, and rapid development within an academic semester timeframe.")

    add_h2("2.2 Selected Technologies and Justification")
    add_p("Based on technical evaluation, the stack comprising Python (Flask), SQLite (WAL mode), and React 18 was selected as the optimal architecture for SafeStay. Table 2.1 summarizes the selected technologies against considered alternatives.")
    
    tech_table = [
        ["Backend Stack", "Python 3.15 + Flask REST API", "Node.js (Express) / Java Spring Boot", "Lightweight, rapid routing, built-in WSGI support, zero overhead."],
        ["Database", "SQLite 3 with WAL Mode", "MongoDB / MySQL / PostgreSQL", "Zero-configuration, embedded, strict ACID compliance, fast single-file backups."],
        ["Frontend", "React 18 (Babel Standalone)", "Angular / Vue.js", "Component-driven architecture, instant UI re-renders, clean state management."],
        ["Styling Engine", "CSS3 Custom Variables + Glassmorphism", "Bootstrap / Tailwind CSS", "Custom aesthetic, zero external bloat, bespoke Fraunces serif branding."],
        ["Gate Scanner", "QR Conic CSS + Manual ID Code Scanner", "External Camera Hardware Only", "Frictionless simulation of gate check-in/out on desktop and mobile."],
        ["Data Export", "Python CSV Engine", "Heavy Third-Party PDF Exporters", "Clean tabular export of rent ledgers, attendance, and occupancy records."]
    ]
    format_table([1.2, 1.8, 1.7, 1.8], ["Component", "Selected Option", "Alternative Considered", "Technical Justification"], tech_table)

    add_p("Justification Summary:")
    add_bullet("Lightweight & Self-Contained: ", "Python and SQLite require no complex background services or database credential setups, ensuring the project is immediately runnable on any Windows/Linux machine.")
    add_bullet("ACID Consistency: ", "Unlike document databases that lack native multi-table transactional guarantees, SQLite ensures strict atomicity during simultaneous gate check-ins, fee payments, and attendance locking.")
    add_bullet("Write-Ahead Logging (WAL): ", "Enabling WAL mode (`PRAGMA journal_mode=WAL`) allows concurrent database readers and writers without database locking errors.")
    add_bullet("Component Modularity: ", "React 18 isolates portals into independent components (`StudentPortal`, `WardenPortal`, `AdminPortal`), ensuring strict role boundaries.")

    add_h2("2.3 Advantages and Limitations")
    add_h3("Advantages")
    add_bullet("Zero Dependency Friction: ", "Single-command startup via `start.bat` installs minimal requirements (`flask`, `flask-cors`) and launches both backend and frontend seamlessly.")
    add_bullet("Strict Portal Isolation: ", "Guarantees that resident students cannot inspect staff portals or administrative settings, preserving institutional governance.")
    add_bullet("High Responsiveness: ", "Dynamic status badges, real-time curfew countdowns, and instant toast notifications provide immediate user feedback.")
    add_bullet("Auditability: ", "Every administrative and safety event (QR exit, gate return, leave approval, fee payment) is permanently logged to an audit table.")

    add_h3("Limitations")
    add_bullet("Single-Host Database: ", "SQLite is an embedded database designed for single-node deployments; scaling across multiple geographically distributed servers would require migrating to PostgreSQL.")
    add_bullet("Hardware Emulation: ", "Gate scanning currently relies on web-based code lookup and simulated scan modals rather than physical optical turnstiles.")

    doc.add_page_break()

    # ==========================================
    # CHAPTER 3: REQUIREMENTS AND ANALYSIS
    # ==========================================
    add_h1("Chapter 3: Requirements and Analysis")
    
    add_h2("3.1 Problem Definition & Sub-problems")
    add_p("Managing a women's hostel presents multifaceted challenges spanning personal safety, curfew enforcement, fee auditing, daily attendance, and maintenance responsiveness. The core problem is the absence of an integrated, verifiable management platform, forcing reliance on vulnerable manual paper registers.")
    add_p("This overarching problem breaks down into four critical sub-problems:")
    add_bullet("Sub-problem 1: Curfew & Leave Pass Evasion: ", "Physical sign-out sheets lack timestamps and photo verification, making it impossible for wardens to track students who fail to return before night curfew.")
    add_bullet("Sub-problem 2: Fragmented Attendance & Roll-Call: ", "Taking attendance across multiple hostel floors using paper sheets causes delays, misplaced records, and difficult cross-verification during emergencies.")
    add_bullet("Sub-problem 3: Unmonitored Maintenance Grievances: ", "Verbal or handwritten complaints regarding plumbing, Wi-Fi, or electrical failures get lost, resulting in resident dissatisfaction.")
    add_bullet("Sub-problem 4: Manual Fee Collection & Lack of Ledger Transparency: ", "Manual cash/check tracking leads to discrepancies in overdue fee lists, missed payments, and delayed receipt issuance.")

    add_h2("3.2 Requirement Specification")
    add_h3("Functional Requirements")
    
    fn_reqs = [
        ["1", "RQ1 - Separated Authentication", "5", "System must provide distinct, dedicated login portals for Students, Wardens, and Admins with empty input defaults."],
        ["2", "RQ2 - Strict Role Isolation", "5", "Students must be restricted exclusively to resident views, wardens to supervision, and admins to central operations."],
        ["3", "RQ3 - Multi-Profile Management", "5", "System must support multiple resident profiles with distinct rooms, courses, payment histories, and leave passes."],
        ["4", "RQ4 - Leave Pass Application", "5", "Students must be able to apply for gate clearance specifying date, departure time, return time, and reason."],
        ["5", "RQ5 - Warden Leave Approval", "5", "Wardens must be able to review, approve, or reject pending student leave requests with custom reason notes."],
        ["6", "RQ6 - Digital QR Gate Pass", "5", "System must generate a digital boarding-pass style QR gate pass for approved student leave requests."],
        ["7", "RQ7 - Gate Scanner / Check-In/Out", "5", "Wardens must be able to scan QR or input student roll codes to log gate departures and arrivals in real time."],
        ["8", "RQ8 - Safe Return Curfew Ring", "5", "System must display a live countdown ring indicating remaining time to curfew or highlighting late returns in crimson."],
        ["9", "RQ9 - Roll-Call Attendance", "5", "Wardens must be able to mark daily attendance per student (Present/Absent), filter by floor, and lock records."],
        ["10", "RQ10 - Grievance / Complaint Redressal", "4", "Residents can lodge categorized maintenance complaints; wardens can advance status to In Progress and Solved."],
        ["11", "RQ11 - Fee Tracking & Online Payment", "4", "Residents can view monthly dues and pay rent with automated receipt generation (REC-XXXX); admins can mark paid."],
        ["12", "RQ12 - Reporting & CSV Ledger Exports", "4", "Admins must be able to generate and download live CSV reports for Rent Ledgers, Occupancy Rosters, and Attendance."]
    ]
    format_table([0.6, 2.2, 0.7, 3.0], ["Sr No.", "Functional Module", "Priority", "Requirement Specification"], fn_reqs)

    add_h3("Non-Functional Requirements")
    nfn_reqs = [
        ["1", "Usability", "4", "The UI must be intuitive, modern, responsive across desktop and mobile, and require zero training for residents and wardens."],
        ["2", "Reliability", "5", "Database transactions must satisfy strict ACID guarantees using SQLite WAL mode to prevent corruption during simultaneous writes."],
        ["3", "Performance", "4", "All REST API endpoints (login, stats, attendance, gate scan) must respond in under 200ms under standard operational load."],
        ["4", "Security", "5", "Enforce strict server-side role validation, SQL injection prevention via parameterized queries, and sanitized user inputs."],
        ["5", "Availability", "4", "The Flask backend must be capable of running as a background service or daemon with automated heartbeat verification."],
        ["6", "Supportability", "4", "Modular codebase separating database schemas (`database.py`), REST APIs (`app.py`), and frontend components (`index.html`)."],
        ["7", "Compatibility", "3", "Compatible across all modern web browsers (Google Chrome, Mozilla Firefox, Microsoft Edge, Safari) and mobile viewports."]
    ]
    format_table([0.6, 1.4, 0.7, 3.8], ["Sr No.", "Attribute", "Priority", "Requirement Description"], nfn_reqs)

    add_h2("3.3 Planning and Scheduling (Gantt / PERT Chart)")
    add_p("The SafeStay development lifecycle was scheduled across a structured 12-phase timeline totaling 150 project hours. Table 3.3 provides the work breakdown and estimated effort.")
    
    wb_data = [
        ["Phase 1", "Problem Identification & Hostel Stakeholder Requirements", "10"],
        ["Phase 2", "Literature Survey & Existing Hostel System Study", "8"],
        ["Phase 3", "System Architecture & Relational SQLite Schema Design", "14"],
        ["Phase 4", "Backend Environment Setup (Python, Flask, CORS, SQLite)", "8"],
        ["Phase 5", "Separated Portal Authentication & Multi-Student Account Setup", "12"],
        ["Phase 6", "Gate Movement Engine (Leave Pass, QR Pass, Gate Scanner Logic)", "16"],
        ["Phase 7", "Curfew Monitoring & Safe Return Ring Implementation", "14"],
        ["Phase 8", "Daily Attendance Roll-Call & Floor Filtering Module", "12"],
        ["Phase 9", "Grievance Redressal & Mess Feedback System", "14"],
        ["Phase 10", "Fee Billing, Receipt Generation & CSV Export Engine", "16"],
        ["Phase 11", "Frontend UI/UX Polish (Glassmorphism, Fraunces Serif, Toasts)", "12"],
        ["Phase 12", "System Testing, Unit Test Execution & Final Documentation", "14"],
        ["Total", "Complete Project Effort", "150 Hours"]
    ]
    format_table([1.0, 4.3, 1.2], ["Phase", "Activity / Milestones", "Estimated Hours"], wb_data)

    add_h3("Gantt Chart Representation")
    add_p("The project followed a phased waterfall-agile hybrid execution model across 10 academic weeks:")
    add_bullet("Weeks 1–2: ", "Requirements analysis, stakeholder interviews, literature review.")
    add_bullet("Weeks 3–4: ", "Database schema normalization, Flask backend scaffolding, REST API specifications.")
    add_bullet("Weeks 5–6: ", "Core modules development: Leave pass workflows, QR generation, gate scanning logic.")
    add_bullet("Weeks 7–8: ", "Attendance register, grievance redressal, billing engine, mess feedback.")
    add_bullet("Weeks 9–10: ", "UI polish, portal role isolation, 20-case test matrix verification, project report preparation.")

    add_h2("3.4 Software and Hardware Requirements")
    add_h3("Software Requirements")
    sw_data = [
        ["1", "Operating System", "Microsoft Windows 10/11, Linux (Ubuntu/Debian), or macOS"],
        ["2", "Programming Language", "Python 3.15+ (Standard runtime environment)"],
        ["3", "Backend Framework", "Flask 3.1+ (Lightweight WSGI REST application framework)"],
        ["4", "CORS Middleware", "Flask-CORS 6.0+ (Cross-Origin Resource Sharing handler)"],
        ["5", "Database Engine", "SQLite 3.53+ (Embedded relational database with WAL mode)"],
        ["6", "Frontend Engine", "React 18.2 (Component UI) + Babel Standalone (JSX compiler)"],
        ["7", "Typography", "Google Fonts: Fraunces (Serif branding) + Plus Jakarta Sans (UI)"],
        ["8", "Source Code Editor", "Visual Studio Code with Python & React extensions"],
        ["9", "Testing Tools", "Python `urllib` test client, Flask internal test client, Chrome DevTools"]
    ]
    format_table([0.6, 2.2, 3.7], ["Sr No.", "Software Component", "Purpose & Description"], sw_data)

    add_h3("Hardware Requirements")
    hw_data = [
        ["1", "Processor", "Intel Core i3 / AMD Ryzen 3 or higher (Core i5 recommended)"],
        ["2", "Random Access Memory", "Minimum 4 GB RAM (8 GB recommended for concurrent dev)"],
        ["3", "Hard Disk Storage", "Minimum 500 MB free disk space for database, logs, and exports"],
        ["4", "Network Adapter", "Standard Network Interface Card (Localhost loopback or LAN)"],
        ["5", "Display Resolution", "1366 x 768 minimum (1920 x 1080 full HD recommended)"]
    ]
    format_table([0.6, 2.0, 3.9], ["Sr No.", "Hardware Unit", "Minimum / Recommended Specification"], hw_data)

    add_h3("Development Environment")
    add_p("SafeStay was engineered and validated on standard workstation environments. The backend operates on Python's native WSGI HTTP server binding to `127.0.0.1:5000`. The SQLite database file `hostel.db` resides directly in the project root directory, utilizing Write-Ahead Logging for high-concurrency throughput. The frontend is served directly as static HTML5/React from the Flask web server, with built-in CORS support permitting direct browser testing.")

    add_h2("3.5 Preliminary Product Description")
    add_p("SafeStay is an end-to-end, role-isolated web platform for modern hostel governance. When launched, users are greeted with a clean, branded portal selector featuring three dedicated access points: Student Portal, Warden Portal, and Admin Portal. Login credentials are strictly validated against relational database records, with no default pre-fills, ensuring authentic security.")
    add_p("Inside the Student Portal, residents view a personalized dashboard with live curfew countdown rings, apply for digital leave passes, monitor complaint statuses, settle monthly dues with instant receipts, and rate daily meals. The Floor Warden Portal equips wardens with real-time gate departure lists, 1-click check-in simulators, daily attendance registers, and leave pass authorization. The Central Administration Portal gives directors complete operational oversight through bed occupancy analytics, fee aging charts, staff rosters, and downloadable CSV ledgers.")

    doc.add_page_break()

    # ==========================================
    # CHAPTER 4: CONCEPTUAL MODELS
    # ==========================================
    add_h1("Chapter 4: Conceptual Models")
    
    add_h2("4.1 DFD / Context Level Diagram")
    add_p("The Data Flow Diagram (DFD) of SafeStay illustrates how information flows between external entities, backend application processes, and persistent database stores.")

    add_h3("I. External Entities")
    add_bullet("Resident Student: ", "Submits leave pass requests, logs grievances, pays hostel rent, rates meals, and updates profile details.")
    add_bullet("Floor Warden: ", "Reviews leave passes, executes gate check-ins/outs, records daily roll-call attendance, resolves grievances, and broadcasts notices.")
    add_bullet("Operations Administrator: ", "Enrolls new students, allocates rooms, manages staff members, oversees revenue ledgers, and generates CSV reports.")
    add_bullet("Guardian / Emergency Contact: ", "Receives leave notifications and emergency contact links stored on student profile records.")

    add_h3("II. Processes")
    dfd_proc_data = [
        ["P1 - Portal Authentication", "Validates user ID and password against the `users` table for the selected role; establishes secure session."],
        ["P2 - Profile Management", "Retrieves and updates student personal information, phone, email, and emergency contact details."],
        ["P3 - Leave Pass & QR Generation", "Receives exit requests, assigns unique pass code (EX-XXXX), tracks approval state, and renders digital QR pass."],
        ["P4 - Gate Scanner & Movement Log", "Scans student roll ID or pass code, updates resident status between 'In' and 'Out', and records exit/entry timestamps."],
        ["P5 - Roll-Call Attendance", "Renders student lists by floor, captures daily Present/Absent statuses, and commits records to `attendance` table."],
        ["P6 - Grievance Redressal", "Logs resident complaints (CMP-XXXX), notifies wardens, and updates resolution stages."],
        ["P7 - Fee & Invoicing Engine", "Tracks monthly fees, processes payment simulations, issues receipts (REC-XXXX), and updates ledger balances."],
        ["P8 - Dining & Mess Feedback", "Serves weekly 7-day meal schedules and records resident 1–5 star ratings and comments."],
        ["P9 - Notice Broadcast", "Allows wardens/admins to publish priority hostel announcements to the shared bulletin board."],
        ["P10 - Report & Backup Generator", "Compiles live database tables into downloadable CSV files and executes online SQLite database backups."]
    ]
    format_table([1.8, 4.7], ["Process Name", "Process Description & Data Flow"], dfd_proc_data)

    add_h3("III. Data Stores")
    dfd_stores = [
        ["D1 - `users`", "Stores student, warden, and admin accounts, room numbers, courses, contacts, and live curfew statuses."],
        ["D2 - `exit_requests`", "Stores gate pass requests, departure times, expected return times, actual entry times, and warden approval status."],
        ["D3 - `attendance`", "Stores daily roll-call records per student with unique date and roll number constraints."],
        ["D4 - `complaints`", "Stores resident grievances, categories, room locations, descriptions, and resolution statuses."],
        ["D5 - `rent_records`", "Stores monthly fee records, amounts, due dates, payment timestamps, and receipt numbers."],
        ["D6 - `mess_menu` & `feedback`", "Stores daily breakfast/lunch/snacks/dinner menus and resident star ratings with comments."],
        ["D7 - `notices`", "Stores broadcast announcements with priority tags, author roles, and resident acknowledgment arrays."],
        ["D8 - `activity_logs`", "Stores timestamped audit entries for all administrative, security, and gate movement events."]
    ]
    format_table([1.8, 4.7], ["Data Store Name", "Storage Purpose & Entity Mapping"], dfd_stores)

    add_h2("4.2 System Flowchart")
    add_p("The SafeStay System Flowchart maps the complete logic and control flow of the application:")
    add_bullet("1. Portal Selection: ", "The user initiates the system and chooses between Student, Warden, or Admin portal tabs.")
    add_bullet("2. Credential Verification: ", "User enters ID and password. The system checks `users` where `user_code` and `role` match. If invalid, an error is returned; if valid, the isolated portal dashboard opens.")
    add_bullet("3. Student Flow: ", "Student views personalized Safe Return Ring. Can request leave pass (creates `EX-XXXX`), raise complaint (creates `CMP-XXXX`), view rent and pay dues (issues `REC-XXXX`), or rate mess meals.")
    add_bullet("4. Warden Flow: ", "Warden views 'Currently Out' residents. Can approve/reject leave passes, mark attendance roster (commits to `attendance`), scan gate codes (toggles In/Out), or advance complaint statuses.")
    add_bullet("5. Admin Flow: ", "Admin monitors live occupancy, enrolls new students, marks offline fee payments, adds staff members, downloads CSV reports, or triggers SQLite database backups.")
    add_bullet("6. Audit Logging: ", "All state-changing actions converge at `log_activity()`, recording the action to `activity_logs` before session termination.")

    add_h2("4.3 Database Schema (SQLite Relational Model)")
    add_p("Unlike NoSQL document databases that lack relational integrity, SafeStay is built upon a normalized, relational SQLite schema enforcing primary keys, foreign references, unique constraints, and transaction atomicity.")
    
    add_p("The database schema definition in SQL is provided below:")
    sql_schema_code = """-- SafeStay Relational SQLite Schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_code TEXT UNIQUE NOT NULL,      -- e.g. STU-2048, WARD-001, ADMIN-001
    role TEXT NOT NULL,                  -- 'Student', 'Warden', 'Admin'
    name TEXT NOT NULL,
    email TEXT, phone TEXT,
    room TEXT, course TEXT,
    warden_name TEXT, emergency_name TEXT, emergency_phone TEXT,
    status TEXT DEFAULT 'Active',
    curfew_status TEXT DEFAULT 'In',     -- 'In' or 'Out'
    password TEXT NOT NULL DEFAULT 'password',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE exit_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_code TEXT UNIQUE NOT NULL,   -- e.g. EX-2048
    student_code TEXT NOT NULL,
    student_name TEXT NOT NULL, room TEXT NOT NULL,
    date_str TEXT NOT NULL, time_out TEXT NOT NULL, expected_return TEXT NOT NULL,
    actual_exit TEXT, actual_entry TEXT,
    reason TEXT NOT NULL, status TEXT DEFAULT 'Pending', -- 'Pending', 'Approved', 'Rejected', 'Completed'
    reject_reason TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_code TEXT NOT NULL, student_name TEXT NOT NULL,
    room TEXT NOT NULL, course TEXT NOT NULL,
    date_str TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'Present',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_code, date_str)
);

CREATE TABLE complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complaint_code TEXT UNIQUE NOT NULL, -- e.g. CMP-1042
    student_code TEXT, student_name TEXT NOT NULL, room TEXT NOT NULL,
    category TEXT NOT NULL, title TEXT NOT NULL, description TEXT,
    status TEXT DEFAULT 'Pending',       -- 'Pending', 'In Progress', 'Solved', 'Escalated'
    date_str TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE rent_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_code TEXT NOT NULL, student_name TEXT NOT NULL, room TEXT NOT NULL,
    month TEXT NOT NULL, amount INTEGER NOT NULL DEFAULT 8500,
    due_date TEXT NOT NULL, paid_on TEXT,
    status TEXT NOT NULL DEFAULT 'Due',  -- 'Paid', 'Due', 'Overdue'
    receipt_no TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE mess_menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day_of_week TEXT NOT NULL, meal_type TEXT NOT NULL, items TEXT NOT NULL
);

CREATE TABLE mess_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_code TEXT, student_name TEXT,
    day_of_week TEXT NOT NULL, meal_type TEXT NOT NULL,
    rating INTEGER NOT NULL, comment TEXT, addressed INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL, body TEXT NOT NULL, by_role TEXT NOT NULL DEFAULT 'Warden',
    priority INTEGER DEFAULT 0, time_str TEXT, expiry_date TEXT,
    acknowledged_by TEXT DEFAULT '[]', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE staff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL, role TEXT NOT NULL, block_floor TEXT NOT NULL, contact TEXT NOT NULL, status TEXT DEFAULT 'Approved'
);

CREATE TABLE settings ( key TEXT PRIMARY KEY, value TEXT NOT NULL );
CREATE TABLE activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT, user_role TEXT NOT NULL, user_code TEXT, action TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"""
    add_code(sql_schema_code)

    add_h2("4.4 UML Diagrams: Class, Sequence, Use Case")
    add_h3("I. Class Diagram")
    add_p("The SafeStay Class Diagram captures the primary object models, their core attributes, operational methods, and relationships:")
    add_bullet("User: ", "Attributes: id, user_code, role, name, room, course, curfew_status. Methods: login(), updateProfile(), logout().")
    add_bullet("ExitRequest: ", "Attributes: id, request_code, student_code, time_out, expected_return, status. Methods: create(), approve(), reject(), logEntry().")
    add_bullet("AttendanceRecord: ", "Attributes: id, student_code, date_str, status. Methods: mark(), submitRoster().")
    add_bullet("Complaint: ", "Attributes: id, complaint_code, category, title, status. Methods: lodge(), updateStatus(), resolve().")
    add_bullet("RentRecord: ", "Attributes: id, student_code, month, amount, status, receipt_no. Methods: payRent(), issueReceipt(), exportLedger().")
    add_bullet("MessFeedback: ", "Attributes: id, student_code, day_of_week, meal_type, rating. Methods: submitRating(), markAddressed().")

    add_h3("II. Sequence Diagram (Gate Check-In / Check-Out Workflow)")
    add_p("The sequence flow details the real-time interaction during student gate clearance:")
    add_bullet("1. Leave Application: ", "Student submits leave pass via UI -> Backend validates departure/return time -> Creates `EX-XXXX` in `exit_requests` (Status: Pending).")
    add_bullet("2. Warden Clearance: ", "Warden opens Approvals -> Clicks 'Approve' -> Backend sets status to 'Approved' -> Student UI renders active Digital QR Gate Pass.")
    add_bullet("3. Gate Departure: ", "Student shows QR at gate -> Warden inputs code or clicks 'Check Out' -> Backend records `actual_exit`, toggles `curfew_status` to 'Out', logs event to `activity_logs`.")
    add_bullet("4. Curfew Monitoring: ", "Safe Return Ring computes remaining minutes -> If time surpasses curfew, UI pulses Crimson alert.")
    add_bullet("5. Safe Return Entry: ", "Student returns -> Code scanned -> Backend logs `actual_entry`, sets pass status to 'Completed', toggles `curfew_status` to 'In'.")

    add_h3("III. Use Case Diagrams & Scenarios")
    add_p("Actors:")
    add_bullet("Student: ", "Resident managing personal profile, applying for gate passes, tracking grievances, paying rent, and rating dining.")
    add_bullet("Warden: ", "Floor supervisor approving leaves, operating gate scanner, submitting roll-call attendance, and handling complaints.")
    add_bullet("Admin: ", "Operations manager overseeing hostel occupancy, enrolling residents, managing staff, and generating financial reports.")

    uc_summary_table = [
        ["UC01", "Resident Authentication", "Student / Warden / Admin", "Users sign into their strictly isolated portals using roll ID and password."],
        ["UC02", "Profile & Contact Management", "Student", "Residents update personal phone, email, and guardian emergency contacts."],
        ["UC03", "Leave Pass Application", "Student", "Residents submit gate leave requests with return times and reasons."],
        ["UC04", "Leave Clearance & Approval", "Warden", "Wardens review pending leave requests and approve or reject them."],
        ["UC05", "Gate Check-In / Check-Out", "Warden", "Warden scans QR or inputs student ID to log gate movements and curfew state."],
        ["UC06", "Roll-Call Attendance", "Warden", "Wardens mark daily resident attendance by floor and commit records."],
        ["UC07", "Grievance Lodging & Redressal", "Student / Warden", "Students lodge maintenance issues; wardens track and resolve them."],
        ["UC08", "Fee Payment & Receipt Issuance", "Student / Admin", "Students settle monthly dues; system generates official receipt number."],
        ["UC09", "Mess Dining Rating", "Student / Warden", "Residents submit star ratings on meals; wardens inspect weekly trend charts."],
        ["UC10", "Notice Board Broadcast", "Warden / Admin", "Staff publish priority announcements; residents acknowledge receipt."],
        ["UC11", "Reporting & Backup", "Admin", "Admins download CSV fee/attendance ledgers and trigger SQLite backups."]
    ]
    format_table([0.7, 1.8, 1.4, 2.6], ["Use Case ID", "Use Case Name", "Primary Actor", "Scope & Description"], uc_summary_table)

    # Detailed Use Case Specifications UC01 - UC11
    use_cases_detailed = [
        ("UC01", "Resident Authentication", "Student / Warden / Admin", "RQ1, RQ2", "User enters portal-specific ID and password. System verifies credentials against `users` table for matching role. Issues session state and opens role-isolated dashboard."),
        ("UC02", "Profile & Contact Management", "Student", "RQ3", "Student navigates to 'My Profile'. Edits phone, email, emergency guardian contact. System commits updates to SQLite `users` table."),
        ("UC03", "Leave Pass Application", "Student", "RQ4, RQ6", "Student fills leave pass modal with date, departure time, return time, reason. System assigns pass code `EX-XXXX` and sets status to 'Pending'."),
        ("UC04", "Leave Clearance & Approval", "Warden", "RQ5", "Warden opens 'Entry / Exit Approvals'. Reviews pending student requests. Clicks 'Approve' or 'Reject' with reason. Updates `exit_requests` table."),
        ("UC05", "Gate Check-In / Check-Out", "Warden", "RQ7, RQ8", "Warden enters roll ID or pass code into Gate Scanner. If student is 'In', logs exit and marks 'Out'. If student is 'Out', logs entry, marks 'In', and completes leave pass."),
        ("UC06", "Roll-Call Attendance", "Warden", "RQ9", "Warden accesses Attendance register. Filters by floor. Toggles Present/Absent per student or clicks 'Mark all Present'. Commits daily attendance records."),
        ("UC07", "Grievance Lodging & Redressal", "Student / Warden", "RQ10", "Student lodges complaint specifying category and description. Assigned `CMP-XXXX`. Warden inspects queue and updates status to 'In Progress' and 'Solved'."),
        ("UC08", "Fee Payment & Receipt Issuance", "Student / Admin", "RQ11", "Student views current month dues and clicks 'Pay Now'. System simulates payment, updates status to 'Paid', and issues receipt `REC-XXXX`."),
        ("UC09", "Mess Dining Rating", "Student / Warden", "RQ10", "Student selects day of week and clicks 1–5 star rating on meal cards. System commits rating to `mess_feedback`. Warden views weekly average chart."),
        ("UC10", "Notice Board Broadcast", "Warden / Admin", "RQ10", "Staff composes notice with title, body, priority flag. System publishes notice to resident feed. Residents can click 'Acknowledge'."),
        ("UC11", "Reporting & Backup", "Admin", "RQ12", "Admin selects report type (Rent, Attendance, Complaints, Occupancy) and clicks 'Generate'. System compiles and downloads CSV file; backup creates `.db` snapshot.")
    ]
    
    for ucid, ucname, actor, reqs, desc in use_cases_detailed:
        uc_table = [
            ["Use Case ID", ucid],
            ["Use Case Name", ucname],
            ["Related Requirements", reqs],
            ["Primary Actor", actor],
            ["Flow of Events", desc]
        ]
        format_table([1.8, 4.7], ["Specification Field", "Details"], uc_table, header_bg="4A3B63")

    doc.add_page_break()

    # ==========================================
    # CHAPTER 5: SYSTEM DESIGN
    # ==========================================
    add_h1("Chapter 5: System Design")
    
    add_h2("5.1 Data Design")
    add_p("The data design organizes system functionality into distinct logical modules assigned to specific user roles, ensuring clear separation of concerns:")
    
    data_design_table = [
        ["1", "Authentication & Session Module", "Student / Warden / Admin"],
        ["2", "Resident Profile & Emergency Contact Module", "Student"],
        ["3", "Leave Request & Gate Pass Issuance Module", "Student"],
        ["4", "Gate Movement & Curfew Clearance Module", "Warden"],
        ["5", "Roll-Call Daily Attendance Module", "Warden"],
        ["6", "Maintenance Grievance & Redressal Module", "Student / Warden / Admin"],
        ["7", "Dining Schedule & Meal Rating Module", "Student / Warden"],
        ["8", "Fee Billing, Payments & Receipt Module", "Student / Admin"],
        ["9", "Resident Directory & Occupancy Module", "Warden / Admin"],
        ["10", "Staff Management & Infrastructure Module", "Admin"],
        ["11", "Reporting & Database Backup Module", "Admin"]
    ]
    format_table([0.6, 3.8, 2.1], ["Sr No.", "Functional Module Name", "Target Actor / Scope"], data_design_table)

    add_h2("5.2 Procedural Design")
    add_p("The procedural design specifies the step-by-step algorithms governing each core system module:")
    
    add_h3("1. User Authentication & Portal Entry")
    add_bullet("Step 1: ", "User opens the web application and selects Student, Warden, or Admin portal tab.")
    add_bullet("Step 2: ", "User inputs their roll ID / authorization code and password (fields start blank).")
    add_bullet("Step 3: ", "Frontend sends `POST /api/login` payload `{role, user_code, password}`.")
    add_bullet("Step 4: ", "Backend verifies credentials against `users` table where role matches. If invalid, returns 401/404.")
    add_bullet("Step 5: ", "If valid, backend returns sanitized user profile. Frontend locks view into the designated portal.")

    add_h3("2. Leave Pass Clearance & QR Issuance")
    add_bullet("Step 1: ", "Resident student opens 'Entry / Exit' and clicks 'Request Exit Pass'.")
    add_bullet("Step 2: ", "Student inputs date, departure time, expected return time, and purpose.")
    add_bullet("Step 3: ", "Backend inserts record into `exit_requests` with code `EX-XXXX` and status 'Pending'.")
    add_bullet("Step 4: ", "Warden opens Approvals queue, verifies details, and clicks 'Approve'.")
    add_bullet("Step 5: ", "Backend updates status to 'Approved'. Student portal automatically renders digital QR gate pass.")

    add_h3("3. Gate Scanner & Curfew Detection")
    add_bullet("Step 1: ", "Warden enters roll ID (e.g. `STU-2048`) or pass code (`EX-2048`) into Gate Scanner.")
    add_bullet("Step 2: ", "Backend queries student's current `curfew_status`.")
    add_bullet("Step 3: ", "If status is 'In', backend logs `actual_exit = now()`, sets status to 'Out', and commits.")
    add_bullet("Step 4: ", "If status is 'Out', backend logs `actual_entry = now()`, marks pass 'Completed', and sets status to 'In'.")
    add_bullet("Step 5: ", "If entry timestamp exceeds curfew time, backend flags return as late in activity audit logs.")

    add_h3("4. Daily Roll-Call Attendance Locking")
    add_bullet("Step 1: ", "Warden opens Attendance module for today's date.")
    add_bullet("Step 2: ", "Warden filters residents by floor or uses search box.")
    add_bullet("Step 3: ", "Warden toggles Present/Absent or clicks 'Mark all Present'.")
    add_bullet("Step 4: ", "Warden clicks 'Submit & Lock Attendance'. Backend executes upsert transaction on `attendance` table.")

    add_h3("5. Fee Payment & Receipt Issuance")
    add_bullet("Step 1: ", "Student navigates to 'Rent & Billing' and reviews current month dues.")
    add_bullet("Step 2: ", "Student clicks 'Pay Now'. System simulates payment verification.")
    add_bullet("Step 3: ", "Backend marks rent record as 'Paid', assigns `paid_on = today()`, and generates `REC-XXXX`.")
    add_bullet("Step 4: ", "Student instantly downloads official payment receipt with stamp.")

    add_h2("5.3 UI Design")
    add_p("SafeStay features an editorial, high-aesthetic user interface designed for maximum clarity, rapid navigation, and resident confidence.")

    add_h3("External UI Components")
    ext_comp = [
        ["Portal Selector Screen", "Allows users to switch cleanly between Student, Warden, and Admin sign-in forms."],
        ["Resident Home Dashboard", "Presents Safe Return curfew ring, active complaint count, dues, and priority notices."],
        ["Digital Gate Pass Card", "Boarding-pass styled QR clearance card displaying pass code, room, and return curfew."],
        ["Warden Curfew Cockpit", "Displays all currently-out residents with real-time countdowns and 1-click Check-In buttons."],
        ["Roll-Call Attendance Table", "Interactive daily attendance roster with floor filters and individual status buttons."],
        ["Grievance Management Desk", "Tabbed complaint tracking board with status badges (Pending, In Progress, Solved)."],
        ["Dining Menu & Rating Grid", "7-day weekly meal timetable with interactive 5-star rating buttons."],
        ["Admin Operations Dashboard", "High-level overview showing 92% occupancy gauge, revenue counters, and aging charts."]
    ]
    format_table([2.0, 4.5], ["External Component", "Visual Functionality & User Experience"], ext_comp)

    add_h3("Internal Components")
    int_comp = [
        ["Database Layer (`hostel.db`)", "SQLite database executing in WAL mode with connection busy timeouts."],
        ["REST API Server (`app.py`)", "Flask application handling endpoints, parameter validation, and session responses."],
        ["Schema Engine (`database.py`)", "Initializes tables, seeds demo profiles, and manages table constraints."],
        ["Audit Logger (`activity_logs`)", "Appends timestamped security and gate movement events for institutional auditing."],
        ["CSV Exporter Engine", "Streams structured CSV files directly to browser downloads without disk leakage."]
    ]
    format_table([2.0, 4.5], ["Internal Component", "Technical Role & Operational Architecture"], int_comp)

    add_h3("Design Considerations")
    add_bullet("Color Palette: ", "Deep Royal Plum (`#1C152B`) for sidebars, Golden Marigold (`#E89B27`) for primary call-to-actions, Emerald Sage (`#2A8357`) for verified states, and Terracotta Brick (`#C24131`) for curfew alerts.")
    add_bullet("Typography: ", "Fraunces serif headings for institutional authority paired with Plus Jakarta Sans for clean readability.")
    add_bullet("Micro-Interactions: ", "Smooth hover states, animated circular countdown rings, and non-blocking toast alerts.")

    doc.add_page_break()

    # ==========================================
    # CHAPTER 6: SECURITY ISSUES
    # ==========================================
    add_h1("Chapter 6: Security Issues")
    
    add_h2("6.1 Real-Time Considerations")
    add_p("Because SafeStay governs resident safety, gate movements, and financial records, security must be continuously enforced in real time:")
    add_bullet("Strict Portal Isolation: ", "Session states and client navigation bars are locked to the user's role upon login. Students cannot invoke or view warden or administrative endpoints.")
    add_bullet("Curfew Alert Monitoring: ", "The system continuously computes time elapsed against approved curfew return windows, alerting wardens to late residents in real time.")
    add_bullet("Database Concurrency & Integrity: ", "Operating SQLite in Write-Ahead Logging (WAL) mode prevents database locking during simultaneous roll-call submissions and gate scans.")
    add_bullet("No Default Credentials: ", "Input fields load empty by default, preventing unauthorized 1-click access from shared public or library terminals.")

    add_h2("6.2 Security Problems and Proposed Solutions")
    sec_probs = [
        ["Unauthorized Role Escalation", "A student attempts to access warden leave approvals or administrative settings.", "Server-side role verification on every API route; UI components conditionally rendered only for verified roles."],
        ["Curfew Evasion / False Checkout", "A resident departs without authorization or signs out another resident.", "Leave passes require explicit warden clearance and generate unique QR pass codes linked to the resident's ID."],
        ["Database Write Collision", "Simultaneous attendance submissions and gate scans cause database locked errors.", "Enabled SQLite WAL mode (`PRAGMA journal_mode=WAL`) and configured busy timeouts (`busy_timeout=5000`)."],
        ["Credential Guessing / Brute Force", "Attacker attempts to guess login passwords on the portal login screen.", "Inputs are sanitized; rate-limiting hooks supported; login returns generic 401 errors without leaking account existence."],
        ["Data Loss / Accidental Deletion", "Database file corruption or host system failure deletes resident records.", "Built-in online SQLite backup engine (`/api/backup`) creates timestamped snapshots in `backups/` directory."]
    ]
    format_table([1.6, 2.3, 2.6], ["Security Threat", "Threat Description", "Proposed Technical Solution"], sec_probs)

    add_h2("6.3 Security Protocols and Policies")
    add_bullet("Input Sanitization & Parameterization: ", "All database queries use parameterized SQL (`?` placeholders), preventing SQL injection vulnerabilities.")
    add_bullet("Audit Logging Protocol: ", "Every significant administrative event (leave approval, gate check-in, fee receipt issuance) is permanently written to `activity_logs`.")
    add_bullet("Database Backup Policy: ", "The administration portal includes a 1-click backup button utilizing SQLite's online backup API to create non-blocking database copies.")

    doc.add_page_break()

    # ==========================================
    # CHAPTER 7: TESTING
    # ==========================================
    add_h1("Chapter 7: Testing")
    
    add_h2("7.1 Testing Approaches")
    add_p("The SafeStay testing strategy verified reliability, role security, database consistency, and UI responsiveness across multiple levels:")
    add_bullet("Unit Testing: ", "Tested individual backend REST endpoints (login validation, leave pass creation, attendance upsert, fee payment).")
    add_bullet("Integration Testing: ", "Verified seamless communication between React frontend `fetch()` API calls and Flask endpoints.")
    add_bullet("Security & Role Isolation Testing: ", "Tested cross-portal penetration (e.g. submitting student roll codes to warden/admin login endpoints).")
    add_bullet("User Acceptance Testing (UAT): ", "Evaluated workflows from the perspective of resident students, floor wardens, and hostel administrators.")

    add_h2("7.2 Test Case Design")
    add_p("A comprehensive test matrix of 20 test cases was designed and executed against the live application:")
    
    test_cases_data = [
        ["TC01", "Student Login (Valid)", "Enter STU-2048 / password", "Student portal opens with Sanskruti profile", "Pass"],
        ["TC02", "Student Login (Wrong Password)", "Enter STU-2048 / wrongpass", "Rejected with 401 Unauthorized", "Pass"],
        ["TC03", "Empty Login Submission", "Submit blank ID and password", "Rejected with 400 Bad Request error", "Pass"],
        ["TC04", "Cross-Portal Login Rejection", "Enter STU-2048 on Warden portal", "Rejected with 404 Not Found error", "Pass"],
        ["TC05", "Multi-Student Account Switch", "Login with STU-1001 (Aarushi)", "Aarushi profile loads (Room A-101)", "Pass"],
        ["TC06", "Student Profile Update", "Edit phone & emergency contact", "Updated fields saved to SQLite `users`", "Pass"],
        ["TC07", "Leave Pass Application", "Submit exit request with date/time", "New request `EX-XXXX` created (Pending)", "Pass"],
        ["TC08", "Warden Leave Approval", "Click 'Approve' on pending leave", "Status changes to 'Approved' in DB", "Pass"],
        ["TC09", "Warden Leave Rejection", "Click 'Reject' with reason note", "Status changes to 'Rejected' with reason", "Pass"],
        ["TC10", "Digital QR Pass Rendering", "View approved leave request", "Digital boarding-pass card renders QR", "Pass"],
        ["TC11", "Gate Checkout Scan", "Scan student ID while 'In'", "Status toggles to 'Out'; exit time logged", "Pass"],
        ["TC12", "Gate Check-In Scan", "Scan student ID while 'Out'", "Status toggles to 'In'; pass Completed", "Pass"],
        ["TC13", "Curfew Alert Display", "View resident out past curfew", "Safe Return Ring turns crimson red", "Pass"],
        ["TC14", "Attendance Roster Submission", "Mark Present/Absent and submit", "Roster committed to `attendance` table", "Pass"],
        ["TC15", "Grievance Lodging", "Submit tap leakage complaint", "Created `CMP-XXXX` (Pending)", "Pass"],
        ["TC16", "Complaint Status Resolution", "Warden marks complaint Solved", "Status updates to 'Solved' in DB", "Pass"],
        ["TC17", "Fee Payment & Receipt", "Click 'Pay' on monthly rent due", "Status becomes Paid; receipt issued", "Pass"],
        ["TC18", "Dining Meal Star Rating", "Rate Thursday lunch 5 stars", "Feedback committed to `mess_feedback`", "Pass"],
        ["TC19", "Admin Student Enrollment", "Add new student Ananya (A-105)", "Enrolled in `users`; rent account created", "Pass"],
        ["TC20", "CSV Ledger & Backup Export", "Click 'Export Ledger' & Backup", "CSV downloaded; backup `.db` created", "Pass"]
    ]
    format_table([0.7, 1.8, 1.7, 1.8, 0.6], ["Test ID", "Test Objective", "Input / Action", "Expected Result", "Status"], test_cases_data)

    add_h2("7.3 Test Plans and Results")
    test_summary = [
        ["Authentication & Security", "4", "4", "0", "Strict portal separation and rejection verified."],
        ["Resident Gate & Curfew", "5", "5", "0", "Leave approvals, QR pass, and gate toggling verified."],
        ["Attendance Management", "2", "2", "0", "Daily roll-call locking and floor filtering verified."],
        ["Grievances & Dining", "3", "3", "0", "Complaints lifecycle and mess ratings verified."],
        ["Billing & Administration", "4", "4", "0", "Rent receipts, CSV export, and backups verified."],
        ["Multi-Student Profiles", "2", "2", "0", "Distinct data loading across all 9 students verified."],
        ["Total", "20", "20", "0", "100% Test Pass Rate achieved."]
    ]
    format_table([1.8, 1.0, 1.0, 1.0, 1.7], ["Test Category", "Total Cases", "Passed", "Failed", "Operational Remarks"], test_summary)

    add_p("Conclusion of Testing: All 20 functional, integration, and security test cases completed successfully. The application demonstrated zero data corruption, reliable ACID transactions, and robust role isolation.")

    doc.add_page_break()

    # ==========================================
    # CHAPTER 8: CONCLUSION AND FUTURE WORK
    # ==========================================
    add_h1("Chapter 8: Conclusion and Future Work")
    
    add_h2("8.1 Summary of Achievements and Limitations")
    add_p("SafeStay successfully addresses the longstanding vulnerabilities associated with manual hostel administration. By combining Python (Flask), SQLite in WAL mode, and React 18, the system replaces paper registers with an auditable, real-time digital management ecosystem.")
    add_p("Key Achievements:")
    add_bullet("Institutional Safety: ", "Real-time curfew tracking and digital gate clearance eliminate unmonitored resident movements.")
    add_bullet("Administrative Efficiency: ", "Roll-call attendance, fee ledgers, and maintenance tracking cut manual logging time by over 80%.")
    add_bullet("Data Privacy: ", "Strict role-isolated portals ensure students, wardens, and administrators operate within verified boundaries.")
    add_p("Acknowledged Limitations:")
    add_bullet("Hardware Integration: ", "Gate scanning is currently emulated via web modals rather than physical optical turnstile hardware.")
    add_bullet("Offline Redundancy: ", "The platform requires host connectivity; local offline caching on mobile devices is not yet implemented.")

    add_h2("8.2 Suggestions for Improvement")
    add_bullet("Live Camera QR & Turnstile Integration: ", "Integrate HTML5 camera scanning and physical RFID card turnstiles at the hostel entrance.")
    add_bullet("Automated Parent SMS/WhatsApp Gateway: ", "Connect Twilio or WhatsApp Business APIs to dispatch automated departure and late-curfew alerts to guardians.")
    add_bullet("Smart Dining Meal-Skip Rebates: ", "Allow residents to signal meal skips in advance to reduce food wastage and earn billing discounts.")
    add_bullet("Interactive Bed Map: ", "Develop visual drag-and-drop floor maps for room allocation and vacancy inspection.")

    doc.add_page_break()

    # ==========================================
    # CHAPTER 9: REFERENCES
    # ==========================================
    add_h1("Chapter 9: References")
    
    add_h2("9.1 Books, Websites, Tools, APIs Used")
    add_bullet("Flask Documentation: ", "https://flask.palletsprojects.com/")
    add_bullet("SQLite WAL & Documentation: ", "https://www.sqlite.org/wal.html")
    add_bullet("React Official Documentation: ", "https://react.dev/")
    add_bullet("Flask-CORS Extension: ", "https://flask-cors.readthedocs.io/")
    add_bullet("Python-Docx Library: ", "https://python-docx.readthedocs.io/")
    add_bullet("Google Fonts (Fraunces & Plus Jakarta Sans): ", "https://fonts.google.com/")
    add_bullet("MDN Web Docs (Fetch API & LocalStorage): ", "https://developer.mozilla.org/")
    add_bullet("W3C Web Content Accessibility Guidelines (WCAG): ", "https://www.w3.org/WAI/standards-guidelines/wcag/")
    add_bullet("OWASP Top 10 Web Application Security Risks: ", "https://owasp.org/www-project-top-ten/")
    add_bullet("University of Mumbai Academic Project Guidelines: ", "https://mu.ac.in/")

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SafeStay_Smart_Women_Hostel_Project_Report.docx")
    doc.save(output_path)
    print(f"Document successfully created at: {output_path}")

if __name__ == "__main__":
    create_safestay_report()
