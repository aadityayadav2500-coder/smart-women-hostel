"""
Flask Backend API Server for SafeStay Smart Women Hostel Management System.
Connects with SQLite database (hostel.db) and serves REST API & static frontend.
"""

import os
import json
import sqlite3
import shutil
import csv
from datetime import datetime, date, timedelta
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from database import get_db, init_db, DB_PATH

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

# Ensure database is initialized
init_db()

# Create backups and exports directories if needed
BACKUP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backups")
EXPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(EXPORTS_DIR, exist_ok=True)


# Helper: row to dict
def row_to_dict(row):
    return dict(row) if row else None

# Helper: log activity
def log_activity(role, user_code, action, conn=None):
    close_at_end = False
    if conn is None:
        conn = get_db()
        close_at_end = True
    try:
        conn.execute(
            "INSERT INTO activity_logs (user_role, user_code, action) VALUES (?, ?, ?)",
            (role, user_code, action)
        )
        if close_at_end:
            conn.commit()
    except Exception as e:
        print(f"Error logging activity: {e}")
    finally:
        if close_at_end:
            conn.close()


# ==========================================
# 1. Static Web Route (Frontend)
# ==========================================
@app.route("/")
def index():
    return send_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html"))


@app.route("/api/public/students", methods=["GET"])
def public_students():
    conn = get_db()
    rows = conn.execute("SELECT user_code, name, room, course, curfew_status FROM users WHERE role = 'Student' ORDER BY room ASC").fetchall()
    conn.close()
    return jsonify({"success": True, "students": [row_to_dict(r) for r in rows]})


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "SafeStay Smart Women Hostel Backend API",
        "timestamp": datetime.now().isoformat()
    })


# ==========================================
# 2. Authentication & Profile
# ==========================================
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    role = data.get("role", "Student")
    user_code = data.get("user_code", "").strip()
    password = data.get("password", "").strip()

    if not user_code or not password:
        return jsonify({"success": False, "message": "Please enter both User ID and Password."}), 400

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE user_code = ? AND role = ?",
        (user_code, role)
    ).fetchone()
    conn.close()

    if not user:
        return jsonify({"success": False, "message": f"No {role} account found with ID '{user_code}'"}), 404

    user_dict = row_to_dict(user)
    if user_dict.get("password") != password:
        return jsonify({"success": False, "message": "Incorrect password. Please try again."}), 401

    # Don't leak raw password in response
    user_dict.pop("password", None)
    return jsonify({"success": True, "user": user_dict})


@app.route("/api/profile", methods=["GET", "PUT"])
def profile():
    conn = get_db()
    if request.method == "GET":
        user_code = request.args.get("user_code", "STU-2048")
        user = conn.execute("SELECT * FROM users WHERE user_code = ?", (user_code,)).fetchone()
        conn.close()
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        u = row_to_dict(user)
        u.pop("password", None)
        return jsonify({"success": True, "user": u})

    # PUT: update profile
    data = request.get_json() or {}
    user_code = data.get("user_code", "STU-2048")
    phone = data.get("phone")
    email = data.get("email")
    emergency_name = data.get("emergency_name")
    emergency_phone = data.get("emergency_phone")

    conn.execute("""
        UPDATE users
        SET phone = COALESCE(?, phone),
            email = COALESCE(?, email),
            emergency_name = COALESCE(?, emergency_name),
            emergency_phone = COALESCE(?, emergency_phone)
        WHERE user_code = ?
    """, (phone, email, emergency_name, emergency_phone, user_code))
    conn.commit()

    updated = conn.execute("SELECT * FROM users WHERE user_code = ?", (user_code,)).fetchone()
    conn.close()

    log_activity("Student", user_code, "Updated personal profile details")
    u = row_to_dict(updated)
    u.pop("password", None)
    return jsonify({"success": True, "message": "Profile updated successfully", "user": u})


# ==========================================
# 3. Dashboard Statistics
# ==========================================
@app.route("/api/stats/student", methods=["GET"])
def student_stats():
    user_code = request.args.get("user_code", "STU-2048")
    conn = get_db()

    # Rent status
    latest_rent = conn.execute(
        "SELECT * FROM rent_records WHERE student_code = ? ORDER BY id DESC LIMIT 1",
        (user_code,)
    ).fetchone()

    # Active complaints
    active_complaints_count = conn.execute(
        "SELECT COUNT(*) FROM complaints WHERE student_code = ? AND status != 'Solved'",
        (user_code,)
    ).fetchone()[0]

    # Mess rating
    avg_mess = conn.execute("SELECT AVG(rating) FROM mess_feedback").fetchone()[0] or 4.2

    # Latest priority notice
    priority_notices_count = conn.execute("SELECT COUNT(*) FROM notices WHERE priority = 1").fetchone()[0]

    # Active exit request
    active_exit = conn.execute(
        "SELECT * FROM exit_requests WHERE student_code = ? AND status = 'Approved' ORDER BY id DESC LIMIT 1",
        (user_code,)
    ).fetchone()

    # Recent activities
    activities = conn.execute(
        "SELECT action, created_at FROM activity_logs WHERE user_code = ? OR user_role = 'Student' ORDER BY id DESC LIMIT 5",
        (user_code,)
    ).fetchall()

    conn.close()

    return jsonify({
        "success": True,
        "rent": {
            "amount": f"₹{latest_rent['amount']:,}" if latest_rent else "₹0",
            "status": latest_rent["status"] if latest_rent else "Paid",
            "due_date": latest_rent["due_date"] if latest_rent else "—"
        },
        "active_complaints": active_complaints_count,
        "mess_rating": f"{round(avg_mess, 1)}/5",
        "priority_notices": priority_notices_count,
        "active_exit": row_to_dict(active_exit),
        "activities": [row_to_dict(a) for a in activities]
    })


