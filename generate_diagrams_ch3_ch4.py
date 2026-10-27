"""
Generates Chapter 3 and Chapter 4 diagrams for the SafeStay Project Report.
Uses matplotlib to produce clean, high-resolution academic engineering diagrams.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUT_DIR = "report_figures"
os.makedirs(OUT_DIR, exist_ok=True)

def setup_ax(w=10, h=6, bg='#F8FAFC'):
    fig, ax = plt.subplots(figsize=(w, h), dpi=150)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    return fig, ax

def draw_card(ax, x, y, w, h, title="", subtitle="", color="#FFFFFF", border="#2A1F3D", title_color="#2A1F3D", lw=1.5, radius=0.15):
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad={radius}",
                                facecolor=color, edgecolor=border, linewidth=lw)
    ax.add_patch(box)
    if title:
        ty = y + h - 0.35 if subtitle else y + h/2
        ax.text(x + w/2, ty, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color=title_color)
    if subtitle:
        ax.text(x + w/2, y + 0.35, subtitle, ha='center', va='center', fontsize=8, color='#475569')

def draw_arrow(ax, x1, y1, x2, y2, label="", color="#4A3567", style='-|>', lw=1.5, rad=0.0, ls='-'):
    arrow = patches.FancyArrowPatch((x1, y1), (x2, y2),
                                   arrowstyle=style, mutation_scale=12,
                                   color=color, linewidth=lw, linestyle=ls,
                                   connectionstyle=f"arc3,rad={rad}")
    ax.add_patch(arrow)
    if label:
        mx = (x1 + x2)/2
        my = (y1 + y2)/2 + 0.18
        ax.text(mx, my, label, ha='center', va='center', fontsize=7.5, color='#1E293B',
                bbox=dict(boxstyle='square,pad=0.1', facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=0.5))

def draw_oval(ax, x, y, rx, ry, title="", color="#FEF3C7", border="#D97706", lw=1.5):
    ellipse = patches.Ellipse((x, y), rx*2, ry*2, facecolor=color, edgecolor=border, linewidth=lw)
    ax.add_patch(ellipse)
    if title:
        ax.text(x, y, title, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#78350F')

# ==========================================
# 1. Gantt Chart (Fig 3.1)
# ==========================================
def gen_fig3_1_gantt():
    fig, ax = plt.subplots(figsize=(10.5, 5.5), dpi=150)
    ax.set_facecolor('#FFFFFF')
    
    tasks = [
        "1. Problem Definition & Needs Assessment",
        "2. Literature Survey & Tech Analysis",
        "3. SRS & Feasibility Study",
        "4. Database Schema & Architecture Design",
        "5. Backend API & Auth Engine Development",
        "6. Frontend UI/UX (React & Tailwind)",
        "7. QR Scanner & Curfew Pass Module",
        "8. Security Hardening & Role Isolation",
        "9. Integration & Multi-User Verification",
        "10. UAT, Performance & Security Testing",
        "11. Documentation & Thesis Preparation"
    ]
    starts = [1, 2, 4, 6, 8, 11, 14, 16, 18, 20, 21]
    durations = [2, 3, 3, 3, 5, 5, 3, 3, 3, 3, 4]
    colors = ['#4A3567', '#6366F1', '#3B82F6', '#0284C7', '#0D9488', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899', '#2A1F3D']
    
    y_pos = range(len(tasks))
    ax.barh(y_pos, durations, left=starts, height=0.55, color=colors, edgecolor='#1E293B', linewidth=0.8, alpha=0.9)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(tasks, fontsize=8.5, fontweight='bold', color='#1E293B')
    ax.invert_yaxis()
    ax.set_xlabel('Project Schedule (Weeks 1 to 24 - Academic Year 2026-2027)', fontsize=9.5, fontweight='bold', color='#2A1F3D')
    ax.set_xlim(0, 25)
    ax.set_xticks(range(1, 25))
    ax.grid(axis='x', linestyle='--', alpha=0.5, color='#94A3B8')
    
    # Milestone marker
    ax.axvline(x=12, color='#DC2626', linestyle=':', linewidth=1.5)
    ax.text(12.2, 0.2, 'Mid-Term Review', color='#DC2626', fontsize=8, fontweight='bold')
    ax.axvline(x=24, color='#16A34A', linestyle=':', linewidth=1.5)
    ax.text(22.2, 10.5, 'Final Delivery', color='#16A34A', fontsize=8, fontweight='bold')
    
    plt.title('Figure 3.1: SafeStay Project Work Breakdown & Implementation Schedule (Gantt Chart)', fontsize=11, fontweight='bold', pad=14, color='#2A1F3D')
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig3_1_gantt.png", bbox_inches='tight')
    plt.close()

# ==========================================
# 2. System Architecture (Fig 4.1)
# ==========================================
def gen_fig4_1_architecture():
    fig, ax = setup_ax(10, 6)
    
    # Title
    ax.text(5, 5.7, "Figure 4.1: SafeStay 3-Tier Enterprise System Architecture", ha='center', fontsize=11, fontweight='bold', color='#2A1F3D')
    
    # Tier 1: Presentation Tier
    draw_card(ax, 0.5, 3.8, 9, 1.6, title="TIER 1: PRESENTATION TIER (CLIENT BROWSER SPA)", subtitle="", color="#F8FAFC", border="#6366F1", title_color="#312E81", lw=1.8)
    draw_card(ax, 0.8, 4.0, 2.6, 1.0, title="Student Portal", subtitle="React 18 SPA • QR Code • Pass UI", color="#EEF2FF", border="#818CF8", title_color="#3730A3")
    draw_card(ax, 3.7, 4.0, 2.6, 1.0, title="Warden Portal", subtitle="Roll Call • QR Scanner • Grievance", color="#EEF2FF", border="#818CF8", title_color="#3730A3")
    draw_card(ax, 6.6, 4.0, 2.6, 1.0, title="Admin Portal", subtitle="Roster • Ledger • Audit Logs • Export", color="#EEF2FF", border="#818CF8", title_color="#3730A3")
    
    # Connectors Tier 1 to 2
    draw_arrow(ax, 2.1, 3.8, 2.1, 3.0, "HTTPS / JSON REST", "#4F46E5", lw=1.5)
    draw_arrow(ax, 5.0, 3.8, 5.0, 3.0, "REST API Endpoints", "#4F46E5", lw=1.5)
    draw_arrow(ax, 7.9, 3.8, 7.9, 3.0, "Stateful Session Tokens", "#4F46E5", lw=1.5)
    
    # Tier 2: Application Tier
    draw_card(ax, 0.5, 1.8, 9, 1.2, title="TIER 2: APPLICATION CONTROLLER TIER (PYTHON FLASK REST BACKEND)", subtitle="", color="#F1F5F9", border="#0D9488", title_color="#134E4A", lw=1.8)
    draw_card(ax, 0.8, 1.95, 1.9, 0.75, title="Auth & RBAC", subtitle="SHA-256 / Session", color="#F0FDFA", border="#5EEAD4", title_color="#042F2E")
    draw_card(ax, 2.9, 1.95, 1.9, 0.75, title="Curfew & Gate", subtitle="Passes & Scanning", color="#F0FDFA", border="#5EEAD4", title_color="#042F2E")
    draw_card(ax, 5.0, 1.95, 1.9, 0.75, title="Fee & Ledger", subtitle="Invoices & Reports", color="#F0FDFA", border="#5EEAD4", title_color="#042F2E")
    draw_card(ax, 7.1, 1.95, 2.1, 0.75, title="Audit & Incident", subtitle="Disaster Recovery", color="#F0FDFA", border="#5EEAD4", title_color="#042F2E")
    
    # Connectors Tier 2 to 3
    draw_arrow(ax, 3.5, 1.8, 3.5, 1.1, "PRAGMA WAL Queries", "#0D9488", lw=1.5)
    draw_arrow(ax, 6.5, 1.8, 6.5, 1.1, "Atomic Transactions", "#0D9488", lw=1.5)
    
    # Tier 3: Data Tier
    draw_card(ax, 0.5, 0.2, 9, 0.9, title="TIER 3: DATA PERSISTENCE TIER (SQLITE 3 WITH WRITE-AHEAD LOGGING)", subtitle="", color="#FEF2F2", border="#EF4444", title_color="#991B1B", lw=1.8)
    draw_card(ax, 0.8, 0.3, 2.6, 0.6, title="Relational Tables", subtitle="Users, Attendance, Fees", color="#FFFFFF", border="#FCA5A5", title_color="#7F1D1D")
    draw_card(ax, 3.7, 0.3, 2.6, 0.6, title="ACID Engine & Indexes", subtitle="Foreign Keys • Timeout=20s", color="#FFFFFF", border="#FCA5A5", title_color="#7F1D1D")
    draw_card(ax, 6.6, 0.3, 2.6, 0.6, title="Automated Snapshots", subtitle="Online Backup API", color="#FFFFFF", border="#FCA5A5", title_color="#7F1D1D")
    
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig4_1_architecture.png", bbox_inches='tight')
    plt.close()

# ==========================================
# 3. DFD Level 0 (Fig 4.2)
# ==========================================
def gen_fig4_2_dfd0():
    fig, ax = setup_ax(10, 6)
    ax.text(5, 5.7, "Figure 4.2: Data Flow Diagram (DFD) Level 0 - Context Diagram", ha='center', fontsize=11, fontweight='bold', color='#2A1F3D')
    
    # Central Process
    draw_card(ax, 3.6, 2.2, 2.8, 1.8, title="0.0\nSAFESTAY SMART\nHOSTEL SYSTEM", subtitle="Central Automated Hub", color="#2A1F3D", border="#C5A880", title_color="#FFFFFF", lw=2)
    
    # External Entities
    draw_card(ax, 0.4, 3.8, 2.0, 1.2, title="STUDENT\n(RESIDENT)", subtitle="Hostel Resident", color="#EFF6FF", border="#3B82F6", title_color="#1E3A8A")
    draw_card(ax, 0.4, 1.0, 2.0, 1.2, title="PARENT /\nGUARDIAN", subtitle="Next of Kin", color="#F0FDF4", border="#22C55E", title_color="#14532D")
    draw_card(ax, 7.6, 3.8, 2.0, 1.2, title="WARDEN\n(OPERATOR)", subtitle="Security & Discipline", color="#FEF3C7", border="#F59E0B", title_color="#78350F")
    draw_card(ax, 7.6, 1.0, 2.0, 1.2, title="ADMINISTRATOR", subtitle="Hostel Director", color="#FDF2F8", border="#EC4899", title_color="#831843")
    
    # Data flows
    draw_arrow(ax, 2.4, 4.6, 3.6, 3.6, "Gate Pass Req / Grievance", "#3B82F6")
    draw_arrow(ax, 3.6, 3.2, 2.4, 4.0, "Pass QR / Rent Invoices", "#3B82F6")
    
    draw_arrow(ax, 2.4, 1.6, 3.6, 2.4, "Emergency Contact Acknowledgment", "#22C55E")
    draw_arrow(ax, 3.6, 2.3, 2.4, 1.2, "SMS Gate Alerts / SOS Notice", "#22C55E")
    
    draw_arrow(ax, 7.6, 4.6, 6.4, 3.6, "Roll Call / Verification Scan", "#F59E0B")
    draw_arrow(ax, 6.4, 3.2, 7.6, 4.0, "Curfew Roster / Alert Triggers", "#F59E0B")
    
    draw_arrow(ax, 7.6, 1.6, 6.4, 2.4, "Config / Fee Schedule / Roster", "#EC4899")
    draw_arrow(ax, 6.4, 2.3, 7.6, 1.2, "Audit Trails / CSV Ledgers", "#EC4899")
    
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig4_2_dfd0.png", bbox_inches='tight')
    plt.close()

# ==========================================
# 4. DFD Level 1 (Fig 4.3)
# ==========================================
def gen_fig4_3_dfd1():
    fig, ax = setup_ax(10.5, 6.5)
    ax.text(5.25, 6.2, "Figure 4.3: Data Flow Diagram (DFD) Level 1 - Detailed Functional System Flow", ha='center', fontsize=11, fontweight='bold', color='#2A1F3D')
    
    # Processes
    draw_card(ax, 1.0, 4.8, 1.9, 0.9, title="1.0 Authentication", subtitle="Validate Credentials", color="#F1F5F9", border="#475569", title_color="#0F172A")
    draw_card(ax, 4.3, 4.8, 1.9, 0.9, title="2.0 Room Allocation", subtitle="Assign Beds & Wings", color="#F1F5F9", border="#475569", title_color="#0F172A")
    draw_card(ax, 7.6, 4.8, 1.9, 0.9, title="3.0 Gate Pass & Curfew", subtitle="QR Token & Scanner", color="#F1F5F9", border="#475569", title_color="#0F172A")
    
    draw_card(ax, 1.0, 2.0, 1.9, 0.9, title="4.0 Grievance Redressal", subtitle="Triage Complaints", color="#F1F5F9", border="#475569", title_color="#0F172A")
    draw_card(ax, 4.3, 2.0, 1.9, 0.9, title="5.0 Billing & Ledger", subtitle="Fee Records & Dues", color="#F1F5F9", border="#475569", title_color="#0F172A")
    draw_card(ax, 7.6, 2.0, 1.9, 0.9, title="6.0 Audit & Emergency", subtitle="SOS & Safety Alerts", color="#F1F5F9", border="#475569", title_color="#0F172A")
    
    # Data Stores (Open-ended boxes)
    def draw_datastore(x, y, w, h, name):
        ax.plot([x, x+w], [y, y], color='#2563EB', lw=2)
        ax.plot([x, x+w], [y+h, y+h], color='#2563EB', lw=2)
        ax.plot([x, x], [y, y+h], color='#2563EB', lw=2)
        ax.fill_between([x, x+w], y, y+h, color='#EFF6FF', alpha=0.9)
        ax.text(x+w/2, y+h/2, name, ha='center', va='center', fontsize=8, fontweight='bold', color='#1E40AF')
        
    draw_datastore(1.0, 3.4, 1.9, 0.6, "D1: Users Table")
    draw_datastore(4.3, 3.4, 1.9, 0.6, "D2: Rooms & Beds")
    draw_datastore(7.6, 3.4, 1.9, 0.6, "D3: Passes & Attendance")
    draw_datastore(2.6, 0.5, 2.2, 0.6, "D4: Grievance Logs")
    draw_datastore(5.8, 0.5, 2.2, 0.6, "D5: Financial Ledgers")
    
    # Flows
    draw_arrow(ax, 1.95, 4.8, 1.95, 4.0, "Session", "#2563EB")
    draw_arrow(ax, 5.25, 4.8, 5.25, 4.0, "Assign Bed", "#2563EB")
    draw_arrow(ax, 8.55, 4.8, 8.55, 4.0, "Log Scan", "#2563EB")
    draw_arrow(ax, 1.95, 2.0, 3.0, 1.1, "Lodge", "#2563EB")
    draw_arrow(ax, 5.25, 2.0, 6.2, 1.1, "Invoices", "#2563EB")
    
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig4_3_dfd1.png", bbox_inches='tight')
    plt.close()

# ==========================================
# 5. DFD Level 2 (Fig 4.4)
# ==========================================
def gen_fig4_4_dfd2():
    fig, ax = setup_ax(10, 6)
    ax.text(5, 5.7, "Figure 4.4: DFD Level 2 - Gate Pass & Curfew Verification Subsystem", ha='center', fontsize=11, fontweight='bold', color='#2A1F3D')
    
    draw_card(ax, 0.5, 3.8, 1.8, 1.2, "Student Resident", "Submits Request", "#EFF6FF", "#3B82F6", "#1E3A8A")
    draw_card(ax, 3.0, 4.0, 1.8, 0.9, "3.1 Request Intake", "Check Eligibility", "#F8FAFC", "#475569", "#0F172A")
    draw_card(ax, 5.4, 4.0, 1.8, 0.9, "3.2 Warden Review", "Verify Curfew & Reason", "#F8FAFC", "#475569", "#0F172A")
    draw_card(ax, 7.7, 4.0, 1.8, 0.9, "3.3 QR Encoding", "Sign JSON Token", "#F8FAFC", "#475569", "#0F172A")
    
    draw_card(ax, 7.7, 1.8, 1.8, 0.9, "3.4 Optical Scan", "Guard Terminal", "#F8FAFC", "#475569", "#0F172A")
    draw_card(ax, 4.5, 1.8, 2.2, 0.9, "3.5 Curfew Violation Engine", "Compare Entry vs Curfew", "#F8FAFC", "#EF4444", "#991B1B")
    draw_card(ax, 1.0, 1.8, 2.2, 0.9, "3.6 Register & SMS", "Mark Late / Alert Warden", "#FEF2F2", "#EF4444", "#991B1B")
    
    # Arrows
    draw_arrow(ax, 2.3, 4.45, 3.0, 4.45, "Pass Form", "#3B82F6")
    draw_arrow(ax, 4.8, 4.45, 5.4, 4.45, "Pending Record", "#475569")
    draw_arrow(ax, 7.2, 4.45, 7.7, 4.45, "Approve", "#475569")
    draw_arrow(ax, 8.6, 4.0, 8.6, 2.7, "Dynamic QR Image", "#10B981")
    draw_arrow(ax, 7.7, 2.25, 6.7, 2.25, "Decoded Timestamp", "#475569")
    draw_arrow(ax, 4.5, 2.25, 3.2, 2.25, "Curfew Breach", "#DC2626")
    
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig4_4_dfd2.png", bbox_inches='tight')
    plt.close()

# ==========================================
# 6. System Flowchart (Fig 4.5)
# ==========================================
def gen_fig4_5_flowchart():
    fig, ax = setup_ax(10, 6.5)
    ax.text(5, 6.2, "Figure 4.5: SafeStay Complete Operational Flowchart", ha='center', fontsize=11, fontweight='bold', color='#2A1F3D')
    
    # Start
    draw_oval(ax, 5, 5.6, 0.8, 0.35, "START", "#DCFCE7", "#16A34A")
    draw_arrow(ax, 5, 5.25, 5, 4.8, "", "#475569")
    
    # Login Decision
    draw_card(ax, 3.8, 4.1, 2.4, 0.7, "Login & Role Verify", "SHA-256 Auth", "#F8FAFC", "#2A1F3D", "#2A1F3D")
    draw_arrow(ax, 5, 4.1, 5, 3.4, "", "#475569")
    
    # Role Fork
    draw_card(ax, 0.8, 2.4, 2.4, 0.9, "STUDENT ROUTE", "Passes • Invoices • SOS\nGrievances • Mess Menu", "#EFF6FF", "#3B82F6", "#1E3A8A")
    draw_card(ax, 3.8, 2.4, 2.4, 0.9, "WARDEN ROUTE", "Roll Call • QR Gate Scan\nPass Approval • Triage", "#FEF3C7", "#D97706", "#78350F")
    draw_card(ax, 6.8, 2.4, 2.4, 0.9, "ADMIN ROUTE", "Roster Mgt • Ledger Audit\nReports CSV • System Config", "#FDF2F8", "#DB2777", "#831843")
    
    draw_arrow(ax, 4.2, 3.4, 2.0, 3.3, "Role = Student", "#3B82F6")
    draw_arrow(ax, 5.0, 3.4, 5.0, 3.3, "Role = Warden", "#D97706")
    draw_arrow(ax, 5.8, 3.4, 8.0, 3.3, "Role = Admin", "#DB2777")
    
    # Aggregation
    draw_card(ax, 3.5, 1.1, 3.0, 0.7, "Audit Log & State Commit", "SQLite WAL Write", "#F1F5F9", "#0F172A", "#0F172A")
    draw_arrow(ax, 2.0, 2.4, 4.0, 1.8, "Action Log", "#475569")
    draw_arrow(ax, 5.0, 2.4, 5.0, 1.8, "Action Log", "#475569")
    draw_arrow(ax, 8.0, 2.4, 6.0, 1.8, "Action Log", "#475569")
    
    # End
    draw_oval(ax, 5, 0.4, 0.8, 0.3, "END SESSION", "#FEE2E2", "#DC2626")
    draw_arrow(ax, 5, 1.1, 5, 0.7, "Logout", "#DC2626")
    
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig4_5_flowchart.png", bbox_inches='tight')
    plt.close()

# ==========================================
# 7. ER Diagram (Fig 4.6)
# ==========================================
def gen_fig4_6_erd():
    fig, ax = setup_ax(10.5, 6.5)
    ax.text(5.25, 6.2, "Figure 4.6: SafeStay Relational Entity-Relationship Diagram (ERD)", ha='center', fontsize=11, fontweight='bold', color='#2A1F3D')
    
    # Entities
    def draw_entity(x, y, w, h, name, attrs):
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                                    facecolor="#FFFFFF", edgecolor="#1E293B", linewidth=1.5)
        ax.add_patch(box)
        # Header
        hdr = patches.Rectangle((x, y+h-0.35), w, 0.35, facecolor="#2A1F3D", edgecolor="#1E293B", linewidth=1)
        ax.add_patch(hdr)
        ax.text(x+w/2, y+h-0.18, name, ha='center', va='center', fontsize=8, fontweight='bold', color='#FFFFFF')
        # Attributes
        ay = y + h - 0.55
        for a in attrs:
            ax.text(x+0.1, ay, a, ha='left', va='center', fontsize=6.8, color='#334155')
            ay -= 0.18

    draw_entity(0.5, 3.8, 2.0, 1.8, "USERS", ["PK id (INTEGER)", "username (VARCHAR)", "password_hash (VARCHAR)", "role (VARCHAR)", "full_name (VARCHAR)", "status (VARCHAR)"])
    draw_entity(3.1, 3.8, 2.1, 1.8, "STUDENTS", ["PK id (INTEGER)", "FK user_id (INT)", "roll_no (VARCHAR)", "phone (VARCHAR)", "parent_phone (VARCHAR)", "FK room_id (INT)"])
    draw_entity(5.8, 3.8, 2.0, 1.8, "ROOMS", ["PK id (INTEGER)", "room_number (VARCHAR)", "wing (VARCHAR)", "capacity (INTEGER)", "occupied (INTEGER)", "monthly_fee (FLOAT)"])
    draw_entity(8.2, 3.8, 2.0, 1.8, "GATE_PASSES", ["PK id (INTEGER)", "FK student_id (INT)", "reason (TEXT)", "out_time (DATETIME)", "in_time (DATETIME)", "status (VARCHAR)"])
    
    draw_entity(0.5, 0.6, 2.0, 1.8, "ATTENDANCE", ["PK id (INTEGER)", "FK student_id (INT)", "date (DATE)", "status (VARCHAR)", "marked_by (VARCHAR)", "timestamp (DATETIME)"])
    draw_entity(3.1, 0.6, 2.1, 1.8, "COMPLAINTS", ["PK id (INTEGER)", "FK student_id (INT)", "category (VARCHAR)", "title (VARCHAR)", "status (VARCHAR)", "created_at (DATETIME)"])
    draw_entity(5.8, 0.6, 2.0, 1.8, "PAYMENTS", ["PK id (INTEGER)", "FK student_id (INT)", "month (VARCHAR)", "amount (FLOAT)", "status (VARCHAR)", "receipt_no (VARCHAR)"])
    draw_entity(8.2, 0.6, 2.0, 1.8, "AUDIT_LOGS", ["PK id (INTEGER)", "user_id (INTEGER)", "action (VARCHAR)", "details (TEXT)", "ip_address (VARCHAR)", "timestamp (DATETIME)"])
    
    # Relationships
    draw_arrow(ax, 2.5, 4.7, 3.1, 4.7, "1:1", "#475569")
    draw_arrow(ax, 5.2, 4.7, 5.8, 4.7, "N:1", "#475569")
    draw_arrow(ax, 5.2, 4.4, 8.2, 4.4, "1:N", "#475569", rad=0.2)
    draw_arrow(ax, 3.8, 3.8, 1.5, 2.4, "1:N", "#475569")
    draw_arrow(ax, 4.15, 3.8, 4.15, 2.4, "1:N", "#475569")
    draw_arrow(ax, 4.8, 3.8, 6.8, 2.4, "1:N", "#475569")
    
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig4_6_erd.png", bbox_inches='tight')
    plt.close()

# ==========================================
# 8. UML Class Diagram (Fig 4.7)
# ==========================================
def gen_fig4_7_class():
    fig, ax = setup_ax(10.5, 6.5)
    ax.text(5.25, 6.2, "Figure 4.7: SafeStay UML Class Diagram", ha='center', fontsize=11, fontweight='bold', color='#2A1F3D')
    
    def draw_uml_class(x, y, w, h, name, attrs, methods):
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0",
                                    facecolor="#FFFFFF", edgecolor="#2A1F3D", linewidth=1.5)
        ax.add_patch(box)
        # Class Header
        hdr = patches.Rectangle((x, y+h-0.35), w, 0.35, facecolor="#EDE9FE", edgecolor="#2A1F3D", linewidth=1)
        ax.add_patch(hdr)
        ax.text(x+w/2, y+h-0.18, name, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#4C1D95')
        
        # Attributes
        ay = y + h - 0.52
        for a in attrs:
            ax.text(x+0.08, ay, a, ha='left', va='center', fontsize=6.8, color='#0F172A')
            ay -= 0.16
            
        # Divider line
        div_y = y + len(methods)*0.16 + 0.15
        ax.plot([x, x+w], [div_y, div_y], color='#2A1F3D', lw=1)
        
        # Methods
        my = div_y - 0.14
        for m in methods:
            ax.text(x+0.08, my, m, ha='left', va='center', fontsize=6.8, color='#047857')
            my -= 0.16

    draw_uml_class(0.5, 3.5, 2.6, 2.3, "User",
                   ["- id: int", "- username: str", "- password_hash: str", "- role: RoleEnum", "- active: bool"],
                   ["+ login(pwd): bool", "+ change_password(): void", "+ get_role(): RoleEnum", "+ logout(): void"])
                   
    draw_uml_class(3.8, 3.5, 2.8, 2.3, "StudentResident",
                   ["- roll_no: str", "- room_id: int", "- parent_phone: str", "- cur_status: str"],
                   ["+ apply_gatepass(reason): Pass", "+ lodge_complaint(): void", "+ pay_dues(amt): Receipt", "+ trigger_sos(): void"])
                   
    draw_uml_class(7.3, 3.5, 2.7, 2.3, "GatePass",
                   ["- pass_id: int", "- token_hash: str", "- out_time: DateTime", "- curfew_time: DateTime", "- status: PassStatus"],
                   ["+ generate_qr(): Image", "+ verify_scan(guard): bool", "+ check_curfew_late(): bool", "+ approve(warden): void"])
                   
    draw_uml_class(0.5, 0.6, 2.6, 2.4, "AttendanceRecord",
                   ["- record_id: int", "- student_id: int", "- date: Date", "- curfew_status: str", "- timestamp: DateTime"],
                   ["+ mark_roll_call(status): void", "+ flag_unauthorized(): void", "+ get_monthly_pct(): float"])
                   
    draw_uml_class(3.8, 0.6, 2.8, 2.4, "Complaint",
                   ["- ticket_no: str", "- category: CategoryEnum", "- desc: str", "- resolution: str", "- status: TicketStatus"],
                   ["+ escalate(warden): void", "+ resolve(notes): void", "+ reopen(): void", "+ get_timeline(): List"])
                   
    draw_uml_class(7.3, 0.6, 2.7, 2.4, "BillingInvoice",
                   ["- invoice_no: str", "- student_id: int", "- amount: float", "- due_date: Date", "- paid_date: Date"],
                   ["+ generate_invoice(): void", "+ record_receipt(): str", "+ export_ledger_csv(): File", "+ send_due_notice(): void"])
                   
    # Class Inherit / Assoc lines
    draw_arrow(ax, 3.1, 4.6, 3.8, 4.6, "inherits", "#6D28D9", style='-|>')
    draw_arrow(ax, 6.6, 4.6, 7.3, 4.6, "requests 1..*", "#1E293B", style='->')
    draw_arrow(ax, 1.8, 3.5, 1.8, 3.0, "has", "#1E293B", style='->')
    draw_arrow(ax, 5.2, 3.5, 5.2, 3.0, "lodges 0..*", "#1E293B", style='->')
    draw_arrow(ax, 8.6, 3.5, 8.6, 3.0, "billed to", "#1E293B", style='->')

    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig4_7_class.png", bbox_inches='tight')
    plt.close()

# ==========================================
# 9. Sequence Diagrams (Figs 4.8, 4.9, 4.10)
# ==========================================
def gen_fig4_8_seq_gate():
    fig, ax = setup_ax(10, 6)
    ax.text(5, 5.7, "Figure 4.8: UML Sequence Diagram - Curfew Gate Pass & Optical QR Verification", ha='center', fontsize=11, fontweight='bold', color='#2A1F3D')
    
    # Lifelines
    actors = ["Resident Student", "Frontend Portal", "REST Controller", "Database (WAL)", "Warden / Guard"]
    xs = [1.0, 3.0, 5.0, 7.0, 9.0]
    for x, act in zip(xs, actors):
        draw_card(ax, x-0.8, 4.8, 1.6, 0.6, act, "", "#EDE9FE", "#6D28D9", "#4C1D95")
        ax.plot([x, x], [4.8, 0.5], color='#94A3B8', linestyle='--', lw=1.2)
        
    # Sequence steps
    steps = [
        (1.0, 3.0, 4.4, "1: Fill Gate Pass Form & Reason", False),
        (3.0, 5.0, 4.0, "2: POST /api/student/gatepass", False),
        (5.0, 7.0, 3.6, "3: INSERT into gate_passes (PENDING)", False),
        (7.0, 5.0, 3.3, "4: Pass Created Confirmation", True),
        (5.0, 9.0, 2.9, "5: Notify Warden Dashboard", False),
        (9.0, 5.0, 2.5, "6: PUT /api/warden/gatepass/approve", False),
        (5.0, 3.0, 2.1, "7: Return Signed QR Token Payload", True),
        (3.0, 1.0, 1.7, "8: Render Dynamic QR Code on Phone", True),
        (1.0, 9.0, 1.3, "9: Present Optical QR at Hostel Gate", False),
        (9.0, 5.0, 0.9, "10: Scan & Check Curfew Timestamps", False),
    ]
    for x1, x2, y, txt, is_ret in steps:
        ls = '--' if is_ret else '-'
        col = '#059669' if is_ret else '#2563EB'
        draw_arrow(ax, x1, y, x2, y, txt, col, style='-|>', lw=1.3, ls=ls)
        
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig4_8_seq_gate.png", bbox_inches='tight')
    plt.close()

def gen_fig4_9_seq_complaint():
    fig, ax = setup_ax(10, 5.5)
    ax.text(5, 5.2, "Figure 4.9: UML Sequence Diagram - Resident Grievance Lifecycle", ha='center', fontsize=11, fontweight='bold', color='#2A1F3D')
    
    actors = ["Resident Student", "Student UI", "Flask Grievance API", "Database", "Hostel Warden"]
    xs = [1.0, 3.0, 5.0, 7.0, 9.0]
    for x, act in zip(xs, actors):
        draw_card(ax, x-0.8, 4.3, 1.6, 0.6, act, "", "#FEF3C7", "#D97706", "#78350F")
        ax.plot([x, x], [4.3, 0.5], color='#94A3B8', linestyle='--', lw=1.2)
        
    steps = [
        (1.0, 3.0, 3.9, "1: Submit Complaint (Room/Mess/WiFi)", False),
        (3.0, 5.0, 3.4, "2: POST /api/student/complaints", False),
        (5.0, 7.0, 2.9, "3: INSERT into complaints (Status: Open)", False),
        (5.0, 9.0, 2.4, "4: Alert Warden Dashboard Notification", False),
        (9.0, 5.0, 1.9, "5: Assign to Maintenance Technician", False),
        (5.0, 7.0, 1.4, "6: UPDATE status='Resolved', notes='Fixed'", False),
        (5.0, 1.0, 0.9, "7: Push SMS / In-App Resolution Notice", True)
    ]
    for x1, x2, y, txt, is_ret in steps:
        ls = '--' if is_ret else '-'
        draw_arrow(ax, x1, y, x2, y, txt, '#D97706', style='-|>', lw=1.3, ls=ls)
        
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig4_9_seq_complaint.png", bbox_inches='tight')
    plt.close()

def gen_fig4_10_seq_payment():
    fig, ax = setup_ax(10, 5.5)
    ax.text(5, 5.2, "Figure 4.10: UML Sequence Diagram - Digital Rent Billing & Verification", ha='center', fontsize=11, fontweight='bold', color='#2A1F3D')
    
    actors = ["Resident Student", "Billing UI", "Payment Controller", "DB Ledger", "Hostel Admin"]
    xs = [1.0, 3.0, 5.0, 7.0, 9.0]
    for x, act in zip(xs, actors):
        draw_card(ax, x-0.8, 4.3, 1.6, 0.6, act, "", "#F0FDF4", "#16A34A", "#14532D")
        ax.plot([x, x], [4.3, 0.5], color='#94A3B8', linestyle='--', lw=1.2)
        
    steps = [
        (9.0, 5.0, 3.9, "1: POST /api/admin/invoices/generate (Batch Monthly)", False),
        (5.0, 7.0, 3.4, "2: INSERT dues for all enrolled residents", False),
        (1.0, 3.0, 2.9, "3: View Monthly Fee Breakdown & Due Date", False),
        (3.0, 5.0, 2.4, "4: POST /api/student/pay (Mock UPI/Card Engine)", False),
        (5.0, 7.0, 1.9, "5: UPDATE payment status='Paid', rec_no='REC-948'", False),
        (5.0, 3.0, 1.4, "6: Return Digital Receipt PDF/HTML", True),
        (9.0, 5.0, 0.9, "7: Real-time Reconciliation in Executive Ledger", False)
    ]
    for x1, x2, y, txt, is_ret in steps:
        ls = '--' if is_ret else '-'
        draw_arrow(ax, x1, y, x2, y, txt, '#16A34A', style='-|>', lw=1.3, ls=ls)
        
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig4_10_seq_payment.png", bbox_inches='tight')
    plt.close()

# ==========================================
# 10. Main System Use Case (Fig 4.11)
# ==========================================
def gen_fig4_11_usecase_main():
    fig, ax = setup_ax(10.5, 7.0)
    ax.text(5.25, 6.7, "Figure 4.11: SafeStay Overall System Use Case Diagram", ha='center', fontsize=11, fontweight='bold', color='#2A1F3D')
    
    # Boundary box
    box = patches.FancyBboxPatch((2.2, 0.4), 6.1, 5.9, boxstyle="square,pad=0.1",
                                facecolor="#FFFFFF", edgecolor="#2A1F3D", linewidth=1.8)
    ax.add_patch(box)
    ax.text(5.25, 6.05, "SafeStay Hostel Automation Boundary", ha='center', fontsize=9, fontweight='bold', color='#4A3567')
    
    # Actors
    def draw_actor(x, y, name):
        ax.plot(x, y+0.4, 'o', markersize=14, color='#2A1F3D')
        ax.plot([x, x], [y+0.25, y-0.2], color='#2A1F3D', lw=2)
        ax.plot([x-0.25, x+0.25], [y+0.1, y+0.1], color='#2A1F3D', lw=2)
        ax.plot([x, x-0.2], [y-0.2, y-0.5], color='#2A1F3D', lw=2)
        ax.plot([x, x+0.2], [y-0.2, y-0.5], color='#2A1F3D', lw=2)
        ax.text(x, y-0.75, name, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#2A1F3D')
        
    draw_actor(1.0, 4.4, "Student Resident")
    draw_actor(1.0, 1.8, "Hostel Warden")
    draw_actor(9.5, 3.2, "Administrator")
    
    # Use cases
    ucs = [
        (3.6, 5.5, "UC01: Authenticate & Role Verify"),
        (6.8, 5.5, "UC02: Profile & Room Info"),
        (3.6, 4.6, "UC03: Apply & View Gate Pass QR"),
        (6.8, 4.6, "UC04: Real-time Roll Call Register"),
        (3.6, 3.7, "UC05: Lodge Grievance / Complaint"),
        (6.8, 3.7, "UC06: Pay Rent & Mess Fees"),
        (3.6, 2.8, "UC07: Check Mess Menu Schedule"),
        (6.8, 2.8, "UC08: Emergency SOS Broadcasting"),
        (3.6, 1.9, "UC09: Curfew Breach Audit Alert"),
        (6.8, 1.9, "UC10: Security Log Inspection"),
        (5.2, 1.0, "UC11: Analytical Report & CSV Export")
    ]
    for x, y, title in ucs:
        draw_oval(ax, x, y, 1.3, 0.35, title, color='#F3E8FF', border='#7E22CE', lw=1.2)
        
    # Associations
    # Student connects to UC01, UC02, UC03, UC05, UC06, UC07, UC08
    for uy in [5.5, 4.6, 3.7, 2.8]:
        ax.plot([1.3, 2.3], [4.4, uy], color='#7E22CE', lw=1)
    # Warden connects to UC01, UC03, UC04, UC05, UC07, UC09
    for uy in [5.5, 4.6, 3.7, 1.9]:
        ax.plot([1.3, 2.3], [1.8, uy], color='#D97706', lw=1)
    # Admin connects to all
    for uy in [5.5, 4.6, 3.7, 2.8, 1.9, 1.0]:
        ax.plot([9.2, 8.1], [3.2, uy], color='#2563EB', lw=1)
        
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig4_11_usecase_main.png", bbox_inches='tight')
    plt.close()

# ==========================================
# 11. Individual Use Cases (Figs 4.12 to 4.22)
# ==========================================
def gen_individual_usecases():
    uc_specs = [
        ("fig4_12_uc01.png", "Figure 4.12: UC01 - Secure Role-Based Authentication",
         "Student, Warden, Admin", ["Enter Username & Password", "Validate SHA-256 Hash", "Verify Account Status", "Assign Isolated Portal Route", "Establish Secure Session"]),
        ("fig4_13_uc02.png", "Figure 4.13: UC02 - Student Profile & Room Allocation",
         "Student, Admin", ["Query Student Master Record", "Lookup Wing & Bed Number", "Display Roommate Information", "Update Emergency Guardian Phone", "Validate Bed Capacity"]),
        ("fig4_14_uc03.png", "Figure 4.14: UC03 - Curfew Gate Pass Generation & QR Scanning",
         "Student, Warden, Guard", ["Submit Outstation/Local Pass", "Warden Authorizes Movement", "Generate Encrypted Token", "Render Scalable QR on Device", "Optical Gate Camera Verification"]),
        ("fig4_15_uc04.png", "Figure 4.15: UC04 - Real-Time Attendance Register",
         "Warden, Admin", ["Fetch Today's Roll Call List", "Filter by Wing and Floor", "Mark Present / Absent / On-Leave", "Auto-Check Gate Scan Records", "Calculate Nightly Headcount"]),
        ("fig4_16_uc05.png", "Figure 4.16: UC05 - Anonymous & Open Grievance Redressal",
         "Student, Warden, Admin", ["Lodge Complaint with Category", "Select Anonymity Mode", "Warden Triages to Department", "Update Remediation Progress", "Resident Confirms Resolution"]),
        ("fig4_17_uc06.png", "Figure 4.17: UC06 - Digital Fee Collection & Invoicing",
         "Student, Admin", ["Query Monthly Fee Schedule", "View Itemized Rent & Mess Dues", "Execute Simulated Digital Payment", "Generate PDF Transaction Receipt", "Update Institutional Ledger"]),
        ("fig4_18_uc07.png", "Figure 4.18: UC07 - Mess Menu Schedule & Nutrition Feedback",
         "Student, Warden", ["Load 7-Day Breakfast/Lunch/Dinner", "Warden Edits Special Holiday Meals", "Display Daily Calorie & Diet Tags", "Resident Rates Meal Quality", "Log Special Dietary Requests"]),
        ("fig4_19_uc08.png", "Figure 4.19: UC08 - Emergency SOS Broadcasting",
         "Student, Warden, Admin", ["Resident Presses Panic Trigger", "Fetch Resident Geo & Room Location", "Dispatch Siren Alert to Warden Screen", "Send Guardian SMS Alert", "Log Police & Medical Dispatch"]),
        ("fig4_20_uc09.png", "Figure 4.20: UC09 - Automated Nightly Curfew Breach Logging",
         "System Cron, Warden", ["Compare Entry Time vs Curfew (9:30 PM)", "Flag Unaccounted Missing Hosteler", "Generate Breach Incident Notice", "Alert Warden on Duty", "Record Strike on Resident Record"]),
        ("fig4_21_uc10.png", "Figure 4.21: UC10 - System-Wide Audit Trail & Security Tracking",
         "Admin", ["Capture Every State Mutation", "Log User ID, Timestamp, IP Address", "Prevent Log Tampering & Purging", "Filter Audit Records by Actor", "Export Immutable Forensic Evidence"]),
        ("fig4_22_uc11.png", "Figure 4.22: UC11 - Analytical Reporting & CSV Exportation",
         "Admin", ["Query Room Occupancy Trends", "Generate Fee Collection Summary", "Export Roll Call & Gate Logs to CSV", "Analyze Grievance Resolution Times", "Generate Regulatory Board Reports"])
    ]
    
    for filename, title, actors, steps in uc_specs:
        fig, ax = setup_ax(9.5, 4.5)
        ax.text(4.75, 4.1, title, ha='center', fontsize=10.5, fontweight='bold', color='#2A1F3D')
        
        # Left actor card
        draw_card(ax, 0.4, 1.4, 2.2, 1.8, "PRIMARY ACTORS", actors, "#EFF6FF", "#3B82F6", "#1E3A8A")
        
        # Central boundary box
        draw_card(ax, 3.0, 0.4, 6.0, 3.4, "Use Case Execution Flow", "", "#FFFFFF", "#2A1F3D", "#4A3567", lw=1.5)
        
        sy = 3.0
        for i, s in enumerate(steps):
            draw_oval(ax, 6.0, sy, 2.6, 0.24, f"{i+1}. {s}", "#F5F3FF", "#7C3AED", lw=1)
            if i < len(steps)-1:
                draw_arrow(ax, 6.0, sy-0.24, 6.0, sy-0.42, "", "#7C3AED", lw=1.2)
            sy -= 0.62
            
        draw_arrow(ax, 2.6, 2.3, 3.4, 3.0, "Initiates", "#3B82F6")
        
        plt.tight_layout()
        plt.savefig(f"{OUT_DIR}/{filename}", bbox_inches='tight')
        plt.close()

if __name__ == "__main__":
    print("Generating Chapter 3 and Chapter 4 diagrams...")
    gen_fig3_1_gantt()
    gen_fig4_1_architecture()
    gen_fig4_2_dfd0()
    gen_fig4_3_dfd1()
    gen_fig4_4_dfd2()
    gen_fig4_5_flowchart()
    gen_fig4_6_erd()
    gen_fig4_7_class()
    gen_fig4_8_seq_gate()
    gen_fig4_9_seq_complaint()
    gen_fig4_10_seq_payment()
    gen_fig4_11_usecase_main()
    gen_individual_usecases()
    print("All Chapter 3 and Chapter 4 diagrams generated successfully!")
