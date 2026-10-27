# SafeStay — Smart Women Hostel Management System

A full-stack, responsive hostel management platform built with a high-performance **Python (Flask)** REST backend, **SQLite** database, and an interactive **React** frontend.

---

## 🚀 Quick Start

### Option 1: Double-Click
Double-click `start.bat` on Windows. It will automatically check dependencies, ensure the SQLite database is initialized, start the backend on port `5000`, and open the website in your default browser.

### Option 2: Command Line
```powershell
# 1. Install dependencies
python -m pip install -r requirements.txt

# 2. Initialize database (pre-seeded with demo data)
python database.py

# 3. Start the server
python app.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser.

> **Note:** The frontend can also be accessed by opening `index.html` directly in your browser. It automatically detects the local backend and connects via CORS.

---

## 🔐 Separated Login Portals & Strict Role Isolation

The platform features **strictly isolated portals** with dedicated login experiences. Once a user signs in, they are locked into their specific portal with zero access or links to other roles:

### 🎓 1. Resident Student Portal
*Dedicated for hostel residents to manage amenities, curfew passes, and fees.*
- **Quick Profile Selector:** One-click quick selection between 9 unique resident profiles or manual ID entry.
- **Pre-seeded Student Profiles (Default Password: `password`):**
  - **Sanskruti Patil** (`STU-2048`) — Room A-204, B.Tech CS (Active Exit Pass: EX-2048, Complaint: CMP-1042)
  - **Aarushi Patel** (`STU-1001`) — Room A-101, BCA (Solved Complaint: CMP-1029)
  - **Diya Shah** (`STU-1002`) — Room A-102, B.Com (Pending Exit Pass: EX-2051)
  - **Isha Nair** (`STU-1003`) — Room A-103, B.Sc (Currently Out / Overdue Curfew Alert)
  - **Kavya Singh** (`STU-1004`) — Room A-104, B.Tech (Overdue Rent Due: ₹8,500)
  - **Meera Joshi** (`STU-2001`) — Room A-201, BBA (Active Exit Pass: EX-2054)
  - **Nandini Rao** (`STU-2002`) — Room A-202, BCA (Currently Out)
  - **Priya Verma** (`STU-2003`) — Room A-203, B.Tech (Pending Leave: EX-2052)
  - **Riya Das** (`STU-2004`) — Room A-204, B.Sc (Internet Complaint: CMP-1038)
- **Features:** Personalized Dashboard with Safe Return Ring, Emergency Contacts Profile editing, Fee Payment with downloadable receipts (`REC-XXXX`), Grievance / Complaint submission with live tracking, Digital Gate QR Boarding Pass, Weekly Mess Menu with 5-star rating feedback, and Notice Board acknowledgment.

### 🛡️ 2. Floor Warden Portal
*Dedicated for hostel floor wardens. Wardens cannot access Admin or Student private screens.*
- **Credentials:** `WARD-001` / `password` (Meera Sharma, Block A Warden)
- **Features:**
  - **Dashboard:** Curfew countdowns for all residents currently out, with 1-click **"Check In"** gate return simulator.
  - **Roll-Call Attendance:** Daily attendance register with floor filters, Present/Absent toggles, "All Present" shortcut, and database lock.
  - **Gate Clearance & Scanner:** Approve or reject student exit requests; scan or enter resident QR pass codes to log gate movements.
  - **Grievance Resolution:** Filter, inspect, and advance student complaints from Pending to In Progress and Solved.
  - **Resident Directory:** Searchable directory showing room numbers, contact numbers, fee status, and real-time In/Out gate status.
  - **Notice Broadcast:** Compose and publish announcements with priority tags.
  - **Mess Analytics:** Daily rating trend bar charts and resident feedback comment review.

### ⚙️ 3. Operations Administration Portal
*Restricted administrative zone for hostel directors and operators.*
- **Credentials:** `ADMIN-001` / `password` (Hostel Administration)
- **Features:**
  - **Live Overview:** Bed occupancy metrics (184/200 beds, 92%), revenue collections, rent aging charts, and complaint distribution charts.
  - **Resident Enrollment:** Add new students with automatic room allocation and rent ledger creation; toggle active/inactive status.
  - **Financial Ledgers:** View fee statuses, mark offline payments as paid, broadcast bulk payment reminders, and export CSV ledgers.
  - **Staff Management:** View warden assignments and add new staff members.
  - **CSV Report Generator:** Generate real CSV downloads for Rent Ledgers, Occupancy Rosters, Complaint Logs, and Attendance Registers.
  - **Configuration & Backup:** Update curfew hours, hostel capacity, and trigger 1-click SQLite database backups to the `backups/` directory.

---

## 🗄️ Database Architecture (`hostel.db`)

Built on SQLite with **Write-Ahead Logging (WAL)** and high-concurrency connection pools:
- `users` — Resident student credentials, warden accounts, admin credentials, rooms, and curfew statuses.
- `notices` — Broadcast announcements with priority tags, author roles, and acknowledgment arrays.
- `complaints` — Resident maintenance and mess grievances with status workflows.
- `exit_requests` — Gate passes with departure/return timestamps and approval statuses.
- `rent_records` — Monthly hostel fee billing records with receipt IDs.
- `mess_menu` & `mess_feedback` — 7-day meal plans and resident star ratings.
- `attendance` — Daily attendance roll-call records.
- `staff` — Warden directory and floor assignments.
- `settings` — System parameters (curfew cutoff, capacity, backup logs).
- `activity_logs` — Administrative and security event audit logs.

---

## 📁 Project Structure

```text
smart-women-hostel/
├── app.py              # Flask REST API backend & static server
├── database.py         # SQLite schema initialization and seed dataset
├── hostel.db           # SQLite database file (WAL mode enabled)
├── index.html          # High-performance React 18 frontend with portal isolation
├── requirements.txt    # Python package dependencies
├── start.bat           # Windows 1-click startup script
├── start.ps1           # PowerShell startup script
└── README.md           # Documentation & user guide
```