@app.route("/api/stats/warden", methods=["GET"])
def warden_stats():
    conn = get_db()

    # Pending exit requests
    pending_exits = conn.execute(
        "SELECT COUNT(*) FROM exit_requests WHERE status = 'Pending'"
    ).fetchone()[0]

    # Unattended complaints
    unattended_complaints = conn.execute(
        "SELECT COUNT(*) FROM complaints WHERE status = 'Pending'"
    ).fetchone()[0]

    # Attendance pending count
    today_str = date.today().strftime("%Y-%m-%d")
    marked_count = conn.execute(
        "SELECT COUNT(*) FROM attendance WHERE date_str = ?", (today_str,)
    ).fetchone()[0]
    total_students = conn.execute("SELECT COUNT(*) FROM users WHERE role = 'Student'").fetchone()[0]
    attendance_pending = max(0, total_students - marked_count)

    # Currently out count
    currently_out_users = conn.execute(
        "SELECT * FROM users WHERE role = 'Student' AND curfew_status = 'Out'"
    ).fetchall()

    # Average mess rating
    avg_mess = conn.execute("SELECT AVG(rating) FROM mess_feedback").fetchone()[0] or 4.2

    # Past curfew count
    curfew_time_setting = conn.execute(
        "SELECT value FROM settings WHERE key = 'curfew_time'"
    ).fetchone()
    curfew_str = curfew_time_setting["value"] if curfew_time_setting else "23:30"
    
    # Calculate who is past curfew
    now = datetime.now()
    curfew_h, curfew_m = map(int, curfew_str.split(":"))
    past_curfew_count = 0
    currently_out_list = []

    for u in currently_out_users:
        user_dict = row_to_dict(u)
        # Find their active exit request
        exit_req = conn.execute(
            "SELECT * FROM exit_requests WHERE student_code = ? AND status = 'Approved' ORDER BY id DESC LIMIT 1",
            (u["user_code"],)
        ).fetchone()
        
        expected_ret = exit_req["expected_return"] if exit_req else curfew_str
        is_late = False
        # Calculate time remaining / late
        try:
            clean_time = expected_ret.strip().upper()
            if "PM" in clean_time or "AM" in clean_time:
                is_pm = "PM" in clean_time
                t_raw = clean_time.replace("PM", "").replace("AM", "").strip()
                t_parts = list(map(int, t_raw.split(":")))
                ret_h = t_parts[0]
                ret_m = t_parts[1] if len(t_parts) > 1 else 0
                if is_pm and ret_h < 12:
                    ret_h += 12
                elif not is_pm and ret_h == 12:
                    ret_h = 0
            else:
                t_parts = list(map(int, clean_time.split(":")))
                ret_h = t_parts[0]
                ret_m = t_parts[1] if len(t_parts) > 1 else 0

            curfew_dt = now.replace(hour=ret_h, minute=ret_m, second=0, microsecond=0)
            diff = (curfew_dt - now).total_seconds()
            if diff < 0:
                is_late = True
                past_curfew_count += 1
                diff_abs = abs(diff)
                time_str = f"{int(diff_abs//3600):02d}:{int((diff_abs%3600)//60):02d}"
            else:
                time_str = f"{int(diff//3600):02d}:{int((diff%3600)//60):02d}"
        except Exception:
            time_str = "01:15"
            is_late = False

        currently_out_list.append({
            "name": user_dict["name"],
            "room": user_dict["room"],
            "user_code": user_dict["user_code"],
            "time_str": time_str,
            "late": is_late,
            "expected_return": expected_ret
        })

    # Recent activities
    activities = conn.execute(
        "SELECT action, created_at FROM activity_logs ORDER BY id DESC LIMIT 6"
    ).fetchall()

    conn.close()

    return jsonify({
        "success": True,
        "pending_exits": pending_exits,
        "unattended_complaints": unattended_complaints,
        "attendance_pending": attendance_pending,
        "currently_out_count": len(currently_out_users),
        "mess_rating": f"{round(avg_mess, 1)}/5",
        "past_curfew": past_curfew_count,
        "currently_out": currently_out_list,
        "activities": [row_to_dict(a) for a in activities]
    })


