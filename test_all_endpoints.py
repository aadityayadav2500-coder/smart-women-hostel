import urllib.request
import urllib.parse
import json

BASE = "http://127.0.0.1:5000"

def request_api(path, method="GET", data=None):
    quoted_path = urllib.parse.quote(path, safe='/?&=')
    url = f"{BASE}{quoted_path}"
    body = json.dumps(data).encode("utf-8") if data else None
    headers = {"Content-Type": "application/json"} if data else {}
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=5) as res:
            raw = res.read().decode()
            try:
                data = json.loads(raw)
            except Exception:
                data = {"html_length": len(raw)}
            return res.status, data
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except Exception:
            return e.code, {"error": str(e)}
    except Exception as e:
        return 0, {"error": str(e)}

print("=== TESTING BACKEND ENDPOINTS ===")

tests = [
    ("/", "GET", None),
    ("/api/health", "GET", None),
    ("/api/public/students", "GET", None),
    ("/api/login", "POST", {"role": "Student", "user_code": "STU-2048", "password": "password"}),
    ("/api/login", "POST", {"role": "Warden", "user_code": "WARD-001", "password": "password"}),
    ("/api/login", "POST", {"role": "Admin", "user_code": "ADMIN-001", "password": "password"}),
    ("/api/profile?user_code=STU-2048", "GET", None),
    ("/api/profile", "PUT", {"user_code": "STU-2048", "phone": "+91 98765 43021"}),
    ("/api/stats/student?user_code=STU-2048", "GET", None),
    ("/api/stats/warden", "GET", None),
    ("/api/stats/admin", "GET", None),
    ("/api/students", "GET", None),
    ("/api/students?search=diya&floor=Floor 1", "GET", None),
    ("/api/notices", "GET", None),
    ("/api/complaints", "GET", None),
    ("/api/complaints?student_code=STU-2048", "GET", None),
    ("/api/exit-requests", "GET", None),
    ("/api/exit-requests?student_code=STU-2048", "GET", None),
    ("/api/rent", "GET", None),
    ("/api/rent?student_code=STU-2048", "GET", None),
    ("/api/attendance", "GET", None),
    ("/api/mess/menu", "GET", None),
    ("/api/mess/feedback", "GET", None),
    ("/api/staff", "GET", None),
    ("/api/settings", "GET", None),
    ("/api/settings", "PUT", {"curfew_time": "23:30"}),
    ("/api/notifications/test", "POST", {"channel": "WhatsApp"}),
    ("/api/reports/generate", "POST", {"type": "Rent ledger", "format": "CSV"}),
    ("/api/reports/generate", "POST", {"type": "Occupancy", "format": "CSV"}),
    ("/api/reports/generate", "POST", {"type": "Complaint log", "format": "CSV"}),
    ("/api/reports/generate", "POST", {"type": "Attendance", "format": "CSV"}),
    ("/api/reports/generate", "POST", {"type": "Notice feed", "format": "CSV"}),
    ("/api/gate/scan", "POST", {"code": "STU-2048"}),
    ("/api/gate/scan", "POST", {"code": "STU-2048"}), # scan back
    ("/api/backup", "POST", {})
]

for path, method, payload in tests:
    status, body = request_api(path, method, payload)
    succ = body.get("success", True) if isinstance(body, dict) else True
    res_str = f"status={status}, ok={succ}"
    if status >= 400 and path != "/api/health":
        print(f"❌ FAIL: {method:5} {path:40} -> {res_str} - {body}")
    elif path == "/api/health" and status == 404:
        print(f"⚠️  MISSING: {method:5} {path:40} -> 404 Not Found")
    else:
        print(f"✓ PASS: {method:5} {path:40} -> {res_str}")
