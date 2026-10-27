"""
Database initialization, schema creation, and realistic seed data for SafeStay Smart Women Hostel.
"""

import sqlite3
import os
import json
from datetime import datetime, date

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hostel.db")

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=20.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_code TEXT UNIQUE NOT NULL,
        role TEXT NOT NULL,
        name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        room TEXT,
        course TEXT,
        warden_name TEXT,
        emergency_name TEXT,
        emergency_phone TEXT,
        status TEXT DEFAULT 'Active',
        curfew_status TEXT DEFAULT 'In',
        password TEXT NOT NULL DEFAULT 'password',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Notices table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        body TEXT NOT NULL,
        by_role TEXT NOT NULL DEFAULT 'Warden',
        priority INTEGER DEFAULT 0,
        time_str TEXT,
        expiry_date TEXT,
        acknowledged_by TEXT DEFAULT '[]',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Complaints table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        complaint_code TEXT UNIQUE NOT NULL,
        student_code TEXT,
        student_name TEXT NOT NULL,
        room TEXT NOT NULL,
        category TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'Pending',
        date_str TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Exit requests table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exit_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        request_code TEXT UNIQUE NOT NULL,
        student_code TEXT NOT NULL,
        student_name TEXT NOT NULL,
        room TEXT NOT NULL,
        date_str TEXT NOT NULL,
        time_out TEXT NOT NULL,
        expected_return TEXT NOT NULL,
        actual_exit TEXT,
        actual_entry TEXT,
        reason TEXT NOT NULL,
        status TEXT DEFAULT 'Pending',
        reject_reason TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Rent records table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rent_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_code TEXT NOT NULL,
        student_name TEXT NOT NULL,
        room TEXT NOT NULL,
        month TEXT NOT NULL,
        amount INTEGER NOT NULL DEFAULT 8500,
        due_date TEXT NOT NULL,
        paid_on TEXT,
        status TEXT NOT NULL DEFAULT 'Due',
        receipt_no TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Mess menu table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mess_menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day_of_week TEXT NOT NULL,
        meal_type TEXT NOT NULL,
        items TEXT NOT NULL
    )
    """)

    # Mess feedback table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mess_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_code TEXT,
        student_name TEXT,
        day_of_week TEXT NOT NULL,
        meal_type TEXT NOT NULL,
        rating INTEGER NOT NULL,
        comment TEXT,
        addressed INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Attendance table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_code TEXT NOT NULL,
        student_name TEXT NOT NULL,
        room TEXT NOT NULL,
        course TEXT NOT NULL,
        date_str TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Present',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(student_code, date_str)
    )
    """)

    # Staff table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        block_floor TEXT NOT NULL,
        contact TEXT NOT NULL,
        status TEXT DEFAULT 'Approved',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Settings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    )
    """)

    # Activity logs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activity_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_role TEXT NOT NULL,
        user_code TEXT,
        action TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    # Seed initial data if users table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        seed_data(cursor)
        conn.commit()

    conn.close()

def seed_data(cursor):
    # 1. Seed Users
    users_data = [
        # Student (Sanskruti)
        ("STU-2048", "Student", "Sanskruti Patil", "sanskruti@example.com", "+91 98765 43021", "A-204", "B.Tech Computer Science", "Meera Sharma", "Rajesh Patil", "+91 98765 11111", "Active", "Out", "password"),
        # Other students
        ("STU-1001", "Student", "Aarushi Patel", "aarushi@example.com", "98765 12001", "A-101", "BCA", "Meera Sharma", "Suresh Patel", "+91 98765 11001", "Active", "In", "password"),
        ("STU-1002", "Student", "Diya Shah", "diya@example.com", "98765 12002", "A-102", "B.Com", "Meera Sharma", "Kishore Shah", "+91 98765 11002", "Active", "In", "password"),
        ("STU-1003", "Student", "Isha Nair", "isha@example.com", "98765 12003", "A-103", "B.Sc", "Meera Sharma", "Gopal Nair", "+91 98765 11003", "Active", "Out", "password"),
        ("STU-1004", "Student", "Kavya Singh", "kavya@example.com", "98765 12004", "A-104", "B.Tech", "Meera Sharma", "Anil Singh", "+91 98765 11004", "Active", "In", "password"),
        ("STU-2001", "Student", "Meera Joshi", "meera.j@example.com", "98765 12005", "A-201", "BBA", "Meera Sharma", "Vinod Joshi", "+91 98765 11005", "Active", "In", "password"),
        ("STU-2002", "Student", "Nandini Rao", "nandini@example.com", "98765 12006", "A-202", "BCA", "Meera Sharma", "Mohan Rao", "+91 98765 11006", "Active", "Out", "password"),
        ("STU-2003", "Student", "Priya Verma", "priya@example.com", "98765 12007", "A-203", "B.Tech", "Meera Sharma", "Ramesh Verma", "+91 98765 11007", "Active", "In", "password"),
        ("STU-2004", "Student", "Riya Das", "riya@example.com", "98765 12008", "A-204", "B.Sc", "Meera Sharma", "Debasish Das", "+91 98765 11008", "Active", "In", "password"),
        
        # Warden
        ("WARD-001", "Warden", "Meera Sharma", "meera.warden@example.com", "+91 98765 30001", "Warden Office, Block A", "Block A • Warden", "", "Office Desk", "+91 98765 30000", "Active", "In", "password"),
        
        # Admin
        ("ADMIN-001", "Admin", "Hostel Admin", "admin@safestayhostel.com", "+91 98765 00001", "Admin Office", "Operations Head", "", "Emergency Desk", "+91 98765 00000", "Active", "In", "password")
    ]

    cursor.executemany("""
    INSERT INTO users (user_code, role, name, email, phone, room, course, warden_name, emergency_name, emergency_phone, status, curfew_status, password)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, users_data)

    # 2. Seed Notices
    notices_data = [
        ("Water tank maintenance tonight", "Water supply in Block A may be interrupted from 10:30 PM to 12:00 AM.", "Warden", 1, "Today, 6:20 PM", "2026-09-01"),
        ("Mess feedback week is open", "Please rate meals you have already received this week to help us improve menu quality.", "Admin", 0, "Today, 10:00 AM", "2026-09-05"),
        ("Library timings extended", "Study room remains open until 11:30 PM on weekdays during exam preparations.", "Warden", 0, "Yesterday", "2026-09-15"),
        ("Fire drill on Saturday morning", "Mandatory fire safety mock drill for all residents at 9:00 AM in the central courtyard.", "Admin", 1, "2 days ago", "2026-09-03")
    ]
    cursor.executemany("""
    INSERT INTO notices (title, body, by_role, priority, time_str, expiry_date)
    VALUES (?, ?, ?, ?, ?, ?)
    """, notices_data)

    # 3. Seed Complaints
    complaints_data = [
        ("CMP-1042", "STU-2048", "Sanskruti Patil", "A-204", "Maintenance", "Bathroom tap leakage", "The cold water tap in bathroom A-204 is continuously dripping.", "In Progress", "27 Aug"),
        ("CMP-1038", "STU-2004", "Riya Das", "A-204", "Internet", "Wi-Fi not working in room", "Wi-Fi signal drops frequently on 2nd floor wing A.", "Pending", "25 Aug"),
        ("CMP-1029", "STU-1001", "Aarushi Patel", "A-101", "Mess", "Mess food too salty", "Dinner dal was excessively salty on Thursday evening.", "Solved", "21 Aug"),
        ("CMP-1025", "STU-1004", "Kavya Singh", "A-104", "Safety", "Corridor bulb flickering", "Corridor light outside room 104 needs replacement.", "Solved", "18 Aug"),
        ("CMP-1045", "STU-1002", "Diya Shah", "A-102", "Maintenance", "Study table light not turning on", "Desk light bulb needs replacement in Room A-102.", "Solved", "22 Aug"),
        ("CMP-1046", "STU-2001", "Meera Joshi", "A-201", "Maintenance", "Study room ceiling fan vibrating", "Speed regulator in study room 2nd floor is loose.", "In Progress", "26 Aug"),
        ("CMP-1047", "STU-2003", "Priya Verma", "A-203", "Maintenance", "Water purifier filter beeping", "1st floor wing A water cooler needs filter service.", "Pending", "27 Aug")
    ]
    cursor.executemany("""
    INSERT INTO complaints (complaint_code, student_code, student_name, room, category, title, description, status, date_str)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, complaints_data)

    # 4. Seed Exit Requests
    exit_requests_data = [
        ("EX-2048", "STU-2048", "Sanskruti Patil", "A-204", "27 Aug", "8:10 PM", "11:30 PM", "8:10 PM", None, "Personal", "Approved", None),
        ("EX-2050", "STU-2004", "Riya Das", "A-204", "27 Aug", "8:00 PM", "11:30 PM", None, None, "Personal", "Pending", None),
        ("EX-2051", "STU-1002", "Diya Shah", "A-102", "28 Aug", "5:30 PM", "9:30 PM", None, None, "College work", "Pending", None),
        ("EX-2052", "STU-2003", "Priya Verma", "A-203", "29 Aug", "6:00 PM", "10:30 PM", None, None, "Family event", "Pending", None),
        ("EX-2031", "STU-2048", "Sanskruti Patil", "A-204", "24 Aug", "7:40 PM", "10:15 PM", "7:40 PM", "10:15 PM", "Study group", "Completed", None),
        ("EX-2022", "STU-1003", "Isha Nair", "A-103", "27 Aug", "7:00 PM", "10:30 PM", "7:02 PM", None, "Project discussion", "Approved", None),
        ("EX-2053", "STU-1004", "Kavya Singh", "A-104", "25 Aug", "6:30 PM", "9:45 PM", "6:30 PM", "9:45 PM", "Library research", "Completed", None),
        ("EX-2054", "STU-2001", "Meera Joshi", "A-201", "27 Aug", "8:15 PM", "11:00 PM", "8:15 PM", None, "Group assignment", "Approved", None),
        ("EX-2055", "STU-1001", "Aarushi Patel", "A-101", "26 Aug", "5:00 PM", "8:30 PM", "5:02 PM", "8:25 PM", "College fest preparation", "Completed", None)
    ]
    cursor.executemany("""
    INSERT INTO exit_requests (request_code, student_code, student_name, room, date_str, time_out, expected_return, actual_exit, actual_entry, reason, status, reject_reason)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, exit_requests_data)

    # 5. Seed Rent Records
    rent_data = [
        # Sanskruti
        ("STU-2048", "Sanskruti Patil", "A-204", "August 2026", 8500, "05 Sep 2026", None, "Due", None),
        ("STU-2048", "Sanskruti Patil", "A-204", "July 2026", 8500, "05 Aug 2026", "02 Jul 2026", "Paid", "REC-7801"),
        ("STU-2048", "Sanskruti Patil", "A-204", "June 2026", 8500, "05 Jul 2026", "03 Jun 2026", "Paid", "REC-6701"),
        ("STU-2048", "Sanskruti Patil", "A-204", "May 2026", 8500, "05 Jun 2026", "02 May 2026", "Paid", "REC-5601"),
        
        # Aarushi
        ("STU-1001", "Aarushi Patel", "A-101", "August 2026", 8500, "05 Sep 2026", "20 Aug 2026", "Paid", "REC-8101"),
        ("STU-1001", "Aarushi Patel", "A-101", "July 2026", 8500, "05 Aug 2026", "03 Jul 2026", "Paid", "REC-7101"),
        ("STU-1001", "Aarushi Patel", "A-101", "June 2026", 8500, "05 Jul 2026", "01 Jun 2026", "Paid", "REC-6101"),
        
        # Diya
        ("STU-1002", "Diya Shah", "A-102", "August 2026", 8500, "05 Sep 2026", None, "Due", None),
        ("STU-1002", "Diya Shah", "A-102", "July 2026", 8500, "05 Aug 2026", "04 Jul 2026", "Paid", "REC-7102"),
        ("STU-1002", "Diya Shah", "A-102", "June 2026", 8500, "05 Jul 2026", "02 Jun 2026", "Paid", "REC-6102"),
        
        # Isha
        ("STU-1003", "Isha Nair", "A-103", "August 2026", 8500, "05 Sep 2026", "22 Aug 2026", "Paid", "REC-8103"),
        ("STU-1003", "Isha Nair", "A-103", "July 2026", 8500, "05 Aug 2026", "02 Jul 2026", "Paid", "REC-7103"),
        
        # Kavya
        ("STU-1004", "Kavya Singh", "A-104", "August 2026", 8500, "01 Aug 2026", None, "Overdue", None),
        ("STU-1004", "Kavya Singh", "A-104", "July 2026", 8500, "05 Aug 2026", "10 Jul 2026", "Paid", "REC-7104"),
        
        # Meera Joshi
        ("STU-2001", "Meera Joshi", "A-201", "August 2026", 8500, "05 Sep 2026", "25 Aug 2026", "Paid", "REC-8201"),
        ("STU-2001", "Meera Joshi", "A-201", "July 2026", 8500, "05 Aug 2026", "02 Jul 2026", "Paid", "REC-7201"),
        
        # Nandini
        ("STU-2002", "Nandini Rao", "A-202", "August 2026", 8500, "05 Sep 2026", None, "Due", None),
        ("STU-2002", "Nandini Rao", "A-202", "July 2026", 8500, "05 Aug 2026", "05 Jul 2026", "Paid", "REC-7202"),
        
        # Priya
        ("STU-2003", "Priya Verma", "A-203", "August 2026", 8500, "05 Sep 2026", "18 Aug 2026", "Paid", "REC-8203"),
        ("STU-2003", "Priya Verma", "A-203", "July 2026", 8500, "05 Aug 2026", "03 Jul 2026", "Paid", "REC-7203"),
        
        # Riya
        ("STU-2004", "Riya Das", "A-204", "August 2026", 8500, "05 Sep 2026", "15 Aug 2026", "Paid", "REC-8204"),
        ("STU-2004", "Riya Das", "A-204", "July 2026", 8500, "05 Aug 2026", "04 Jul 2026", "Paid", "REC-7204")
    ]
    cursor.executemany("""
    INSERT INTO rent_records (student_code, student_name, room, month, amount, due_date, paid_on, status, receipt_no)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, rent_data)

    # 6. Seed Mess Menu
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    menus = {
        "Monday": [
            ("Breakfast", "Idli Sambhar, Chutney, Tea / Coffee"),
            ("Lunch", "Rajma, Steamed Rice, Roti, Boondi Raita"),
            ("Snacks", "Samosa, Mint Chutney, Green Tea"),
            ("Dinner", "Aloo Gobi, Dal Tadka, Phulka, Kheer")
        ],
        "Tuesday": [
            ("Breakfast", "Methi Thepla, Curd, Pickle, Tea"),
            ("Lunch", "Chole, Bhature / Rice, Onion Salad"),
            ("Snacks", "Veg Cutlet, Tomato Sauce, Tea"),
            ("Dinner", "Mix Veg Korma, Jeera Rice, Chapati, Gulab Jamun")
        ],
        "Wednesday": [
            ("Breakfast", "Upma, Coconut Chutney, Banana, Tea"),
            ("Lunch", "Kadhi Pakora, Khichdi / Rice, Papad"),
            ("Snacks", "Biscuits, Fruit Salad, Masala Chai"),
            ("Dinner", "Egg Curry / Paneer Bhurji, Roti, Rice, Dal")
        ],
        "Thursday": [
            ("Breakfast", "Poha, Boiled Eggs / Sprouts, Tea"),
            ("Lunch", "Dal Makhani, Rice, Roti, Cucumber Salad"),
            ("Snacks", "Tea, Rusks, Seasonal Fruit"),
            ("Dinner", "Paneer Butter Masala, Jeera Rice, Roti, Custard")
        ],
        "Friday": [
            ("Breakfast", "Aloo Paratha, Curd, Butter, Tea"),
            ("Lunch", "Veg Biryani, Mirchi Ka Salan, Raita"),
            ("Snacks", "Dhokla, Chutney, Lemonade / Tea"),
            ("Dinner", "Palak Paneer, Tawa Roti, Rice, Moong Dal Halwa")
        ],
        "Saturday": [
            ("Breakfast", "Masala Dosa, Sambhar, Filter Coffee"),
            ("Lunch", "Chana Dal, Baingan Bharta, Chapati, Rice"),
            ("Snacks", "Bhel Puri, Masala Chai"),
            ("Dinner", "Special Thali: Shahi Paneer, Naan, Pulao, Ice Cream")
        ],
        "Sunday": [
            ("Breakfast", "Puri Bhaji, Halwa, Masala Chai"),
            ("Lunch", "Continental Pasta, Garlic Bread, Fresh Juice"),
            ("Snacks", "Pakoras, Ginger Tea"),
            ("Dinner", "Dal Fry, Jeera Aloo, Steamed Rice, Phulka, Sweet")
        ]
    }
    for day, meals in menus.items():
        for meal_type, items in meals:
            cursor.execute("""
            INSERT INTO mess_menu (day_of_week, meal_type, items)
            VALUES (?, ?, ?)
            """, (day, meal_type, items))

    # 7. Seed Mess Feedback
    feedback_data = [
        ("STU-2048", "Sanskruti Patil", "Thursday", "Breakfast", 4, "Good poha, fresh tea.", 0),
        ("STU-1002", "Diya Shah", "Thursday", "Lunch", 4, "Loved the dal makhani.", 0),
        ("STU-1004", "Kavya Singh", "Wednesday", "Dinner", 2, "Dinner: paneer was too oily", 0),
        ("STU-1003", "Isha Nair", "Tuesday", "Lunch", 3, "Lunch: rice was cold", 0),
        ("STU-2002", "Nandini Rao", "Monday", "Breakfast", 2, "Breakfast: tea was too sweet", 0)
    ]
    cursor.executemany("""
    INSERT INTO mess_feedback (student_code, student_name, day_of_week, meal_type, rating, comment, addressed)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, feedback_data)

    # 8. Seed Attendance (Today)
    today_str = date.today().strftime("%Y-%m-%d")
    attendance_data = [
        ("STU-1001", "Aarushi Patel", "A-101", "BCA", today_str, "Present"),
        ("STU-1002", "Diya Shah", "A-102", "B.Com", today_str, "Present"),
        ("STU-1003", "Isha Nair", "A-103", "B.Sc", today_str, "Present"),
        ("STU-1004", "Kavya Singh", "A-104", "B.Tech", today_str, "Present"),
        ("STU-2001", "Meera Joshi", "A-201", "BBA", today_str, "Present"),
        ("STU-2002", "Nandini Rao", "A-202", "BCA", today_str, "Present"),
        ("STU-2003", "Priya Verma", "A-203", "B.Tech", today_str, "Present"),
        ("STU-2048", "Sanskruti Patil", "A-204", "B.Tech CS", today_str, "Present"),
        ("STU-2004", "Riya Das", "A-204", "B.Sc", today_str, "Present")
    ]
    cursor.executemany("""
    INSERT OR REPLACE INTO attendance (student_code, student_name, room, course, date_str, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """, attendance_data)

    # 9. Seed Staff
    staff_data = [
        ("Meera Sharma", "Head Warden", "Block A • Floors 1–2", "+91 98765 30001", "Approved"),
        ("Anita Kulkarni", "Assistant Warden", "Block B • Floors 1–2", "+91 98765 30002", "Approved"),
        ("Pooja Menon", "Night Warden", "Block C • Floors 1–3", "+91 98765 30003", "Approved")
    ]
    cursor.executemany("""
    INSERT INTO staff (name, role, block_floor, contact, status)
    VALUES (?, ?, ?, ?, ?)
    """, staff_data)

    # 10. Seed Settings
    settings_data = [
        ("hostel_name", "Sakhi Women's Hostel"),
        ("capacity", "200"),
        ("occupied", "184"),
        ("curfew_time", "23:30"),
        ("email_notifications", "Enabled"),
        ("whatsapp_notifications", "Configured"),
        ("last_backup", datetime.now().strftime("%Y-%m-%d %I:%M %p"))
    ]
    cursor.executemany("""
    INSERT OR REPLACE INTO settings (key, value)
    VALUES (?, ?)
    """, settings_data)

    # 11. Seed Activity Logs
    activity_data = [
        ("Student", "STU-2048", "Exit request for Friday approved"),
        ("Student", "STU-2048", "Rent for August marked Paid"),
        ("Student", "STU-2048", "Complaint CMP-1042 moved to In Progress"),
        ("Warden", "WARD-001", "QR exit logged — Isha Nair"),
        ("Warden", "WARD-001", "Complaint CMP-1042 acknowledged"),
        ("Warden", "WARD-001", "Attendance submitted for Floor 1"),
        ("Warden", "WARD-001", "Notice published: Water tank maintenance tonight")
    ]
    cursor.executemany("""
    INSERT INTO activity_logs (user_role, user_code, action)
    VALUES (?, ?, ?)
    """, activity_data)

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DB_PATH)