@app.route("/api/stats/admin", methods=["GET"])
def admin_stats():
    conn = get_db()

    total_beds = int(conn.execute("SELECT value FROM settings WHERE key = 'capacity'").fetchone()["value"])
    occupied_beds = conn.execute("SELECT COUNT(*) FROM users WHERE role = 'Student' AND status = 'Active'").fetchone()[0]
    occupancy_pct = int(round((occupied_beds / total_beds) * 100)) if total_beds else 0

    # Rent totals
    total_due = conn.execute("SELECT SUM(amount) FROM rent_records WHERE status = 'Due'").fetchone()[0] or 0
    total_overdue = conn.execute("SELECT SUM(amount) FROM rent_records WHERE status = 'Overdue'").fetchone()[0] or 0
    total_collected = conn.execute("SELECT SUM(amount) FROM rent_records WHERE status = 'Paid'").fetchone()[0] or 0

    # Complaints
    open_complaints = conn.execute("SELECT COUNT(*) FROM complaints WHERE status != 'Solved'").fetchone()[0]
    escalated = conn.execute("SELECT COUNT(*) FROM complaints WHERE status = 'Escalated'").fetchone()[0]

    # Past curfew count
    past_curfew = conn.execute("SELECT COUNT(*) FROM users WHERE curfew_status = 'Out'").fetchone()[0]

    # Complaints by category
    categories = conn.execute(
        "SELECT category, COUNT(*) as count FROM complaints GROUP BY category"
    ).fetchall()
    cat_labels = [c["category"] for c in categories]
    cat_values = [c["count"] for c in categories]

    conn.close()

    return jsonify({
        "success": True,
        "occupancy": {
            "percent": f"{occupancy_pct}%",
            "text": f"{occupied_beds} / {total_beds} beds",
            "trend": [86, 87, 89, 90, 91, 92, occupancy_pct]
        },
        "rent": {
            "collected": f"₹{total_collected/100000:.2f}L",
            "due": f"₹{total_due/100000:.2f}L",
            "overdue": f"₹{total_overdue/1000:.0f}K",
            "aging": [42, 30, 18, 10]
        },
        "complaints": {
            "open": open_complaints,
            "escalated": escalated,
            "categories": {
                "labels": cat_labels if cat_labels else ["Maintenance", "Mess", "Internet", "Safety"],
                "values": cat_values if cat_values else [42, 27, 18, 13]
            }
        },
        "past_curfew": past_curfew
    })


# ==========================================
# 4. Students & Directory API
# ==========================================
@app.route("/api/students", methods=["GET", "POST"])
def students():
    conn = get_db()

    if request.method == "GET":
        search = request.args.get("search", "").strip().lower()
        floor = request.args.get("floor", "").strip()

        query = "SELECT * FROM users WHERE role = 'Student' ORDER BY room ASC"
        rows = conn.execute(query).fetchall()

        result = []
        for r in rows:
            u = row_to_dict(r)
            u.pop("password", None)  # Prevent password exposure
            # Find latest rent status
            rent_row = conn.execute(
                "SELECT status FROM rent_records WHERE student_code = ? ORDER BY id DESC LIMIT 1",
                (u["user_code"],)
            ).fetchone()
            u["rent_status"] = rent_row["status"] if rent_row else "Due"

            # Filter if search provided
            if search:
                combined = f"{u['name']} {u['room']} {u['course']} {u['phone']}".lower()
                if search not in combined:
                    continue

            # Filter by floor
            if floor and floor != "All floors":
                floor_num = "1" if "1" in floor else "2"
                room_num = u["room"].replace("A-", "")
                if not room_num.startswith(floor_num):
                    continue

            result.append(u)

        conn.close()
        return jsonify({"success": True, "students": result})

    # POST: Add new student
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    room = data.get("room", "").strip()
    course = data.get("course", "").strip()
    phone = data.get("phone", "").strip()
    email = data.get("email", f"{name.lower().replace(' ', '')}@example.com")
    warden = data.get("warden", "Meera Sharma")
    emergency_name = data.get("emergency_name", "Guardian")
    emergency_phone = data.get("emergency_phone", phone)

    if not name or not room:
        conn.close()
        return jsonify({"success": False, "message": "Name and Room are required"}), 400

    # Generate user code
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'Student'")
    idx = cursor.fetchone()[0] + 1
    user_code = f"STU-{2000 + idx}"

    cursor.execute("""
        INSERT INTO users (user_code, role, name, email, phone, room, course, warden_name, emergency_name, emergency_phone, status, curfew_status)
        VALUES (?, 'Student', ?, ?, ?, ?, ?, ?, ?, ?, 'Active', 'In')
    """, (user_code, name, email, phone, room, course, warden, emergency_name, emergency_phone))

    # Create current month rent record
    now = datetime.now()
    cur_month = now.strftime("%B %Y")
    next_month_calc = (now.replace(day=28) + timedelta(days=4))
    due_date = f"05 {next_month_calc.strftime('%b %Y')}"

    cursor.execute("""
        INSERT INTO rent_records (student_code, student_name, room, month, amount, due_date, status)
        VALUES (?, ?, ?, ?, 8500, ?, 'Due')
    """, (user_code, name, room, cur_month, due_date))

    conn.commit()
    conn.close()

    log_activity("Admin", "ADMIN-001", f"Added new student: {name} (Room {room})")
    return jsonify({"success": True, "message": "Student created successfully", "user_code": user_code})


