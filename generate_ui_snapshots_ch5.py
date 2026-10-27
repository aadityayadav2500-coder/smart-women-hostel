"""
Generates Chapter 5 high-fidelity UI Screen Snapshots for SafeStay Project Report.
Uses matplotlib to render realistic browser frames and modern UI layouts.
"""

import os
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUT_DIR = "report_figures"
os.makedirs(OUT_DIR, exist_ok=True)

def setup_browser_canvas(title_text="SafeStay Portal", url_path="/dashboard", w=11, h=6.8):
    fig, ax = plt.subplots(figsize=(w, h), dpi=150)
    ax.set_facecolor('#0F172A') # Dark slate outer
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.8)
    ax.axis('off')
    
    # Browser Window Outer
    outer = patches.FancyBboxPatch((0.2, 0.2), 10.6, 6.4, boxstyle="round,pad=0.1",
                                  facecolor="#FFFFFF", edgecolor="#334155", linewidth=1.5)
    ax.add_patch(outer)
    
    # Browser Window Title Bar
    titlebar = patches.Rectangle((0.2, 6.1), 10.6, 0.5, facecolor="#F1F5F9", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(titlebar)
    
    # Window Buttons
    ax.plot(0.5, 6.35, 'o', markersize=7, color='#EF4444')
    ax.plot(0.75, 6.35, 'o', markersize=7, color='#F59E0B')
    ax.plot(1.0, 6.35, 'o', markersize=7, color='#10B981')
    
    # Address Bar
    addr_box = patches.FancyBboxPatch((1.4, 6.18), 7.2, 0.34, boxstyle="round,pad=0.05",
                                     facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=0.8)
    ax.add_patch(addr_box)
    ax.text(1.6, 6.35, f"[SECURE] https://safestay-hostel.internal{url_path}", ha='left', va='center', fontsize=7.5, color='#475569')
    
    # Profile & Status in Browser Bar
    ax.text(9.8, 6.35, "ACTIVE HOST: 127.0.0.1", ha='right', va='center', fontsize=7.5, fontweight='bold', color='#10B981')
    
    # App Header Bar (Inside web app)
    app_header = patches.Rectangle((0.2, 5.5), 10.6, 0.6, facecolor="#2A1F3D", edgecolor="#1E162D", linewidth=1)
    ax.add_patch(app_header)
    ax.text(0.6, 5.8, "SafeStay", ha='left', va='center', fontsize=12, fontweight='bold', color='#FFFFFF')
    ax.text(1.9, 5.8, "Smart Women Hostel System", ha='left', va='center', fontsize=8.5, color='#C5A880')
    ax.text(10.3, 5.8, title_text, ha='right', va='center', fontsize=8.5, fontweight='bold', color='#FDE047')
    
    return fig, ax

def draw_sidebar(ax, active_tab="Dashboard", role="Student"):
    # Dark purple sidebar
    sb = patches.Rectangle((0.2, 0.2), 2.2, 5.3, facecolor="#1F172E", edgecolor="#1F172E")
    ax.add_patch(sb)
    
    # Role Badge
    role_box = patches.FancyBboxPatch((0.4, 4.85), 1.8, 0.45, boxstyle="round,pad=0.05",
                                     facecolor="#3B2B54", edgecolor="#C5A880", linewidth=1)
    ax.add_patch(role_box)
    ax.text(1.3, 5.08, f"PORTAL: {role.upper()}", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#FBBF24')
    
    tabs = {
        "Student": ["Dashboard", "My Profile", "Gate Pass", "Complaints", "Rent & Fees", "Mess Menu"],
        "Warden": ["Overview", "Attendance", "QR Gate Scan", "Pass Approvals", "Complaints", "Mess Schedule"],
        "Admin": ["Dashboard", "Student Roster", "Room Allocation", "Financial Ledger", "Reports & CSV", "Audit Trail", "Settings"]
    }.get(role, ["Dashboard"])
    
    ty = 4.4
    for t in tabs:
        is_active = (t == active_tab)
        bg = "#4A3567" if is_active else "#1F172E"
        fg = "#FFFFFF" if is_active else "#94A3B8"
        tb = patches.FancyBboxPatch((0.35, ty-0.12), 1.9, 0.32, boxstyle="round,pad=0.04",
                                   facecolor=bg, edgecolor=None if not is_active else "#C5A880", linewidth=0.8)
        ax.add_patch(tb)
        ax.text(0.6, ty+0.04, f"•  {t}", ha='left', va='center', fontsize=8, fontweight='bold' if is_active else 'normal', color=fg)
        ty -= 0.42

# 1. Login Screen
def gen_fig5_1_login():
    fig, ax = setup_browser_canvas("Authentication Portal", "/login")
    
    # Full page background
    bg = patches.Rectangle((0.2, 0.2), 10.6, 5.3, facecolor="#F8FAFC")
    ax.add_patch(bg)
    
    # Login Card Centered
    card = patches.FancyBboxPatch((3.0, 0.6), 5.0, 4.5, boxstyle="round,pad=0.15",
                                 facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1.5)
    ax.add_patch(card)
    
    # Header inside card
    ax.text(5.5, 4.6, "SafeStay Secure Login", ha='center', fontsize=13, fontweight='bold', color='#2A1F3D')
    ax.text(5.5, 4.25, "Select your authorized portal to authenticate", ha='center', fontsize=8, color='#64748B')
    
    # 3 Role Selectors
    roles = [("Student", 3.4), ("Warden", 4.9), ("Admin", 6.4)]
    for r_name, rx in roles:
        is_sel = (r_name == "Student")
        box = patches.FancyBboxPatch((rx, 3.6), 1.2, 0.45, boxstyle="round,pad=0.05",
                                    facecolor="#EDE9FE" if is_sel else "#F1F5F9",
                                    edgecolor="#6D28D9" if is_sel else "#CBD5E1", linewidth=1.2)
        ax.add_patch(box)
        ax.text(rx+0.6, 3.82, r_name, ha='center', va='center', fontsize=8, fontweight='bold',
                color="#4C1D95" if is_sel else "#475569")
                
    # Input Fields (Empty per user requirement)
    # Username
    ax.text(3.4, 3.25, "Username / Student Roll No", ha='left', fontsize=8, fontweight='bold', color='#334155')
    inp1 = patches.FancyBboxPatch((3.4, 2.75), 4.2, 0.38, boxstyle="round,pad=0.04",
                                 facecolor="#FFFFFF", edgecolor="#94A3B8", linewidth=1)
    ax.add_patch(inp1)
    ax.text(3.55, 2.94, "Enter your assigned username...", ha='left', va='center', fontsize=7.5, color='#94A3B8', style='italic')
    
    # Password
    ax.text(3.4, 2.45, "Password", ha='left', fontsize=8, fontweight='bold', color='#334155')
    inp2 = patches.FancyBboxPatch((3.4, 1.95), 4.2, 0.38, boxstyle="round,pad=0.04",
                                 facecolor="#FFFFFF", edgecolor="#94A3B8", linewidth=1)
    ax.add_patch(inp2)
    ax.text(3.55, 2.14, "••••••••••••", ha='left', va='center', fontsize=7.5, color='#94A3B8')
    
    # Submit Button
    btn = patches.FancyBboxPatch((3.4, 1.25), 4.2, 0.48, boxstyle="round,pad=0.06",
                                facecolor="#2A1F3D", edgecolor="#C5A880", linewidth=1)
    ax.add_patch(btn)
    ax.text(5.5, 1.49, "Sign In to Student Portal →", ha='center', va='center', fontsize=9, fontweight='bold', color='#FFFFFF')
    
    # Security badges
    ax.text(5.5, 0.85, "[SEC] 256-Bit SSL Encrypted  •  Role Isolation Enforced  •  No Default Passwords", ha='center', fontsize=7, color='#64748B')
    
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig5_1_login.png", bbox_inches='tight')
    plt.close()

# 2. Student Dashboard
def gen_fig5_2_student_dash():
    fig, ax = setup_browser_canvas("Resident Dashboard", "/student/dashboard")
    draw_sidebar(ax, "Dashboard", "Student")
    
    # Banner
    banner = patches.FancyBboxPatch((2.6, 4.4), 8.0, 0.9, boxstyle="round,pad=0.08",
                                   facecolor="#EDE9FE", edgecolor="#8B5CF6", linewidth=1.2)
    ax.add_patch(banner)
    ax.text(2.8, 4.95, "Welcome back, Aaditya Yadav (Roll: 6420)!", ha='left', fontsize=11, fontweight='bold', color='#4C1D95')
    ax.text(2.8, 4.62, "Room 204-B (North Wing)  •  Curfew Deadline: 09:30 PM Tonight  •  Attendance Status: Present", ha='left', fontsize=8, color='#5B21B6')
    
    # Stat Cards
    stats = [
        ("Curfew Timer", "1h 45m left", "#F0FDF4", "#16A34A", "#14532D"),
        ("Active Gate Pass", "Valid (Local)", "#EFF6FF", "#2563EB", "#1E3A8A"),
        ("Mess Today", "Paneer & Dal", "#FEF3C7", "#D97706", "#78350F"),
        ("Fee Dues", "Rs. 0.00 (All Clear)", "#FDF2F8", "#DB2777", "#831843")
    ]
    cx = 2.6
    for title, val, bg, bc, fc in stats:
        card = patches.FancyBboxPatch((cx, 3.2), 1.85, 0.95, boxstyle="round,pad=0.06",
                                     facecolor=bg, edgecolor=bc, linewidth=1)
        ax.add_patch(card)
        ax.text(cx+0.15, 3.85, title, ha='left', fontsize=7.5, color='#475569')
        ax.text(cx+0.15, 3.45, val, ha='left', fontsize=9.5, fontweight='bold', color=fc)
        cx += 2.05
        
    # Quick Actions & Timeline
    card1 = patches.FancyBboxPatch((2.6, 0.4), 3.8, 2.5, boxstyle="round,pad=0.08",
                                  facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(card1)
    ax.text(2.8, 2.6, "Quick Resident Actions", ha='left', fontsize=9.5, fontweight='bold', color='#2A1F3D')
    
    q_actions = ["Request Gate Pass", "Emergency SOS Alarm", "Lodge Maintenance Grievance", "View Mess Menu Timetable"]
    qy = 2.1
    for qa in q_actions:
        btn = patches.FancyBboxPatch((2.8, qy-0.08), 3.4, 0.32, boxstyle="round,pad=0.04",
                                    facecolor="#F1F5F9", edgecolor="#CBD5E1", linewidth=0.8)
        ax.add_patch(btn)
        ax.text(3.0, ty:=qy+0.08, f"→  {qa}", ha='left', va='center', fontsize=8, color='#334155')
        qy -= 0.45
        
    # Notice Card
    card2 = patches.FancyBboxPatch((6.8, 0.4), 3.8, 2.5, boxstyle="round,pad=0.08",
                                  facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(card2)
    ax.text(7.0, 2.6, "Hostel Notice Board", ha='left', fontsize=9.5, fontweight='bold', color='#2A1F3D')
    ax.text(7.0, 2.15, "[NOTICE] Mandatory Fire Safety Drill", ha='left', fontsize=8, fontweight='bold', color='#DC2626')
    ax.text(7.0, 1.9, "Tomorrow at 10:00 AM in the Central Courtyard.", ha='left', fontsize=7.5, color='#475569')
    ax.text(7.0, 1.45, "[MEAL] Sunday Special Dinner Feast", ha='left', fontsize=8, fontweight='bold', color='#D97706')
    ax.text(7.0, 1.2, "North Indian Thali + Gulab Jamun served 7:30 PM.", ha='left', fontsize=7.5, color='#475569')
    ax.text(7.0, 0.75, "[WIFI] Wi-Fi Maintenance Tonight", ha='left', fontsize=8, fontweight='bold', color='#2563EB')
    ax.text(7.0, 0.55, "Wing B router upgrade between 12:00 AM - 01:00 AM.", ha='left', fontsize=7.5, color='#475569')
    
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig5_2_student_dash.png", bbox_inches='tight')
    plt.close()

# 3. Student Profile
def gen_fig5_3_student_profile():
    fig, ax = setup_browser_canvas("Resident Profile", "/student/profile")
    draw_sidebar(ax, "My Profile", "Student")
    
    # Left Card - ID Badge
    c1 = patches.FancyBboxPatch((2.6, 0.6), 3.2, 4.7, boxstyle="round,pad=0.08",
                               facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(c1)
    # Photo placeholder
    photo = patches.FancyBboxPatch((3.5, 3.6), 1.4, 1.4, boxstyle="round,pad=0.05",
                                  facecolor="#EDE9FE", edgecolor="#8B5CF6", linewidth=1.5)
    ax.add_patch(photo)
    ax.text(4.2, 4.3, "STUDENT\nPHOTO", ha='center', va='center', fontsize=8, fontweight='bold', color='#6D28D9')
    
    ax.text(4.2, 3.2, "Aaditya Mangesh Yadav", ha='center', fontsize=10, fontweight='bold', color='#2A1F3D')
    ax.text(4.2, 2.9, "Roll No: 6420  •  B.Sc.(IT)", ha='center', fontsize=8, color='#64748B')
    ax.text(4.2, 2.6, "Room 204-B | North Wing", ha='center', fontsize=8, fontweight='bold', color='#059669')
    
    # Details in left card
    det = [("Status", "Active Resident"), ("Contact", "+91 98765 43210"), ("Guardian", "+91 98200 12345"), ("Blood Grp", "O+ Positive")]
    dy = 2.1
    for k, v in det:
        ax.text(2.8, dy, k, ha='left', fontsize=7.5, color='#64748B')
        ax.text(5.6, dy, v, ha='right', fontsize=7.5, fontweight='bold', color='#334155')
        dy -= 0.38
        
    # Right Card - Room Allocation & Roommates
    c2 = patches.FancyBboxPatch((6.1, 0.6), 4.5, 4.7, boxstyle="round,pad=0.08",
                               facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(c2)
    ax.text(6.3, 4.95, "Room Allocation & Facilities", ha='left', fontsize=10.5, fontweight='bold', color='#2A1F3D')
    
    r_info = [("Room Number", "204 (Bed B)"), ("Floor & Wing", "2nd Floor, Wing North"),
              ("Room Type", "Triple Sharing (AC)"), ("Monthly Fee", "Rs. 8,500 / month"),
              ("Hostel Warden", "Ms. Aditi Prajapati")]
    ry = 4.45
    for k, v in r_info:
        ax.text(6.4, ry, f"• {k}:", ha='left', fontsize=8, color='#475569')
        ax.text(10.3, ry, v, ha='right', fontsize=8, fontweight='bold', color='#1E293B')
        ry -= 0.38
        
    # Roommates Table
    ax.text(6.3, 2.4, "Assigned Roommates", ha='left', fontsize=9.5, fontweight='bold', color='#2A1F3D')
    mates = [
        ("Bed A", "Sanskruti Amol Malkar", "6452", "In Hostel"),
        ("Bed C", "Pooja Suresh Sharma", "6488", "On Gate Pass")
    ]
    my = 1.95
    for bed, name, rno, st in mates:
        box = patches.FancyBboxPatch((6.3, my-0.12), 4.1, 0.42, boxstyle="round,pad=0.04",
                                    facecolor="#F8FAFC", edgecolor="#E2E8F0", linewidth=0.8)
        ax.add_patch(box)
        ax.text(6.5, my+0.1, f"{bed}: {name} ({rno})", ha='left', fontsize=7.5, fontweight='bold', color='#334155')
        ax.text(10.2, my+0.1, st, ha='right', fontsize=7, fontweight='bold',
                color='#16A34A' if "In" in st else '#D97706')
        my -= 0.55
        
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig5_3_student_profile.png", bbox_inches='tight')
    plt.close()

# 4. Student Gate Pass
def gen_fig5_4_student_gatepass():
    fig, ax = setup_browser_canvas("Gate Pass Management", "/student/gatepass")
    draw_sidebar(ax, "Gate Pass", "Student")
    
    # Left Card - Apply Form
    c1 = patches.FancyBboxPatch((2.6, 0.5), 4.2, 4.8, boxstyle="round,pad=0.08",
                               facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(c1)
    ax.text(2.8, 4.95, "Apply for Gate Pass", ha='left', fontsize=10.5, fontweight='bold', color='#2A1F3D')
    
    fields = [("Pass Type", "Local Outing (Return by Curfew)"),
              ("Out Time", "2026-10-25 17:00"),
              ("Expected Return", "2026-10-25 21:00 (Before 9:30 PM)"),
              ("Purpose / Destination", "Library Study Group & Stationery Purchase")]
    fy = 4.45
    for lbl, val in fields:
        ax.text(2.8, fy, lbl, ha='left', fontsize=7.5, fontweight='bold', color='#334155')
        ibox = patches.FancyBboxPatch((2.8, fy-0.38), 3.8, 0.3, boxstyle="round,pad=0.04",
                                     facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=0.8)
        ax.add_patch(ibox)
        ax.text(2.95, fy-0.22, val, ha='left', fontsize=7.5, color='#1E293B')
        fy -= 0.72
        
    # Parent Consent checkbox
    ax.text(2.8, 1.5, "[x] Parent Consent Notified via SMS", ha='left', fontsize=7.5, color='#16A34A')
    
    # Submit Button
    sbtn = patches.FancyBboxPatch((2.8, 0.8), 3.8, 0.45, boxstyle="round,pad=0.05",
                                 facecolor="#2A1F3D", edgecolor="#C5A880", linewidth=1)
    ax.add_patch(sbtn)
    ax.text(4.7, 1.02, "Submit Gate Pass Application →", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#FFFFFF')
    
    # Right Card - Active Approved QR Pass
    c2 = patches.FancyBboxPatch((7.1, 0.5), 3.5, 4.8, boxstyle="round,pad=0.08",
                               facecolor="#FFFFFF", edgecolor="#10B981", linewidth=1.5)
    ax.add_patch(c2)
    ax.text(8.85, 4.95, "ACTIVE PASS QR", ha='center', fontsize=10.5, fontweight='bold', color='#047857')
    
    # QR Code Mockup (Checkered box)
    qr_bg = patches.Rectangle((7.65, 2.5), 2.4, 2.2, facecolor="#F8FAFC", edgecolor="#0F172A", linewidth=1.5)
    ax.add_patch(qr_bg)
    # Draw QR modules using deterministic pattern
    random.seed(42)
    for i in range(9):
        qx = 7.8 + i * (2.0 / 8.0)
        for j in range(9):
            qy = 2.65 + j * (1.8 / 8.0)
            if random.random() > 0.45 or (i in [0, 8] and j in [0, 8]):
                ax.plot(qx, qy, 's', markersize=6, color='#0F172A')
                
    ax.text(8.85, 2.15, "PASS ID: GP-2026-8812", ha='center', fontsize=8, fontweight='bold', color='#2A1F3D')
    ax.text(8.85, 1.85, "Status: APPROVED BY WARDEN", ha='center', fontsize=7.5, fontweight='bold', color='#16A34A')
    ax.text(8.85, 1.55, "Valid: Today until 9:00 PM", ha='center', fontsize=7.5, color='#475569')
    ax.text(8.85, 1.05, "Present this screen to the security\nguard at the hostel entry turnstile.", ha='center', fontsize=7, color='#64748B')
    
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig5_4_student_gatepass.png", bbox_inches='tight')
    plt.close()

# 5. Student Complaints
def gen_fig5_5_student_complaint():
    fig, ax = setup_browser_canvas("Grievance Redressal", "/student/complaints")
    draw_sidebar(ax, "Complaints", "Student")
    
    # Left Card - Lodge Grievance
    c1 = patches.FancyBboxPatch((2.6, 0.6), 3.8, 4.7, boxstyle="round,pad=0.08",
                               facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(c1)
    ax.text(2.8, 4.95, "Lodge a Grievance", ha='left', fontsize=10.5, fontweight='bold', color='#2A1F3D')
    
    fields = [("Category", "Electrical (Ceiling Fan / Plug Point)"),
              ("Room / Wing", "Room 204-B (North Wing)"),
              ("Urgency Level", "Medium (Affecting Studies)"),
              ("Detailed Description", "Ceiling fan making clicking sound on speed 3.\nNeed maintenance check.")]
    fy = 4.45
    for lbl, val in fields:
        ax.text(2.8, fy, lbl, ha='left', fontsize=7.5, fontweight='bold', color='#334155')
        ibox = patches.FancyBboxPatch((2.8, fy-0.38), 3.4, 0.3 if "Description" not in lbl else 0.55,
                                     boxstyle="round,pad=0.04", facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=0.8)
        ax.add_patch(ibox)
        ax.text(2.95, fy-0.22, val, ha='left', fontsize=7.2, color='#1E293B')
        fy -= 0.72 if "Description" not in lbl else 0.95
        
    # Anonymity option
    ax.text(2.8, 1.45, "[ ] Submit anonymously (Hide resident name)", ha='left', fontsize=7.5, color='#64748B')
    
    # Submit Button
    sbtn = patches.FancyBboxPatch((2.8, 0.8), 3.4, 0.42, boxstyle="round,pad=0.05",
                                 facecolor="#2A1F3D", edgecolor="#C5A880", linewidth=1)
    ax.add_patch(sbtn)
    ax.text(4.5, 1.01, "Submit Grievance Ticket →", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#FFFFFF')
    
    # Right Card - Past Tickets
    c2 = patches.FancyBboxPatch((6.7, 0.6), 3.9, 4.7, boxstyle="round,pad=0.08",
                               facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(c2)
    ax.text(6.9, 4.95, "My Grievance Status", ha='left', fontsize=10.5, fontweight='bold', color='#2A1F3D')
    
    tickets = [
        ("TKT-2026-104", "Electrical: Fan Sound", "IN PROGRESS", "#D97706", "Assigned to Electrician Ramesh (ETA: 4 PM)"),
        ("TKT-2026-089", "Plumbing: Hot Water Tap", "RESOLVED", "#16A34A", "Replaced washer on Oct 20 by Maintenance"),
        ("TKT-2026-042", "Wi-Fi: 2nd Floor Drop", "RESOLVED", "#16A34A", "Access point reset & firmware updated")
    ]
    ty = 4.35
    for tid, title, st, st_col, notes in tickets:
        tbox = patches.FancyBboxPatch((6.9, ty-0.7), 3.5, 0.75, boxstyle="round,pad=0.04",
                                     facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=0.8)
        ax.add_patch(tbox)
        ax.text(7.05, ty-0.08, tid, ha='left', fontsize=7.5, fontweight='bold', color='#2A1F3D')
        ax.text(10.25, ty-0.08, st, ha='right', fontsize=7, fontweight='bold', color=st_col)
        ax.text(7.05, ty-0.3, title, ha='left', fontsize=7.5, color='#334155')
        ax.text(7.05, ty-0.52, notes, ha='left', fontsize=6.8, color='#64748B', style='italic')
        ty -= 1.15
        
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig5_5_student_complaints.png", bbox_inches='tight')
    plt.close()

# 6. Student Payments
def gen_fig5_6_student_payments():
    fig, ax = setup_browser_canvas("Rent & Fee Management", "/student/payments")
    draw_sidebar(ax, "Rent & Fees", "Student")
    
    # Dues Banner
    b = patches.FancyBboxPatch((2.6, 4.1), 8.0, 1.2, boxstyle="round,pad=0.08",
                              facecolor="#F0FDF4", edgecolor="#16A34A", linewidth=1.2)
    ax.add_patch(b)
    ax.text(2.85, 4.85, "Current Billing Cycle: October 2026", ha='left', fontsize=10.5, fontweight='bold', color='#14532D')
    ax.text(2.85, 4.45, "Room 204-B  •  Total Amount: Rs. 8,500  •  Due Date: 10th October 2026", ha='left', fontsize=8, color='#15803D')
    
    # Pay Now Button
    pbtn = patches.FancyBboxPatch((8.8, 4.4), 1.6, 0.5, boxstyle="round,pad=0.05",
                                 facecolor="#16A34A", edgecolor="#14532D", linewidth=1)
    ax.add_patch(pbtn)
    ax.text(9.6, 4.65, "PAID IN FULL", ha='center', va='center', fontsize=8, fontweight='bold', color='#FFFFFF')
    
    # Ledger Table Card
    c = patches.FancyBboxPatch((2.6, 0.5), 8.0, 3.3, boxstyle="round,pad=0.08",
                              facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(c)
    ax.text(2.85, 3.45, "Fee Payment Ledger & Downloadable Receipts", ha='left', fontsize=10, fontweight='bold', color='#2A1F3D')
    
    # Table header
    th = patches.Rectangle((2.8, 2.9), 7.6, 0.35, facecolor="#2A1F3D")
    ax.add_patch(th)
    cols = [(2.9, "Invoice Ref"), (4.1, "Month"), (5.3, "Description"), (6.8, "Amount"), (8.0, "Status"), (9.3, "Receipt")]
    for x, txt in cols:
        ax.text(x, 3.07, txt, ha='left', fontsize=7.5, fontweight='bold', color='#FFFFFF')
        
    rows = [
        ("INV-2026-104", "Oct 2026", "Room Rent + Mess", "Rs. 8,500.00", "PAID", "v PDF"),
        ("INV-2026-092", "Sep 2026", "Room Rent + Mess", "Rs. 8,500.00", "PAID", "v PDF"),
        ("INV-2026-081", "Aug 2026", "Room Rent + Mess", "Rs. 8,500.00", "PAID", "v PDF"),
        ("INV-2026-070", "Jul 2026", "Security Deposit", "Rs. 15,000.00", "PAID", "v PDF"),
    ]
    ry = 2.5
    for ref, m, desc, amt, st, rec in rows:
        ax.text(2.9, ry, ref, ha='left', fontsize=7.5, color='#334155')
        ax.text(4.1, ry, m, ha='left', fontsize=7.5, color='#334155')
        ax.text(5.3, ry, desc, ha='left', fontsize=7.5, color='#334155')
        ax.text(6.8, ry, amt, ha='left', fontsize=7.5, fontweight='bold', color='#0F172A')
        ax.text(8.0, ry, st, ha='left', fontsize=7.5, fontweight='bold', color='#16A34A')
        ax.text(9.3, ry, rec, ha='left', fontsize=7.5, color='#2563EB')
        ax.plot([2.8, 10.4], [ry-0.12, ry-0.12], color='#E2E8F0', lw=0.6)
        ry -= 0.45
        
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig5_6_student_payments.png", bbox_inches='tight')
    plt.close()

# 7. Student Mess Menu
def gen_fig5_7_student_mess():
    fig, ax = setup_browser_canvas("Mess Timetable & Nutrition", "/student/mess")
    draw_sidebar(ax, "Mess Menu", "Student")
    
    # Day selector
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    dx = 2.6
    for d in days:
        is_cur = (d == "Sun")
        box = patches.FancyBboxPatch((dx, 4.6), 1.05, 0.45, boxstyle="round,pad=0.04",
                                    facecolor="#2A1F3D" if is_cur else "#F1F5F9",
                                    edgecolor="#C5A880" if is_cur else "#CBD5E1", linewidth=1)
        ax.add_patch(box)
        ax.text(dx+0.52, 4.82, d, ha='center', va='center', fontsize=8, fontweight='bold',
                color="#FFFFFF" if is_cur else "#475569")
        dx += 1.15
        
    # Meal Cards
    meals = [
        ("Breakfast (7:30 - 9:30 AM)", ["Poha with crunchy peanuts & lemon", "Boiled eggs / Bananas", "Filter Coffee / Tea", "Calories: ~380 kcal"], "#FEF3C7", "#D97706"),
        ("Lunch (12:30 - 2:30 PM)", ["Paneer Butter Masala", "Yellow Tadka Dal & Steamed Rice", "Fresh Phulkas (3 pcs) + Cucumber Salad", "Calories: ~650 kcal"], "#EFF6FF", "#2563EB"),
        ("Evening Snacks (5:00 - 6:00 PM)", ["Vegetable Cutlet with Mint Chutney", "Hot Ginger Tea / Masala Milk", "Calories: ~220 kcal"], "#FDF2F8", "#DB2777"),
        ("Dinner (7:30 - 9:30 PM)", ["Aloo Gobi Matar & Chapati", "Jeera Rice & Moong Dal", "Sweet: Hot Gulab Jamun", "Calories: ~580 kcal"], "#F0FDF4", "#16A34A")
    ]
    my = 3.9
    for m_title, items, m_bg, m_border in meals:
        card = patches.FancyBboxPatch((2.6, my-0.8), 8.0, 0.78, boxstyle="round,pad=0.06",
                                     facecolor=m_bg, edgecolor=m_border, linewidth=1)
        ax.add_patch(card)
        ax.text(2.85, my-0.2, m_title, ha='left', fontsize=8.5, fontweight='bold', color='#1E293B')
        ax.text(2.85, my-0.5, " • ".join(items[:-1]), ha='left', fontsize=7.5, color='#334155')
        ax.text(10.3, my-0.2, items[-1], ha='right', fontsize=7.2, fontweight='bold', color=m_border)
        my -= 0.95
        
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig5_7_student_mess.png", bbox_inches='tight')
    plt.close()

# 8. Warden Dashboard
def gen_fig5_8_warden_dash():
    fig, ax = setup_browser_canvas("Warden Command Center", "/warden/dashboard")
    draw_sidebar(ax, "Overview", "Warden")
    
    # Stat Cards
    stats = [
        ("Hostel Occupancy", "142 / 150 (95%)", "#EDE9FE", "#7C3AED", "#4C1D95"),
        ("Outside on Gate Pass", "8 Residents", "#EFF6FF", "#2563EB", "#1E3A8A"),
        ("Pending Pass Requests", "3 Awaiting", "#FEF3C7", "#D97706", "#78350F"),
        ("Active Grievances", "4 In-Progress", "#FEF2F2", "#DC2626", "#991B1B")
    ]
    cx = 2.6
    for title, val, bg, bc, fc in stats:
        card = patches.FancyBboxPatch((cx, 4.3), 1.85, 0.95, boxstyle="round,pad=0.06",
                                     facecolor=bg, edgecolor=bc, linewidth=1)
        ax.add_patch(card)
        ax.text(cx+0.15, 4.95, title, ha='left', fontsize=7.2, color='#475569')
        ax.text(cx+0.15, 4.55, val, ha='left', fontsize=9.5, fontweight='bold', color=fc)
        cx += 2.05
        
    # Curfew Countdown & Emergency Alert Banner
    eb = patches.FancyBboxPatch((2.6, 3.4), 8.0, 0.7, boxstyle="round,pad=0.06",
                               facecolor="#2A1F3D", edgecolor="#C5A880", linewidth=1.2)
    ax.add_patch(eb)
    ax.text(2.85, 3.82, "[TIME] Nightly Curfew Lockdown: 09:30 PM", ha='left', fontsize=9.5, fontweight='bold', color='#FFFFFF')
    ax.text(2.85, 3.55, "Gate scanner armed. Automated breach notices will dispatch to Guardians at 09:31 PM.", ha='left', fontsize=7.5, color='#FDE047')
    
    # Left table - Recent Movement
    c1 = patches.FancyBboxPatch((2.6, 0.5), 4.2, 2.6, boxstyle="round,pad=0.06",
                               facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(c1)
    ax.text(2.8, 2.8, "Recent Gate Movements", ha='left', fontsize=9, fontweight='bold', color='#2A1F3D')
    
    moves = [
        ("Aaditya Yadav (6420)", "Room 204", "17:15 OUT", "#2563EB"),
        ("Sanskruti Malkar (6452)", "Room 204", "18:40 IN", "#16A34A"),
        ("Neha Patil (6418)", "Room 102", "19:05 IN", "#16A34A"),
        ("Pooja Sharma (6488)", "Room 301", "19:22 OUT", "#2563EB")
    ]
    my = 2.4
    for name, rm, st, col in moves:
        ax.text(2.8, my, name, ha='left', fontsize=7.5, color='#1E293B')
        ax.text(4.8, my, rm, ha='left', fontsize=7.2, color='#64748B')
        ax.text(6.6, my, st, ha='right', fontsize=7.5, fontweight='bold', color=col)
        my -= 0.45
        
    # Right table - Actionable Alerts
    c2 = patches.FancyBboxPatch((7.0, 0.5), 3.6, 2.6, boxstyle="round,pad=0.06",
                               facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(c2)
    ax.text(7.2, 2.8, "Warden Immediate Tasks", ha='left', fontsize=9, fontweight='bold', color='#2A1F3D')
    
    tasks = [
        ("Approve Outstation Pass (Riya K.)", "Urgent", "#DC2626"),
        ("Review Electrical Ticket (Room 204)", "Today", "#D97706"),
        ("Verify Dinner Mess Nutrition Log", "Routine", "#2563EB"),
        ("Conduct Floor 2 Headcount Roll Call", "9:30 PM", "#7C3AED")
    ]
    ty = 2.4
    for t_text, priority, p_col in tasks:
        ax.text(7.2, ty, t_text, ha='left', fontsize=7.2, color='#1E293B')
        ax.text(10.4, ty, priority, ha='right', fontsize=7, fontweight='bold', color=p_col)
        ty -= 0.45
        
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig5_8_warden_dash.png", bbox_inches='tight')
    plt.close()

# 9. Warden Attendance Register
def gen_fig5_9_warden_attendance():
    fig, ax = setup_browser_canvas("Curfew Roll Call Register", "/warden/attendance")
    draw_sidebar(ax, "Attendance", "Warden")
    
    # Filter Controls
    f_bar = patches.FancyBboxPatch((2.6, 4.6), 8.0, 0.65, boxstyle="round,pad=0.05",
                                  facecolor="#F1F5F9", edgecolor="#CBD5E1", linewidth=0.8)
    ax.add_patch(f_bar)
    ax.text(2.8, 4.95, "Date: 2026-10-25 (Today)  •  Wing: North Wing  •  Floor: 2nd Floor  •  Filter: All Students", ha='left', fontsize=8, color='#334155')
    
    # Table Card
    c = patches.FancyBboxPatch((2.6, 0.5), 8.0, 3.8, boxstyle="round,pad=0.08",
                              facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(c)
    ax.text(2.8, 3.95, "Resident Roll Call Verification (Curfew Deadline: 09:30 PM)", ha='left', fontsize=9.5, fontweight='bold', color='#2A1F3D')
    
    # Table Header
    th = patches.Rectangle((2.8, 3.5), 7.6, 0.35, facecolor="#2A1F3D")
    ax.add_patch(th)
    headers = [(2.9, "Roll No"), (3.9, "Student Name"), (5.8, "Room"), (6.8, "Gate Status"), (8.1, "Curfew Status"), (9.4, "Action")]
    for x, txt in headers:
        ax.text(x, 3.68, txt, ha='left', fontsize=7.5, fontweight='bold', color='#FFFFFF')
        
    students = [
        ("6420", "Aaditya Mangesh Yadav", "204-B", "In (18:45)", "PRESENT", "#16A34A"),
        ("6452", "Sanskruti Amol Malkar", "204-A", "In (18:40)", "PRESENT", "#16A34A"),
        ("6418", "Neha Ravindra Patil", "102-C", "On Pass (9 PM)", "AUTHORIZED", "#2563EB"),
        ("6488", "Pooja Suresh Sharma", "301-B", "Outside (Late)", "BREACH ALERT", "#DC2626"),
        ("6491", "Kavita Ramesh Gupta", "205-A", "In (19:10)", "PRESENT", "#16A34A"),
        ("6502", "Ananya Vinod Shinde", "104-B", "Medical Leave", "ON LEAVE", "#D97706")
    ]
    sy = 3.1
    for rno, name, rm, gst, cst, ccol in students:
        ax.text(2.9, sy, rno, ha='left', fontsize=7.5, color='#334155')
        ax.text(3.9, sy, name, ha='left', fontsize=7.5, fontweight='bold', color='#1E293B')
        ax.text(5.8, sy, rm, ha='left', fontsize=7.5, color='#475569')
        ax.text(6.8, sy, gst, ha='left', fontsize=7.5, color='#334155')
        ax.text(8.1, sy, cst, ha='left', fontsize=7.2, fontweight='bold', color=ccol)
        
        # Checkbox / Toggle
        btn = patches.FancyBboxPatch((9.3, sy-0.08), 1.0, 0.24, boxstyle="round,pad=0.02",
                                    facecolor="#F1F5F9", edgecolor="#CBD5E1", linewidth=0.6)
        ax.add_patch(btn)
        ax.text(9.8, sy+0.04, "Verify ✓", ha='center', va='center', fontsize=6.8, color='#047857')
        
        ax.plot([2.8, 10.4], [sy-0.12, sy-0.12], color='#F1F5F9', lw=0.6)
        sy -= 0.42
        
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig5_9_warden_attendance.png", bbox_inches='tight')
    plt.close()

# 10. Warden QR Scanner
def gen_fig5_10_warden_scanner():
    fig, ax = setup_browser_canvas("Optical QR Gate Scanner", "/warden/scanner")
    draw_sidebar(ax, "QR Gate Scan", "Warden")
    
    # Camera Viewport Left
    cam = patches.FancyBboxPatch((2.6, 0.6), 4.2, 4.6, boxstyle="round,pad=0.08",
                                facecolor="#020617", edgecolor="#22C55E", linewidth=2)
    ax.add_patch(cam)
    ax.text(4.7, 4.85, "[CAM] GATE CAMERA STREAM (LIVE)", ha='center', fontsize=8.5, fontweight='bold', color='#4ADE80')
    
    # Targeting Reticle
    reticle = patches.Rectangle((3.4, 1.8), 2.6, 2.2, facecolor="none", edgecolor="#22C55E", linewidth=1.5, linestyle="--")
    ax.add_patch(reticle)
    ax.plot([3.4, 3.8], [4.0, 4.0], color='#4ADE80', lw=3)
    ax.plot([3.4, 3.4], [3.6, 4.0], color='#4ADE80', lw=3)
    ax.plot([5.6, 6.0], [4.0, 4.0], color='#4ADE80', lw=3)
    ax.plot([6.0, 6.0], [3.6, 4.0], color='#4ADE80', lw=3)
    
    # Laser scan line
    ax.plot([3.4, 6.0], [2.9, 2.9], color='#EF4444', lw=2)
    ax.text(4.7, 1.4, "SCAN STATUS: QR DETECTED & DECODED", ha='center', fontsize=7.5, fontweight='bold', color='#22C55E')
    
    # Right Card - Verification Details
    c2 = patches.FancyBboxPatch((7.0, 0.6), 3.6, 4.6, boxstyle="round,pad=0.08",
                               facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(c2)
    ax.text(8.8, 4.85, "Resident Verification Match", ha='center', fontsize=9.5, fontweight='bold', color='#2A1F3D')
    
    # Match Badge
    mb = patches.FancyBboxPatch((7.3, 4.1), 3.0, 0.45, boxstyle="round,pad=0.04",
                               facecolor="#DCFCE7", edgecolor="#16A34A", linewidth=1)
    ax.add_patch(mb)
    ax.text(8.8, 4.32, "AUTHORIZED ENTRY PERMITTED", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#14532D')
    
    det = [
        ("Student Name", "Aaditya Mangesh Yadav"),
        ("Roll Number", "6420"),
        ("Room Allocated", "204-B (North Wing)"),
        ("Pass Type", "Local Evening Pass"),
        ("Pass Expiry", "Today 21:00 (Valid)"),
        ("Curfew Deadline", "21:30 (On Time)"),
        ("Check-In Time", "18:45:12 PM IST")
    ]
    dy = 3.65
    for k, v in det:
        ax.text(7.3, dy, k, ha='left', fontsize=7.2, color='#64748B')
        ax.text(10.3, dy, v, ha='right', fontsize=7.2, fontweight='bold', color='#1E293B')
        dy -= 0.38
        
    # Confirm Check-in Button
    cbtn = patches.FancyBboxPatch((7.3, 0.9), 3.0, 0.45, boxstyle="round,pad=0.05",
                                 facecolor="#16A34A", edgecolor="#14532D", linewidth=1)
    ax.add_patch(cbtn)
    ax.text(8.8, 1.12, "Confirm Check-In & Log Entry ✓", ha='center', va='center', fontsize=8, fontweight='bold', color='#FFFFFF')
    
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig5_10_warden_scanner.png", bbox_inches='tight')
    plt.close()

# 11. Warden Pass Approvals
def gen_fig5_11_warden_passes():
    fig, ax = setup_browser_canvas("Gate Pass Approvals", "/warden/approvals")
    draw_sidebar(ax, "Pass Approvals", "Warden")
    
    c = patches.FancyBboxPatch((2.6, 0.6), 8.0, 4.6, boxstyle="round,pad=0.08",
                              facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(c)
    ax.text(2.8, 4.85, "Pending Resident Gate Pass Requests", ha='left', fontsize=10.5, fontweight='bold', color='#2A1F3D')
    
    th = patches.Rectangle((2.8, 4.3), 7.6, 0.35, facecolor="#2A1F3D")
    ax.add_patch(th)
    headers = [(2.9, "Pass ID"), (3.9, "Resident"), (5.3, "Purpose"), (7.0, "Out / In Time"), (8.5, "Guardian SMS"), (9.6, "Action")]
    for x, txt in headers:
        ax.text(x, 4.48, txt, ha='left', fontsize=7.5, fontweight='bold', color='#FFFFFF')
        
    passes = [
        ("GP-8812", "Aaditya Yadav (6420)", "College Library", "17:00 - 21:00", "Verified ✓", "Approved"),
        ("GP-8814", "Sanskruti Malkar (6452)", "Medical Clinic Visit", "16:00 - 19:30", "Verified ✓", "Approved"),
        ("GP-8819", "Riya Kamat (6433)", "Weekend Home Visit", "Oct 25 - Oct 27", "Awaiting Call", "Approve / Reject"),
        ("GP-8822", "Pooja Sharma (6488)", "Late Project Lab", "19:00 - 22:00", "Parent Confirmed", "Approve / Reject")
    ]
    py = 3.9
    for pid, name, purp, tim, sms, act in passes:
        ax.text(2.9, py, pid, ha='left', fontsize=7.5, color='#334155')
        ax.text(3.9, py, name, ha='left', fontsize=7.5, fontweight='bold', color='#1E293B')
        ax.text(5.3, py, purp, ha='left', fontsize=7.2, color='#475569')
        ax.text(7.0, py, tim, ha='left', fontsize=7.2, color='#334155')
        ax.text(8.5, py, sms, ha='left', fontsize=7.2, fontweight='bold',
                color='#16A34A' if "Verified" in sms or "Confirmed" in sms else '#D97706')
        
        btn = patches.FancyBboxPatch((9.5, py-0.08), 0.85, 0.24, boxstyle="round,pad=0.02",
                                    facecolor="#EDE9FE" if "Approve" in act else "#DCFCE7",
                                    edgecolor="#7C3AED" if "Approve" in act else "#16A34A", linewidth=0.6)
        ax.add_patch(btn)
        ax.text(9.92, py+0.04, act.split("/")[0], ha='center', va='center', fontsize=6.8,
                color="#4C1D95" if "Approve" in act else "#14532D")
        ax.plot([2.8, 10.4], [py-0.12, py-0.12], color='#F1F5F9', lw=0.6)
        py -= 0.65
        
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig5_11_warden_passes.png", bbox_inches='tight')
    plt.close()

# 12. Warden Complaints
def gen_fig5_12_warden_complaints():
    fig, ax = setup_browser_canvas("Grievance Triage Portal", "/warden/complaints")
    draw_sidebar(ax, "Complaints", "Warden")
    
    c = patches.FancyBboxPatch((2.6, 0.6), 8.0, 4.6, boxstyle="round,pad=0.08",
                              facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(c)
    ax.text(2.8, 4.85, "Hostel Grievance Triage & Resolution Dashboard", ha='left', fontsize=10.5, fontweight='bold', color='#2A1F3D')
    
    th = patches.Rectangle((2.8, 4.3), 7.6, 0.35, facecolor="#2A1F3D")
    ax.add_patch(th)
    headers = [(2.9, "Ticket"), (4.0, "Category / Title"), (6.0, "Room"), (7.0, "Priority"), (8.1, "Assigned Staff"), (9.5, "Status")]
    for x, txt in headers:
        ax.text(x, 4.48, txt, ha='left', fontsize=7.5, fontweight='bold', color='#FFFFFF')
        
    complaints = [
        ("TKT-104", "Electrical: Ceiling Fan Noise", "204-B", "MEDIUM", "Ramesh (Elec)", "In-Progress"),
        ("TKT-105", "Water: Low geyser temp", "305-A", "HIGH", "Kalu (Plumber)", "Assigned"),
        ("TKT-106", "Wi-Fi: Drop in Room 102", "102-C", "LOW", "IT Support", "Open"),
        ("TKT-089", "Plumbing: Tap Washer", "204-B", "MEDIUM", "Kalu (Plumber)", "Resolved")
    ]
    cy = 3.9
    for tid, cat, rm, pri, staff, st in complaints:
        ax.text(2.9, cy, tid, ha='left', fontsize=7.5, color='#334155')
        ax.text(4.0, cy, cat, ha='left', fontsize=7.5, fontweight='bold', color='#1E293B')
        ax.text(6.0, cy, rm, ha='left', fontsize=7.2, color='#475569')
        ax.text(7.0, cy, pri, ha='left', fontsize=7.2, fontweight='bold',
                color='#DC2626' if pri=='HIGH' else '#D97706' if pri=='MEDIUM' else '#2563EB')
        ax.text(8.1, cy, staff, ha='left', fontsize=7.2, color='#334155')
        ax.text(9.5, cy, st, ha='left', fontsize=7.2, fontweight='bold',
                color='#16A34A' if st=='Resolved' else '#D97706')
        ax.plot([2.8, 10.4], [cy-0.12, cy-0.12], color='#F1F5F9', lw=0.6)
        cy -= 0.65
        
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig5_12_warden_complaints.png", bbox_inches='tight')
    plt.close()

# 13. Warden Mess Schedule
def gen_fig5_13_warden_mess():
    fig, ax = setup_browser_canvas("Mess Menu Publisher", "/warden/mess")
    draw_sidebar(ax, "Mess Schedule", "Warden")
    
    c = patches.FancyBboxPatch((2.6, 0.6), 8.0, 4.6, boxstyle="round,pad=0.08",
                              facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(c)
    ax.text(2.8, 4.85, "Mess Schedule Management & Special Meal Announcements", ha='left', fontsize=10.5, fontweight='bold', color='#2A1F3D')
    
    # Broadcast box
    bb = patches.FancyBboxPatch((2.8, 3.8), 7.6, 0.75, boxstyle="round,pad=0.06",
                               facecolor="#FEF3C7", edgecolor="#D97706", linewidth=1)
    ax.add_patch(bb)
    ax.text(3.0, 4.25, "[NOTICE] Publish Special Meal Notification to Residents", ha='left', fontsize=8.5, fontweight='bold', color='#78350F')
    ax.text(3.0, 4.0, "Upcoming Festival Feast: Diwali Special Grand Lunch on November 1st • Menu finalized with Mess Committee.", ha='left', fontsize=7.5, color='#92400E')
    
    # Weekly Edit Cards
    days = [("Monday", "Idli Sambar • Dal Makhani • Bhindi Masala"),
            ("Tuesday", "Poha • Chole Bhature • Veg Kadai"),
            ("Wednesday", "Upma • Rajma Chawal • Aloo Shimla"),
            ("Thursday", "Methi Thepla • Paneer Do Pyaza • Dal Tadka")]
    dy = 3.2
    for d, m in days:
        ax.text(2.9, dy, f"• {d}:", ha='left', fontsize=8, fontweight='bold', color='#2A1F3D')
        ax.text(4.4, dy, m, ha='left', fontsize=7.5, color='#334155')
        ax.text(10.2, dy, "[Edit Menu]", ha='right', fontsize=7, color='#2563EB')
        ax.plot([2.8, 10.4], [dy-0.12, dy-0.12], color='#F1F5F9', lw=0.6)
        dy -= 0.55
        
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig5_13_warden_mess.png", bbox_inches='tight')
    plt.close()

# 14. Admin Dashboard
def gen_fig5_14_admin_dash():
    fig, ax = setup_browser_canvas("Administrator Executive Command", "/admin/dashboard")
    draw_sidebar(ax, "Dashboard", "Admin")
    
    # KPI Grid
    kpis = [
        ("Total Capacity", "150 Beds", "#EDE9FE", "#6D28D9"),
        ("Active Residents", "142 Enrolled (95%)", "#DCFCE7", "#16A34A"),
        ("Monthly Dues", "Rs. 12,07,000 / Rs. 12,40,000", "#EFF6FF", "#2563EB"),
        ("SLA Resolution", "4.2 Hours Avg", "#FEF3C7", "#D97706")
    ]
    kx = 2.6
    for title, val, bg, col in kpis:
        card = patches.FancyBboxPatch((kx, 4.3), 1.85, 0.95, boxstyle="round,pad=0.06",
                                     facecolor=bg, edgecolor=col, linewidth=1)
        ax.add_patch(card)
        ax.text(kx+0.15, 4.95, title, ha='left', fontsize=7.2, color='#475569')
        ax.text(kx+0.15, 4.55, val, ha='left', fontsize=8.5, fontweight='bold', color=col)
        kx += 2.05
        
    # Occupancy by Wing Chart
    c1 = patches.FancyBboxPatch((2.6, 0.5), 4.2, 3.5, boxstyle="round,pad=0.08",
                               facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(c1)
    ax.text(2.8, 3.65, "Hostel Occupancy by Wing", ha='left', fontsize=9.5, fontweight='bold', color='#2A1F3D')
    
    wings = [("Wing A (North)", 48, 50), ("Wing B (South)", 46, 50), ("Wing C (East)", 48, 50)]
    wy = 3.1
    for wname, occ, cap in wings:
        ax.text(2.8, wy, f"{wname}: {occ}/{cap}", ha='left', fontsize=7.5, color='#334155')
        # Progress bar
        pbar_bg = patches.Rectangle((2.8, wy-0.28), 3.8, 0.16, facecolor="#E2E8F0")
        ax.add_patch(pbar_bg)
        pct = occ/cap
        pbar_fg = patches.Rectangle((2.8, wy-0.28), 3.8*pct, 0.16, facecolor="#4C1D95")
        ax.add_patch(pbar_fg)
        wy -= 0.65
        
    # Security & Audit Summary Right
    c2 = patches.FancyBboxPatch((7.0, 0.5), 3.6, 3.5, boxstyle="round,pad=0.08",
                               facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(c2)
    ax.text(7.2, 3.65, "Security & Compliance Log", ha='left', fontsize=9.5, fontweight='bold', color='#2A1F3D')
    
    events = [
        ("Automated Nightly Backup", "03:00 AM", "SUCCESS"),
        ("Curfew Lockdown Sealed", "09:30 PM", "ENFORCED"),
        ("Parent SMS Gate Gateway", "24/7", "ONLINE"),
        ("Database WAL Checkpoint", "12:00 PM", "HEALTHY")
    ]
    ey = 3.1
    for ev, t, st in events:
        ax.text(7.2, ey, ev, ha='left', fontsize=7.2, color='#1E293B')
        ax.text(7.2, ey-0.2, t, ha='left', fontsize=6.8, color='#64748B')
        ax.text(10.4, ey-0.1, st, ha='right', fontsize=7, fontweight='bold', color='#16A34A')
        ey -= 0.65
        
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig5_14_admin_dash.png", bbox_inches='tight')
    plt.close()

# 15. Admin Students Roster
def gen_fig5_15_admin_students():
    fig, ax = setup_browser_canvas("Resident Master Roster", "/admin/students")
    draw_sidebar(ax, "Student Roster", "Admin")
    
    c = patches.FancyBboxPatch((2.6, 0.6), 8.0, 4.6, boxstyle="round,pad=0.08",
                              facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(c)
    ax.text(2.8, 4.85, "Student Resident Directory & Enrollment Management", ha='left', fontsize=10.5, fontweight='bold', color='#2A1F3D')
    
    # Add Student Button
    abtn = patches.FancyBboxPatch((9.2, 4.75), 1.3, 0.35, boxstyle="round,pad=0.04",
                                 facecolor="#2A1F3D", edgecolor="#C5A880", linewidth=0.8)
    ax.add_patch(abtn)
    ax.text(9.85, 4.92, "+ Add Student", ha='center', va='center', fontsize=7.2, fontweight='bold', color='#FFFFFF')
    
    th = patches.Rectangle((2.8, 4.3), 7.6, 0.35, facecolor="#2A1F3D")
    ax.add_patch(th)
    headers = [(2.9, "Roll No"), (3.8, "Full Name"), (5.6, "Room"), (6.6, "Contact"), (8.0, "Guardian Phone"), (9.6, "Status")]
    for x, txt in headers:
        ax.text(x, 4.48, txt, ha='left', fontsize=7.5, fontweight='bold', color='#FFFFFF')
        
    students = [
        ("6420", "Aaditya Mangesh Yadav", "204-B (North)", "9876543210", "9820012345", "Active"),
        ("6452", "Sanskruti Amol Malkar", "204-A (North)", "9876543211", "9820012346", "Active"),
        ("6418", "Neha Ravindra Patil", "102-C (South)", "9876543212", "9820012347", "Active"),
        ("6488", "Pooja Suresh Sharma", "301-B (East)", "9876543213", "9820012348", "Active"),
        ("6491", "Kavita Ramesh Gupta", "205-A (North)", "9876543214", "9820012349", "Active")
    ]
    sy = 3.9
    for rno, name, rm, ph, gph, st in students:
        ax.text(2.9, sy, rno, ha='left', fontsize=7.5, color='#334155')
        ax.text(3.8, sy, name, ha='left', fontsize=7.5, fontweight='bold', color='#1E293B')
        ax.text(5.6, sy, rm, ha='left', fontsize=7.2, color='#475569')
        ax.text(6.6, sy, ph, ha='left', fontsize=7.2, color='#334155')
        ax.text(8.0, sy, gph, ha='left', fontsize=7.2, color='#334155')
        ax.text(9.6, sy, st, ha='left', fontsize=7.2, fontweight='bold', color='#16A34A')
        ax.plot([2.8, 10.4], [sy-0.12, sy-0.12], color='#F1F5F9', lw=0.6)
        sy -= 0.6
        
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig5_15_admin_students.png", bbox_inches='tight')
    plt.close()

# 16. Admin Room Allocation
def gen_fig5_16_admin_rooms():
    fig, ax = setup_browser_canvas("Room & Bed Inventory", "/admin/rooms")
    draw_sidebar(ax, "Room Allocation", "Admin")
    
    c = patches.FancyBboxPatch((2.6, 0.6), 8.0, 4.6, boxstyle="round,pad=0.08",
                              facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(c)
    ax.text(2.8, 4.85, "Room Allocation Matrix & Bed Occupancy Grid", ha='left', fontsize=10.5, fontweight='bold', color='#2A1F3D')
    
    # Room Cards Grid
    rooms = [
        ("Room 101 (Triple)", "South Wing", "3/3 Occupied", "#EFF6FF", "#2563EB"),
        ("Room 102 (Triple)", "South Wing", "2/3 (1 Vacant)", "#F0FDF4", "#16A34A"),
        ("Room 204 (Triple)", "North Wing", "3/3 Occupied", "#EFF6FF", "#2563EB"),
        ("Room 205 (Double)", "North Wing", "1/2 (1 Vacant)", "#F0FDF4", "#16A34A"),
        ("Room 301 (Triple)", "East Wing", "3/3 Occupied", "#EFF6FF", "#2563EB"),
        ("Room 302 (Single)", "East Wing", "Maintenance", "#FEF2F2", "#DC2626")
    ]
    rx = 2.8
    ry = 3.6
    for i, (r_name, wing, occ, bg, col) in enumerate(rooms):
        rcard = patches.FancyBboxPatch((rx, ry), 2.3, 0.9, boxstyle="round,pad=0.05",
                                      facecolor=bg, edgecolor=col, linewidth=1)
        ax.add_patch(rcard)
        ax.text(rx+0.15, ry+0.65, r_name, ha='left', fontsize=8, fontweight='bold', color='#1E293B')
        ax.text(rx+0.15, ry+0.4, wing, ha='left', fontsize=7.2, color='#64748B')
        ax.text(rx+0.15, ry+0.18, occ, ha='left', fontsize=7.5, fontweight='bold', color=col)
        rx += 2.6
        if i % 3 == 2:
            rx = 2.8
            ry -= 1.2
            
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig5_16_admin_rooms.png", bbox_inches='tight')
    plt.close()

# 17. Admin Financial Ledgers
def gen_fig5_17_admin_finances():
    fig, ax = setup_browser_canvas("Institutional Ledger", "/admin/finances")
    draw_sidebar(ax, "Financial Ledger", "Admin")
    
    c = patches.FancyBboxPatch((2.6, 0.6), 8.0, 4.6, boxstyle="round,pad=0.08",
                              facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(c)
    ax.text(2.8, 4.85, "Institutional Fee Ledgers & Financial Transaction Log", ha='left', fontsize=10.5, fontweight='bold', color='#2A1F3D')
    
    th = patches.Rectangle((2.8, 4.3), 7.6, 0.35, facecolor="#2A1F3D")
    ax.add_patch(th)
    headers = [(2.9, "Txn Ref"), (4.1, "Resident"), (5.8, "Fee Item"), (7.2, "Amount"), (8.4, "Date"), (9.5, "Status")]
    for x, txt in headers:
        ax.text(x, 4.48, txt, ha='left', fontsize=7.5, fontweight='bold', color='#FFFFFF')
        
    txns = [
        ("TXN-9021", "Aaditya Yadav (6420)", "Oct 2026 Rent", "Rs. 8,500.00", "2026-10-05", "SETTLED"),
        ("TXN-9022", "Sanskruti Malkar (6452)", "Oct 2026 Rent", "Rs. 8,500.00", "2026-10-05", "SETTLED"),
        ("TXN-9023", "Neha Patil (6418)", "Oct 2026 Rent", "Rs. 8,500.00", "2026-10-06", "SETTLED"),
        ("TXN-9024", "Pooja Sharma (6488)", "Oct 2026 Rent", "Rs. 8,500.00", "2026-10-08", "SETTLED"),
        ("TXN-9025", "Kavita Gupta (6491)", "Oct 2026 Rent", "Rs. 8,500.00", "Pending", "OVERDUE")
    ]
    ty = 3.9
    for ref, name, item, amt, dt, st in txns:
        ax.text(2.9, ty, ref, ha='left', fontsize=7.5, color='#334155')
        ax.text(4.1, ty, name, ha='left', fontsize=7.5, fontweight='bold', color='#1E293B')
        ax.text(5.8, ty, item, ha='left', fontsize=7.2, color='#475569')
        ax.text(7.2, ty, amt, ha='left', fontsize=7.2, fontweight='bold', color='#0F172A')
        ax.text(8.4, ty, dt, ha='left', fontsize=7.2, color='#334155')
        ax.text(9.5, ty, st, ha='left', fontsize=7.2, fontweight='bold',
                color='#16A34A' if st=='SETTLED' else '#DC2626')
        ax.plot([2.8, 10.4], [ty-0.12, ty-0.12], color='#F1F5F9', lw=0.6)
        ty -= 0.6
        
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig5_17_admin_finances.png", bbox_inches='tight')
    plt.close()

# 18. Admin Reports
def gen_fig5_18_admin_reports():
    fig, ax = setup_browser_canvas("Reports & CSV Export", "/admin/reports")
    draw_sidebar(ax, "Reports & CSV", "Admin")
    
    c = patches.FancyBboxPatch((2.6, 0.6), 8.0, 4.6, boxstyle="round,pad=0.08",
                              facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(c)
    ax.text(2.8, 4.85, "Analytical Reporting & Regulatory CSV Data Exporters", ha='left', fontsize=10.5, fontweight='bold', color='#2A1F3D')
    
    reports = [
        ("Monthly Curfew & Attendance Register", "Complete daily headcounts, out/in gate timestamps, and curfew breach logs.", "attendance_oct2026.csv"),
        ("Financial Fee Collection & Dues Ledger", "Itemized resident rent, mess breakdown, transaction reference numbers, and outstanding dues.", "finance_ledger_oct2026.csv"),
        ("Resident Grievance & SLA Resolution Audit", "Every complaint ticket, turnaround time, technician assigned, and resident sign-off.", "complaints_q3_2026.csv"),
        ("Hostel Student Master Directory", "Active roster with emergency phone contacts, blood group, allocated wing and bed number.", "student_directory_2026.csv")
    ]
    ry = 4.2
    for title, desc, fn in reports:
        rc = patches.FancyBboxPatch((2.8, ry-0.65), 7.6, 0.68, boxstyle="round,pad=0.04",
                                   facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=0.8)
        ax.add_patch(rc)
        ax.text(3.0, ry-0.15, title, ha='left', fontsize=8, fontweight='bold', color='#2A1F3D')
        ax.text(3.0, ry-0.42, desc, ha='left', fontsize=7, color='#64748B')
        
        ebtn = patches.FancyBboxPatch((9.1, ry-0.45), 1.2, 0.32, boxstyle="round,pad=0.03",
                                     facecolor="#16A34A", edgecolor="#14532D", linewidth=0.8)
        ax.add_patch(ebtn)
        ax.text(9.7, ry-0.29, "Export CSV v", ha='center', va='center', fontsize=7, fontweight='bold', color='#FFFFFF')
        ry -= 0.85
        
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig5_18_admin_reports.png", bbox_inches='tight')
    plt.close()

# 19. Admin Audit Trail
def gen_fig5_19_admin_audit():
    fig, ax = setup_browser_canvas("Security Audit Trail", "/admin/audit")
    draw_sidebar(ax, "Audit Trail", "Admin")
    
    c = patches.FancyBboxPatch((2.6, 0.6), 8.0, 4.6, boxstyle="round,pad=0.08",
                              facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(c)
    ax.text(2.8, 4.85, "System-Wide Security Audit Trail & Immutable Activity Log", ha='left', fontsize=10.5, fontweight='bold', color='#2A1F3D')
    
    th = patches.Rectangle((2.8, 4.3), 7.6, 0.35, facecolor="#2A1F3D")
    ax.add_patch(th)
    headers = [(2.9, "Timestamp"), (4.2, "User / Role"), (5.7, "Event Action"), (7.5, "IP Address"), (8.9, "Status")]
    for x, txt in headers:
        ax.text(x, 4.48, txt, ha='left', fontsize=7.5, fontweight='bold', color='#FFFFFF')
        
    logs = [
        ("2026-10-25 18:45:12", "Warden (Aditi P.)", "GATE_SCAN_VERIFIED", "192.168.1.10", "SUCCESS"),
        ("2026-10-25 18:40:05", "Student (6420)", "GATE_PASS_APPROVED_QR", "192.168.1.44", "SUCCESS"),
        ("2026-10-25 17:15:20", "Admin (Root)", "DATABASE_BACKUP_SNAPSHOT", "127.0.0.1", "SUCCESS"),
        ("2026-10-25 16:30:11", "Student (6452)", "COMPLAINT_FILED (TKT-104)", "192.168.1.52", "SUCCESS"),
        ("2026-10-25 15:10:00", "System Daemon", "WAL_CHECKPOINT_PASS", "127.0.0.1", "SUCCESS")
    ]
    ly = 3.9
    for ts, u, ev, ip, st in logs:
        ax.text(2.9, ly, ts, ha='left', fontsize=7.2, color='#334155')
        ax.text(4.2, ly, u, ha='left', fontsize=7.2, fontweight='bold', color='#1E293B')
        ax.text(5.7, ly, ev, ha='left', fontsize=7.2, color='#4C1D95')
        ax.text(7.5, ly, ip, ha='left', fontsize=7.2, color='#64748B')
        ax.text(8.9, ly, st, ha='left', fontsize=7.2, fontweight='bold', color='#16A34A')
        ax.plot([2.8, 10.4], [ly-0.12, ly-0.12], color='#F1F5F9', lw=0.6)
        ly -= 0.6
        
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig5_19_admin_audit.png", bbox_inches='tight')
    plt.close()

# 20. Admin Settings
def gen_fig5_20_admin_settings():
    fig, ax = setup_browser_canvas("System Settings & Maintenance", "/admin/settings")
    draw_sidebar(ax, "Settings", "Admin")
    
    c = patches.FancyBboxPatch((2.6, 0.6), 8.0, 4.6, boxstyle="round,pad=0.08",
                              facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1)
    ax.add_patch(c)
    ax.text(2.8, 4.85, "System Settings, Maintenance & Database Backup Engine", ha='left', fontsize=10.5, fontweight='bold', color='#2A1F3D')
    
    # Curfew Configuration Card
    c1 = patches.FancyBboxPatch((2.8, 3.2), 3.6, 1.3, boxstyle="round,pad=0.05",
                               facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=0.8)
    ax.add_patch(c1)
    ax.text(3.0, 4.25, "Nightly Curfew Configuration", ha='left', fontsize=8.5, fontweight='bold', color='#2A1F3D')
    ax.text(3.0, 3.95, "Mandatory Entry Cutoff: 09:30 PM", ha='left', fontsize=7.5, color='#334155')
    ax.text(3.0, 3.65, "Grace Period: 10 minutes", ha='left', fontsize=7.5, color='#334155')
    ax.text(3.0, 3.35, "Curfew Status: STRICT ACTIVE", ha='left', fontsize=7.5, fontweight='bold', color='#16A34A')
    
    # Online Backup Card
    c2 = patches.FancyBboxPatch((6.8, 3.2), 3.6, 1.3, boxstyle="round,pad=0.05",
                               facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=0.8)
    ax.add_patch(c2)
    ax.text(7.0, 4.25, "Online Database Snapshot Engine", ha='left', fontsize=8.5, fontweight='bold', color='#2A1F3D')
    ax.text(7.0, 3.95, "Storage: SQLite 3 (WAL Mode Active)", ha='left', fontsize=7.5, color='#334155')
    ax.text(7.0, 3.65, "Last Backup: Today 17:15 (hostel_backup.db)", ha='left', fontsize=7.5, color='#334155')
    bbtn = patches.FancyBboxPatch((7.0, 3.3), 3.2, 0.28, boxstyle="round,pad=0.03",
                                 facecolor="#2A1F3D", edgecolor="#C5A880", linewidth=0.8)
    ax.add_patch(bbtn)
    ax.text(8.6, 3.44, "Trigger Live Online Snapshot Now", ha='center', va='center', fontsize=7, fontweight='bold', color='#FFFFFF')
    
    # System Diagnostic & Health
    ax.text(2.8, 2.8, "System Diagnostics & Services Status", ha='left', fontsize=9.5, fontweight='bold', color='#2A1F3D')
    services = [
        ("Python Flask Backend Server", "Port 5000", "RUNNING", "#16A34A"),
        ("SQLite WAL Journal Concurrency", "Zero Locks", "HEALTHY", "#16A34A"),
        ("SMS Notification Gateway", "Twilio API Mock", "READY", "#16A34A"),
        ("Optical QR Scanner Core", "Client-Side WASM", "ACTIVE", "#16A34A")
    ]
    sy = 2.45
    for s_name, port, st, col in services:
        ax.text(2.9, sy, s_name, ha='left', fontsize=7.5, color='#1E293B')
        ax.text(6.0, sy, port, ha='left', fontsize=7.2, color='#64748B')
        ax.text(10.2, sy, st, ha='right', fontsize=7.2, fontweight='bold', color=col)
        ax.plot([2.8, 10.4], [sy-0.1, sy-0.1], color='#F1F5F9', lw=0.6)
        sy -= 0.42
        
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/fig5_20_admin_settings.png", bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    print("Generating Chapter 5 UI screen snapshots...")
    gen_fig5_1_login()
    gen_fig5_2_student_dash()
    gen_fig5_3_student_profile()
    gen_fig5_4_student_gatepass()
    gen_fig5_5_student_complaint()
    gen_fig5_6_student_payments()
    gen_fig5_7_student_mess()
    gen_fig5_8_warden_dash()
    gen_fig5_9_warden_attendance()
    gen_fig5_10_warden_scanner()
    gen_fig5_11_warden_passes()
    gen_fig5_12_warden_complaints()
    gen_fig5_13_warden_mess()
    gen_fig5_14_admin_dash()
    gen_fig5_15_admin_students()
    gen_fig5_16_admin_rooms()
    gen_fig5_17_admin_finances()
    gen_fig5_18_admin_reports()
    gen_fig5_19_admin_audit()
    gen_fig5_20_admin_settings()
    print("All 20 Chapter 5 UI screen snapshots generated successfully!")