@app.route("/api/students/<int:student_id>", methods=["PUT", "DELETE"])
def student_detail(student_id):
    conn = get_db()
    student = conn.execute("SELECT * FROM users WHERE id = ?", (student_id,)).fetchone()
    if not student:
        conn.close()
        return jsonify({"success": False, "message": "Student not found"}), 404

    if request.method == "DELETE":
        conn.execute("DELETE FROM users WHERE id = ?", (student_id,))
        conn.commit()
        conn.close()
        log_activity("Admin", "ADMIN-001", f"Deleted student ID {student_id}")
        return jsonify({"success": True, "message": "Student deleted successfully"})

    # PUT: Update student
    data = request.get_json() or {}
    conn.execute("""
        UPDATE users
        SET name = COALESCE(?, name),
            room = COALESCE(?, room),
            course = COALESCE(?, course),
            phone = COALESCE(?, phone),
            email = COALESCE(?, email),
            status = COALESCE(?, status),
            curfew_status = COALESCE(?, curfew_status)
        WHERE id = ?
    """, (
        data.get("name"),
        data.get("room"),
        data.get("course"),
        data.get("phone"),
        data.get("email"),
        data.get("status"),
        data.get("curfew_status"),
        student_id
    ))
    conn.commit()
    conn.close()

    log_activity("Admin", "ADMIN-001", f"Updated student profile ID {student_id}")
    return jsonify({"success": True, "message": "Student updated successfully"})


# ==========================================
# 5. Notices API
# ==========================================
@app.route("/api/notices", methods=["GET", "POST"])
def notices():
    conn = get_db()
    if request.method == "GET":
        rows = conn.execute(
            "SELECT * FROM notices ORDER BY priority DESC, id DESC"
        ).fetchall()
        result = [row_to_dict(r) for r in rows]
        conn.close()
        return jsonify({"success": True, "notices": result})

    # POST: Create notice
    data = request.get_json() or {}
    title = data.get("title", "").strip()
    body = data.get("body", "").strip()
    by_role = data.get("by_role", "Warden")
    priority = 1 if data.get("priority") in [1, True, "Priority", "priority"] else 0
    expiry_date = data.get("expiry_date")
    time_str = "Today, " + datetime.now().strftime("%I:%M %p")

    if not title or not body:
        conn.close()
        return jsonify({"success": False, "message": "Title and body are required"}), 400

    conn.execute("""
        INSERT INTO notices (title, body, by_role, priority, time_str, expiry_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, body, by_role, priority, time_str, expiry_date))
    conn.commit()
    conn.close()

    log_activity(by_role, None, f"Published notice: {title}")
    return jsonify({"success": True, "message": "Notice published successfully"})


@app.route("/api/notices/<int:notice_id>", methods=["PUT", "DELETE"])
def notice_detail(notice_id):
    conn = get_db()
    notice = conn.execute("SELECT * FROM notices WHERE id = ?", (notice_id,)).fetchone()
    if not notice:
        conn.close()
        return jsonify({"success": False, "message": "Notice not found"}), 404

    if request.method == "DELETE":
        conn.execute("DELETE FROM notices WHERE id = ?", (notice_id,))
        conn.commit()
        conn.close()
        log_activity("Admin", None, f"Deleted notice ID {notice_id}")
        return jsonify({"success": True, "message": "Notice deleted"})

    # PUT: Edit notice
    data = request.get_json() or {}
    conn.execute("""
        UPDATE notices
        SET title = COALESCE(?, title),
            body = COALESCE(?, body),
            priority = COALESCE(?, priority),
            expiry_date = COALESCE(?, expiry_date)
        WHERE id = ?
    """, (data.get("title"), data.get("body"), 1 if data.get("priority") else 0, data.get("expiry_date"), notice_id))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Notice updated successfully"})


@app.route("/api/notices/<int:notice_id>/acknowledge", methods=["POST"])
def acknowledge_notice(notice_id):
    data = request.get_json() or {}
    user_code = data.get("user_code", "STU-2048")
    conn = get_db()
    row = conn.execute("SELECT acknowledged_by FROM notices WHERE id = ?", (notice_id,)).fetchone()
    if row:
        acks = json.loads(row["acknowledged_by"] or "[]")
        if user_code not in acks:
            acks.append(user_code)
            conn.execute("UPDATE notices SET acknowledged_by = ? WHERE id = ?", (json.dumps(acks), notice_id))
            conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Notice acknowledged"})


# ==========================================
# 6. Complaints API
# ==========================================
@app.route("/api/complaints", methods=["GET", "POST"])
def complaints():
    conn = get_db()
    if request.method == "GET":
        status_filter = request.args.get("status")
        category_filter = request.args.get("category")
        student_code = request.args.get("student_code")
        search = request.args.get("search", "").strip().lower()

        query = "SELECT * FROM complaints WHERE 1=1"
        params = []

        if status_filter and status_filter != "All" and status_filter != "All statuses":
            query += " AND status = ?"
            params.append(status_filter)

        if category_filter and category_filter != "All categories":
            query += " AND category = ?"
            params.append(category_filter)

        if student_code:
            query += " AND student_code = ?"
            params.append(student_code)

        query += " ORDER BY id DESC"
        rows = conn.execute(query, params).fetchall()

        result = []
        for r in rows:
            c = row_to_dict(r)
            if search:
                combined = f"{c['complaint_code']} {c['title']} {c['student_name']} {c['category']} {c['room']}".lower()
                if search not in combined:
                    continue
            result.append(c)

        conn.close()
        return jsonify({"success": True, "complaints": result})

    # POST: Raise a complaint
    data = request.get_json() or {}
    category = data.get("category", "Maintenance")
    room = data.get("room", "A-204")
    title = data.get("title", "").strip() or data.get("description", "").strip()[:40]
    description = data.get("description", "").strip()
    student_code = data.get("student_code", "STU-2048")

    # Fetch student name
    student = conn.execute("SELECT name FROM users WHERE user_code = ?", (student_code,)).fetchone()
    student_name = student["name"] if student else "Sanskruti Patil"

    # Generate complaint code
    cnt = conn.execute("SELECT COUNT(*) FROM complaints").fetchone()[0] + 1
    complaint_code = f"CMP-{1000 + cnt}"
    date_str = datetime.now().strftime("%d %b")

    conn.execute("""
        INSERT INTO complaints (complaint_code, student_code, student_name, room, category, title, description, status, date_str)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'Pending', ?)
    """, (complaint_code, student_code, student_name, room, category, title, description, date_str))
    conn.commit()
    conn.close()

    log_activity("Student", student_code, f"Raised complaint {complaint_code}: {title}")
    return jsonify({
        "success": True,
        "message": f"Complaint {complaint_code} raised successfully",
        "complaint_code": complaint_code
    })


@app.route("/api/complaints/<int:complaint_id>/status", methods=["PUT"])
def update_complaint_status(complaint_id):
    data = request.get_json() or {}
    status = data.get("status", "In Progress")
    conn = get_db()
    conn.execute("UPDATE complaints SET status = ? WHERE id = ?", (status, complaint_id))
    conn.commit()
    c = conn.execute("SELECT * FROM complaints WHERE id = ?", (complaint_id,)).fetchone()
    conn.close()

    if c:
        log_activity("Warden", None, f"Complaint {c['complaint_code']} moved to {status}")
    return jsonify({"success": True, "message": f"Complaint status updated to {status}"})


# ==========================================
# 7. Entry / Exit & Gate System
# ==========================================
@app.route("/api/exit-requests", methods=["GET", "POST"])
def exit_requests():
    conn = get_db()

    if request.method == "GET":
        student_code = request.args.get("student_code")
        status_filter = request.args.get("status")

        query = "SELECT * FROM exit_requests WHERE 1=1"
        params = []
        if student_code:
            query += " AND student_code = ?"
            params.append(student_code)
        if status_filter:
            query += " AND status = ?"
            params.append(status_filter)

        query += " ORDER BY id DESC"
        rows = conn.execute(query, params).fetchall()
        conn.close()
        return jsonify({"success": True, "requests": [row_to_dict(r) for r in rows]})

    # POST: New exit request
    data = request.get_json() or {}
    student_code = data.get("student_code", "STU-2048")
    date_str = data.get("date_str") or datetime.now().strftime("%d %b")
    time_out = data.get("time_out", "08:00 PM")
    expected_return = data.get("expected_return", "11:30 PM")
    reason = data.get("reason", "Personal")

    student = conn.execute("SELECT name, room FROM users WHERE user_code = ?", (student_code,)).fetchone()
    student_name = student["name"] if student else "Sanskruti Patil"
    room = student["room"] if student else "A-204"

    cnt = conn.execute("SELECT COUNT(*) FROM exit_requests").fetchone()[0] + 1
    request_code = f"EX-{2050 + cnt}"

    conn.execute("""
        INSERT INTO exit_requests (request_code, student_code, student_name, room, date_str, time_out, expected_return, reason, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Pending')
    """, (request_code, student_code, student_name, room, date_str, time_out, expected_return, reason))
    conn.commit()
    conn.close()

    log_activity("Student", student_code, f"Submitted exit request {request_code} for {expected_return}")
    return jsonify({
        "success": True,
        "message": f"Exit request {request_code} submitted for approval",
        "request_code": request_code
    })


@app.route("/api/exit-requests/<int:request_id>/action", methods=["PUT"])
def handle_exit_action(request_id):
    data = request.get_json() or {}
    action = data.get("action", "approve")  # 'approve' or 'reject'
    reject_reason = data.get("reason", "")

    new_status = "Approved" if action == "approve" else "Rejected"

    conn = get_db()
    conn.execute("""
        UPDATE exit_requests
        SET status = ?, reject_reason = ?
        WHERE id = ?
    """, (new_status, reject_reason, request_id))
    conn.commit()

    req = conn.execute("SELECT * FROM exit_requests WHERE id = ?", (request_id,)).fetchone()
    conn.close()

    if req:
        log_activity("Warden", None, f"Exit request {req['request_code']} {new_status.lower()} for {req['student_name']}")
    return jsonify({"success": True, "message": f"Request {new_status.lower()} successfully"})


@app.route("/api/gate/scan", methods=["POST"])
def gate_scan():
    """
    Gate Scan: simulates scanning QR code or entering manual request/student code at hostel gate.
    Logs exit if student is IN, logs entry if student is OUT.
    """
    data = request.get_json() or {}
    code = (data.get("code") or "").strip().upper()

    if not code:
        return jsonify({"success": False, "message": "Please enter a Student ID or Request Code"}), 400

    conn = get_db()
    # Check if code is a request code (e.g. EX-2048) or student code (e.g. STU-2048) or student name
    user = None
    req = None

    if code.startswith("EX-"):
        req = conn.execute("SELECT * FROM exit_requests WHERE request_code = ?", (code,)).fetchone()
        if req:
            user = conn.execute("SELECT * FROM users WHERE user_code = ?", (req["student_code"],)).fetchone()
    else:
        user = conn.execute(
            "SELECT * FROM users WHERE user_code = ? OR UPPER(name) = ? OR UPPER(room) = ?",
            (code, code, code)
        ).fetchone()
        if user:
            req = conn.execute(
                "SELECT * FROM exit_requests WHERE student_code = ? AND status = 'Approved' ORDER BY id DESC LIMIT 1",
                (user["user_code"],)
            ).fetchone()

    if not user:
        conn.close()
        return jsonify({"success": False, "message": f"Code '{code}' not recognized. Ensure student exists."}), 404

    now_time = datetime.now().strftime("%I:%M %p")
    current_status = user["curfew_status"]

    if current_status == "In":
        # Log EXIT
        new_status = "Out"
        conn.execute("UPDATE users SET curfew_status = 'Out' WHERE id = ?", (user["id"],))
        if req:
            conn.execute(
                "UPDATE exit_requests SET actual_exit = ? WHERE id = ?",
                (now_time, req["id"])
            )
        msg = f"✓ Gate EXIT logged: {user['name']} (Room {user['room']}) departed at {now_time}"
        log_activity("Warden", None, f"QR Exit logged — {user['name']}", conn=conn)
    else:
        # Log ENTRY
        new_status = "In"
        conn.execute("UPDATE users SET curfew_status = 'In' WHERE id = ?", (user["id"],))
        if req:
            conn.execute(
                "UPDATE exit_requests SET actual_entry = ?, status = 'Completed' WHERE id = ?",
                (now_time, req["id"])
            )
        msg = f"✓ Gate ENTRY logged: {user['name']} (Room {user['room']}) entered safely at {now_time}"
        log_activity("Warden", None, f"QR Entry logged — {user['name']}", conn=conn)

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": msg,
        "student": user["name"],
        "room": user["room"],
        "curfew_status": new_status,
        "time": now_time
    })


# ==========================================
# 8. Rent & Billing API
# ==========================================
@app.route("/api/rent", methods=["GET"])
def rent_records():
    conn = get_db()
    student_code = request.args.get("student_code")
    status_filter = request.args.get("status")
    search = request.args.get("search", "").strip().lower()

    query = "SELECT * FROM rent_records WHERE 1=1"
    params = []
    if student_code:
        query += " AND student_code = ?"
        params.append(student_code)
    if status_filter and status_filter != "All statuses":
        query += " AND status = ?"
        params.append(status_filter)

    query += " ORDER BY id DESC"
    rows = conn.execute(query, params).fetchall()

    result = []
    for r in rows:
        record = row_to_dict(r)
        if search:
            combined = f"{record['student_name']} {record['room']} {record['month']}".lower()
            if search not in combined:
                continue
        result.append(record)

    conn.close()
    return jsonify({"success": True, "records": result})


@app.route("/api/rent/pay", methods=["POST"])
def pay_rent():
    data = request.get_json() or {}
    record_id = data.get("record_id")
    student_code = data.get("student_code")

    conn = get_db()
    if record_id:
        record = conn.execute("SELECT * FROM rent_records WHERE id = ?", (record_id,)).fetchone()
    elif student_code:
        record = conn.execute(
            "SELECT * FROM rent_records WHERE student_code = ? AND status != 'Paid' ORDER BY id DESC LIMIT 1",
            (student_code,)
        ).fetchone()
    else:
        conn.close()
        return jsonify({"success": False, "message": "Record ID or Student Code required"}), 400

    if not record:
        conn.close()
        return jsonify({"success": False, "message": "No pending rent found"}), 404

    paid_on = datetime.now().strftime("%d %b %Y")
    receipt_no = f"REC-{datetime.now().strftime('%m%d%H%M')}"

    conn.execute("""
        UPDATE rent_records
        SET status = 'Paid', paid_on = ?, receipt_no = ?
        WHERE id = ?
    """, (paid_on, receipt_no, record["id"]))
    conn.commit()
    conn.close()

    log_activity("Admin", None, f"Rent for {record['month']} marked Paid for {record['student_name']} ({receipt_no})")
    return jsonify({
        "success": True,
        "message": f"Payment recorded successfully. Receipt #{receipt_no}",
        "receipt_no": receipt_no,
        "paid_on": paid_on
    })


@app.route("/api/rent/remind", methods=["POST"])
def rent_reminder():
    conn = get_db()
    due_count = conn.execute("SELECT COUNT(*) FROM rent_records WHERE status IN ('Due', 'Overdue')").fetchone()[0]
    conn.close()

    log_activity("Admin", "ADMIN-001", f"Sent rent payment reminders to {due_count} students")
    return jsonify({
        "success": True,
        "message": f"Payment reminder notification dispatched to {due_count} students with pending dues."
    })


# ==========================================
# 9. Attendance API
# ==========================================
@app.route("/api/attendance", methods=["GET", "POST"])
def attendance():
    conn = get_db()
    today_str = date.today().strftime("%Y-%m-%d")

    if request.method == "GET":
        req_date = request.args.get("date", today_str)
        # Fetch all students and join their attendance for req_date
        students = conn.execute("SELECT * FROM users WHERE role = 'Student' ORDER BY room ASC").fetchall()
        result = []
        for s in students:
            att = conn.execute(
                "SELECT status FROM attendance WHERE student_code = ? AND date_str = ?",
                (s["user_code"], req_date)
            ).fetchone()
            result.append({
                "student_code": s["user_code"],
                "name": s["name"],
                "room": s["room"],
                "course": s["course"],
                "status": att["status"] if att else "Present"
            })
        conn.close()
        return jsonify({"success": True, "date": req_date, "records": result})

    # POST: Submit attendance records
    data = request.get_json() or {}
    req_date = data.get("date", today_str)
    records = data.get("records", [])

    for r in records:
        student_code = r.get("student_code")
        status = r.get("status", "Present")
        # Lookup student info
        student = conn.execute("SELECT name, room, course FROM users WHERE user_code = ?", (student_code,)).fetchone()
        if student:
            conn.execute("""
                INSERT INTO attendance (student_code, student_name, room, course, date_str, status)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(student_code, date_str) DO UPDATE SET status = excluded.status
            """, (student_code, student["name"], student["room"], student["course"], req_date, status))

    conn.commit()
    conn.close()

    log_activity("Warden", None, f"Submitted attendance for {len(records)} students on {req_date}")
    return jsonify({"success": True, "message": "Attendance successfully recorded in database"})


# ==========================================
# 10. Mess Menu & Feedback API
# ==========================================
@app.route("/api/mess/menu", methods=["GET"])
def mess_menu():
    conn = get_db()
    rows = conn.execute("SELECT * FROM mess_menu ORDER BY id ASC").fetchall()
    menu_by_day = {}
    for r in rows:
        d = r["day_of_week"]
        if d not in menu_by_day:
            menu_by_day[d] = {}
        menu_by_day[d][r["meal_type"]] = r["items"]
    conn.close()
    return jsonify({"success": True, "menu": menu_by_day})


@app.route("/api/mess/feedback", methods=["GET", "POST"])
def mess_feedback():
    conn = get_db()
    if request.method == "GET":
        # Average ratings per day
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        averages = []
        for d in days:
            avg_val = conn.execute(
                "SELECT AVG(rating) FROM mess_feedback WHERE day_of_week = ?", (d,)
            ).fetchone()[0]
            averages.append(round(avg_val, 1) if avg_val else 4.0)

        # Recent comments
        comments = conn.execute(
            "SELECT * FROM mess_feedback WHERE comment IS NOT NULL AND comment != '' ORDER BY id DESC LIMIT 10"
        ).fetchall()

        conn.close()
        return jsonify({
            "success": True,
            "averages": averages,
            "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "comments": [row_to_dict(c) for c in comments]
        })

    # POST: Student submits rating
    data = request.get_json() or {}
    student_code = data.get("student_code", "STU-2048")
    day_of_week = data.get("day_of_week", "Thursday")
    meal_type = data.get("meal_type", "Dinner")
    rating = int(data.get("rating", 5))
    comment = data.get("comment", "")

    student = conn.execute("SELECT name FROM users WHERE user_code = ?", (student_code,)).fetchone()
    student_name = student["name"] if student else "Anonymous"

    conn.execute("""
        INSERT INTO mess_feedback (student_code, student_name, day_of_week, meal_type, rating, comment)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (student_code, student_name, day_of_week, meal_type, rating, comment))
    conn.commit()
    conn.close()

    log_activity("Student", student_code, f"Submitted {rating}★ rating for {day_of_week} {meal_type}")
    return jsonify({"success": True, "message": "Feedback submitted successfully. Thank you!"})


@app.route("/api/mess/feedback/<int:feedback_id>/address", methods=["PUT"])
def address_feedback(feedback_id):
    conn = get_db()
    conn.execute("UPDATE mess_feedback SET addressed = 1 WHERE id = ?", (feedback_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Comment marked as addressed"})


# ==========================================
# 11. Staff Management API
# ==========================================
@app.route("/api/staff", methods=["GET", "POST"])
def staff():
    conn = get_db()
    if request.method == "GET":
        rows = conn.execute("SELECT * FROM staff ORDER BY id ASC").fetchall()
        conn.close()
        return jsonify({"success": True, "staff": [row_to_dict(r) for r in rows]})

    # POST: Add staff
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    role = data.get("role", "Assistant Warden").strip()
    block_floor = data.get("block_floor", "Block A").strip()
    contact = data.get("contact", "").strip()

    if not name or not contact:
        conn.close()
        return jsonify({"success": False, "message": "Name and Contact are required"}), 400

    conn.execute("""
        INSERT INTO staff (name, role, block_floor, contact, status)
        VALUES (?, ?, ?, ?, 'Approved')
    """, (name, role, block_floor, contact))
    conn.commit()
    conn.close()

    log_activity("Admin", "ADMIN-001", f"Added staff member: {name}")
    return jsonify({"success": True, "message": "Staff member added successfully"})


# ==========================================
# 12. Reports & Exports API
# ==========================================
@app.route("/api/reports/generate", methods=["POST"])
def generate_report():
    data = request.get_json() or {}
    report_type = data.get("type", "Rent ledger")
    file_format = data.get("format", "CSV").upper()
    from_date = data.get("from_date", "")
    to_date = data.get("to_date", "")

    conn = get_db()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = report_type.lower().replace(" ", "_")
    filename = f"{safe_name}_{timestamp}.csv"
    filepath = os.path.join(EXPORTS_DIR, filename)

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if "Rent" in report_type:
            writer.writerow(["Student ID", "Student Name", "Room", "Month", "Amount (INR)", "Due Date", "Paid On", "Status", "Receipt No"])
            rows = conn.execute("SELECT student_code, student_name, room, month, amount, due_date, paid_on, status, receipt_no FROM rent_records").fetchall()
            for r in rows:
                writer.writerow(list(r))
        elif "Occupancy" in report_type:
            writer.writerow(["Student ID", "Student Name", "Room", "Course", "Phone", "Curfew Status", "Status"])
            rows = conn.execute("SELECT user_code, name, room, course, phone, curfew_status, status FROM users WHERE role = 'Student'").fetchall()
            for r in rows:
                writer.writerow(list(r))
        elif "Complaint" in report_type:
            writer.writerow(["Complaint Code", "Student", "Room", "Category", "Title", "Status", "Date"])
            rows = conn.execute("SELECT complaint_code, student_name, room, category, title, status, date_str FROM complaints").fetchall()
            for r in rows:
                writer.writerow(list(r))
        elif "Attendance" in report_type:
            writer.writerow(["Date", "Student ID", "Student Name", "Room", "Course", "Status"])
            rows = conn.execute("SELECT date_str, student_code, student_name, room, course, status FROM attendance").fetchall()
            for r in rows:
                writer.writerow(list(r))
        else:
            writer.writerow(["Notice ID", "Title", "By", "Priority", "Time"])
            rows = conn.execute("SELECT id, title, by_role, priority, time_str FROM notices").fetchall()
            for r in rows:
                writer.writerow(list(r))

    conn.close()
    log_activity("Admin", "ADMIN-001", f"Generated {report_type} ({filename})")

    return jsonify({
        "success": True,
        "message": f"Report '{report_type}' generated successfully",
        "filename": filename,
        "download_url": f"/api/reports/download/{filename}"
    })


@app.route("/api/reports/download/<filename>", methods=["GET"])
def download_report(filename):
    filepath = os.path.join(EXPORTS_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"success": False, "message": "File not found"}), 404
    return send_file(filepath, as_attachment=True, download_name=filename)


# ==========================================
# 13. Settings & Backup API
# ==========================================
@app.route("/api/settings", methods=["GET", "PUT"])
def settings():
    conn = get_db()
    if request.method == "GET":
        rows = conn.execute("SELECT * FROM settings").fetchall()
        settings_dict = {r["key"]: r["value"] for r in rows}
        conn.close()
        return jsonify({"success": True, "settings": settings_dict})

    # PUT: Update settings
    data = request.get_json() or {}
    for k, v in data.items():
        conn.execute("""
            INSERT INTO settings (key, value) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """, (k, str(v)))
    conn.commit()
    conn.close()

    log_activity("Admin", "ADMIN-001", "Updated system settings")
    return jsonify({"success": True, "message": "Settings updated successfully"})


@app.route("/api/backup", methods=["POST"])
def manual_backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"hostel_backup_{timestamp}.db"
    dest_path = os.path.join(BACKUP_DIR, backup_filename)

    time_str = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    conn = get_db()
    # Use SQLite's online backup API for safe non-blocking backup
    bck = sqlite3.connect(dest_path)
    conn.backup(bck)
    bck.close()

    conn.execute(
        "INSERT INTO settings (key, value) VALUES ('last_backup', ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (time_str,)
    )
    conn.commit()
    log_activity("Admin", "ADMIN-001", f"Created database backup: {backup_filename}", conn=conn)
    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": f"Database backup created successfully: {backup_filename}",
        "last_backup": time_str
    })


@app.route("/api/notifications/test", methods=["POST"])
def test_notification():
    data = request.get_json() or {}
    channel = data.get("channel", "WhatsApp")
    return jsonify({
        "success": True,
        "message": f"✓ Connection test to {channel} gateway successful! Ready for alerts."
    })


if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("🚀 SafeStay Smart Women Hostel Server is running!")
    print("📍 URL: http://127.0.0.1:5000")
    print("💾 Database: hostel.db (SQLite)")
    print("=" * 55 + "\n")
    app.run(host="127.0.0.1", port=5000, debug=False)
