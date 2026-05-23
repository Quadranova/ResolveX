import os
import io
import base64
import qrcode
from flask import Flask, render_template_string, request, redirect, url_for, flash
from google import genai
from google.genai import types

app = Flask(__name__)
app.secret_key = "super_secret_key_for_prototype"

# --- GOOGLE AI STUDIO SETUP ---
# Best Practice: Retrieves your API key safely from environment variables.
# You can set it in your terminal before running: export GEMINI_API_KEY="your_actual_key"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_FALLBACK_API_KEY_HERE")
ai_client = genai.Client(api_key=GEMINI_API_KEY)

# Simulated Users Database
USERS_DB = {
    "citizen1": {"password": "password123", "role": "citizen"},
    "admin1": {"password": "admin123", "role": "admin"},
    "super1": {"password": "super123", "role": "supervisor"}
}

# Expanded Shared Database with initial sample metrics across categories
issues_db = [
    {"id": 1, "category": "Potholes & Road Damage", "description": "Large pothole in the middle of the road.", "severity": "High", "status": "Under Progress"},
    {"id": 2, "category": "Garbage Accumulation", "description": "Overflowing public bin.", "severity": "Medium", "status": "Resolved"},
    {"id": 3, "category": "Water Leakage", "description": "Main water pipeline crack.", "severity": "Critical", "status": "Not Yet Started"},
    {"id": 4, "category": "Broken Streetlights", "description": "Entire lane dark.", "severity": "Low", "status": "Resolved"},
    {"id": 5, "category": "Drainage Issues", "description": "Overflowing sewage onto the pavement.", "severity": "High", "status": "Not Yet Started"},
    {"id": 6, "category": "Traffic Signal Failures", "description": "Main intersection signals are completely blank.", "severity": "Critical", "status": "Under Progress"},
    {"id": 7, "category": "Electrical Hazards", "description": "Exposed hanging high-voltage wire.", "severity": "Critical", "status": "Under Progress"},
    {"id": 8, "category": "Public Safety Risks", "description": "Unstable construction scaffolding over walkway.", "severity": "High", "status": "Not Yet Started"},
    {"id": 9, "category": "Stray Dogs Issue", "description": "Pack of aggressive stray dogs near park.", "severity": "Medium", "status": "Resolved"}
]

# Helper function to inject Base64 QR Code string directly into templates
def generate_qr_base64(issue_id):
    tracking_url = request.url_root + f"track/{issue_id}"
    
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(tracking_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    
    return "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode()

# Upgraded Civic Trust Score Engine explicitly tracking all four requested parameters
def calculate_trust_scores():
    dept_map = {
        "Potholes & Road Damage": "Public Works (Roads)",
        "Water Leakage": "Water Supply & Sewage",
        "Drainage Issues": "Water Supply & Sewage",
        "Garbage Accumulation": "Waste Management",
        "Broken Streetlights": "Electrical & Energy",
        "Electrical Hazards": "Electrical & Energy",
        "Traffic Signal Failures": "Traffic Control",
        "Public Safety Risks": "Public Safety & Welfare",
        "Stray Dogs Issue": "Public Safety & Welfare"
    }
    
    departments = {
        "Public Works (Roads)": {"total": 0, "resolved": 0, "under_progress": 0, "not_started": 0, "critical_backlog": 0},
        "Water Supply & Sewage": {"total": 0, "resolved": 0, "under_progress": 0, "not_started": 0, "critical_backlog": 0},
        "Waste Management": {"total": 0, "resolved": 0, "under_progress": 0, "not_started": 0, "critical_backlog": 0},
        "Electrical & Energy": {"total": 0, "resolved": 0, "under_progress": 0, "not_started": 0, "critical_backlog": 0},
        "Traffic Control": {"total": 0, "resolved": 0, "under_progress": 0, "not_started": 0, "critical_backlog": 0},
        "Public Safety & Welfare": {"total": 0, "resolved": 0, "under_progress": 0, "not_started": 0, "critical_backlog": 0}
    }
    
    for issue in issues_db:
        cat = issue.get("category", "Potholes & Road Damage")
        dept_name = "Public Works (Roads)"
        for standard_cat, dept in dept_map.items():
            if standard_cat.lower() in cat.lower() or cat.lower() in standard_cat.lower():
                dept_name = dept
                break
        
        departments[dept_name]["total"] += 1
        if issue["status"] == "Resolved":
            departments[dept_name]["resolved"] += 1
        elif issue["status"] == "Under Progress":
            departments[dept_name]["under_progress"] += 1
        else:
            departments[dept_name]["not_started"] += 1
            
        if issue["status"] != "Resolved" and ("Critical" in issue["severity"] or "High" in issue["severity"]):
            departments[dept_name]["critical_backlog"] += 1

    final_scores = {}
    for name, stats in departments.items():
        if stats["total"] == 0:
            final_scores[name] = {
                "overall": 85, "resolution_rate": 100, "response_speed": 90, "sla_adherence": 100, "citizen_sat": 95
            }
            continue
            
        res_rate = int((stats["resolved"] / stats["total"]) * 100)
        total_open = stats["under_progress"] + stats["not_started"]
        speed_rate = 100 if total_open == 0 else int((stats["under_progress"] / total_open) * 100)
        sla_calc = max(10, 100 - (stats["critical_backlog"] * 25))
        citizen_calc = max(15, int((res_rate * 0.6) + (speed_rate * 0.4)))
        overall_score = int((res_rate * 0.35) + (speed_rate * 0.20) + (sla_calc * 0.25) + (citizen_calc * 0.20))
        
        final_scores[name] = {
            "overall": max(10, min(100, overall_score)),
            "resolution_rate": res_rate,
            "response_speed": speed_rate,
            "sla_adherence": sla_calc,
            "citizen_sat": citizen_calc
        }
        
    return final_scores

# --- HTML STYLES & LAYOUTS ---
BASE_CSS = """
<style>
    body { font-family: 'Segoe UI', system-ui, sans-serif; background: #f8fafc; color: #1e293b; margin: 0; padding: 20px; }
    .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    h1, h2, h3 { color: #0f172a; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin-bottom: 30px; }
    @media (max-width: 900px) { .grid { grid-template-columns: 1fr; } }
    input, select, textarea { width: 100%; padding: 10px; margin: 8px 0 20px 0; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box; }
    button { background: #2563eb; color: white; border: none; padding: 12px 20px; border-radius: 6px; cursor: pointer; font-weight: 600; }
    button:hover { background: #1d4ed8; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 14px; }
    th, td { text-align: left; padding: 12px; border-bottom: 1px solid #e2e8f0; }
    th { background: #f1f5f9; color: #475569; }
    .badge { display: inline-block; padding: 4px 8px; border-radius: 12px; font-weight: bold; font-size: 12px; }
    .status-Resolved { background: #dcfce7; color: #16a34a; }
    .status-Under-Progress { background: #fef9c3; color: #ca8a04; }
    .status-Not-Yet-Started { background: #fee2e2; color: #dc2626; }
    
    /* Detailed Trust Component Styles */
    .trust-card { background: #f8fafc; padding: 18px; border-radius: 8px; border-left: 5px solid #2563eb; margin-bottom: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.02); }
    .trust-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
    .trust-title { font-weight: bold; color: #1e293b; font-size: 15px; }
    .trust-score-badge { background: #2563eb; color: white; padding: 2px 8px; border-radius: 4px; font-size: 13px; font-weight: bold; }
    .metrics-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 12px; color: #64748b; border-top: 1px solid #e2e8f0; padding-top: 8px; }
    .metric-item { display: flex; justify-content: space-between; }
    .metric-val { font-weight: 600; color: #334155; }
    
    .qr-img { width: 70px; height: 70px; border: 1px solid #e2e8f0; border-radius: 4px; padding: 2px; background: white; }
    .nav-bar { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #f1f5f9; padding-bottom: 15px; margin-bottom: 20px; }
    .logout-btn { background: #64748b; font-size: 13px; padding: 6px 12px; }
</style>
"""

LOGIN_HTML = BASE_CSS + """
<div class="container" style="max-width: 400px; margin: 100px auto;">
    <h2>ResolveX Platform Login</h2>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <p style="color: red;">{{ messages[0] }}</p>
      {% endif %}
    {% endwith %}
    <form method="POST">
        <label>Username</label>
        <input type="text" name="username" required placeholder="citizen1, admin1, or super1">
        <label>Password</label>
        <input type="password" name="password" required>
        <button type="submit" style="width: 100%;">Login</button>
    </form>
</div>
"""

CITIZEN_HTML = BASE_CSS + """
<div class="container">
    <div class="nav-bar">
        <h2>Citizen Central Issue Dashboard</h2>
        <a href="{{ url_for('login') }}"><button class="logout-btn">Log Out</button></a>
    </div>
    
    <div class="grid">
        <div>
            <h3>Report New Infrastructure Issue</h3>
            <form method="POST" enctype="multipart/form-data">
                <label>Add Helpful Notes / Description</label>
                <textarea name="description" rows="3" placeholder="Describe the issue..."></textarea>
                
                <label>Preferred Translation Language (for Gemini output)</label>
                <select name="language">
                    <option value="English">English</option>
                    <option value="Spanish">Spanish</option>
                    <option value="Hindi">Hindi</option>
                    <option value="French">French</option>
                </select>
                
                <label>Upload Proof Photo (Analyzed by Gemini Vision)</label>
                <input type="file" name="image_file" accept="image/*">
                
                <button type="submit">Submit Complaint</button>
            </form>
        </div>
        
        <div>
            <h3>Civic Trust Score Performance Breakdown</h3>
            {% for dept, metrics in trust_scores.items() %}
                <div class="trust-card">
                    <div class="trust-header">
                        <span class="trust-title">{{ dept }}</span>
                        <span class="trust-score-badge">Trust Index: {{ metrics.overall }}</span>
                    </div>
                    <div class="metrics-grid">
                        <div class="metric-item"><span>Resolution Rate:</span><span class="metric-val">{{ metrics.resolution_rate }}%</span></div>
                        <div class="metric-item"><span>Response Speed:</span><span class="metric-val">{{ metrics.response_speed }}%</span></div>
                        <div class="metric-item"><span>SLA Adherence:</span><span class="metric-val">{{ metrics.sla_adherence }}%</span></div>
                        <div class="metric-item"><span>Citizen Satisfaction:</span><span class="metric-val">{{ metrics.citizen_sat }}%</span></div>
                    </div>
                </div>
            {% endfor %}
        </div>
    </div>

    <h3>Your Filed Incident History</h3>
    <table>
        <tr>
            <th>ID</th>
            <th>Category</th>
            <th>AI Assistant Summary Remarks</th>
            <th>Severity</th>
            <th>Status</th>
            <th>Scan to Track Status</th>
        </tr>
        {% for issue in issues %}
        <tr>
            <td>#{{ issue.id }}</td>
            <td><strong>{{ issue.category }}</strong></td>
            <td>{{ issue.description }}</td>
            <td>{{ issue.severity }}</td>
            <td><span class="badge status-{{ issue.status.replace(' ', '-') }}">{{ issue.status }}</span></td>
            <td>
                <img class="qr-img" src="{{ issue.qr_code }}" alt="QR Code"><br/>
                <small style="font-size:10px; color:#64748b;">Scan with Camera</small>
            </td>
        </tr>
        {% endfor %}
    </table>
</div>
"""

ADMIN_HTML = BASE_CSS + """
<div class="container">
    <div class="nav-bar">
        <h2>Operations Admin Action Panel</h2>
        <a href="{{ url_for('login') }}"><button class="logout-btn">Log Out</button></a>
    </div>

    <h3>Open Work-Order Database Row Operations</h3>
    <table>
        <tr>
            <th>ID</th>
            <th>Category & Logs</th>
            <th>Target Severity Modifier</th>
            <th>Execution Status Cycle</th>
            <th>Live Dynamic QR</th>
        </tr>
        {% for issue in issues %}
        <tr>
            <td>#{{ issue.id }}</td>
            <td>
                <strong>{{ issue.category }}</strong><br/>
                <small style="color: #475569;">{{ issue.description }}</small>
            </td>
            <form method="POST">
                <input type="hidden" name="issue_id" value="{{ issue.id }}">
                <td>
                    <select name="severity" style="margin:0; padding:5px;">
                        <option value="Low" {% if issue.severity == 'Low' %}selected{% endif %}>Low</option>
                        <option value="Medium" {% if issue.severity == 'Medium' %}selected{% endif %}>Medium</option>
                        <option value="High" {% if issue.severity == 'High' %}selected{% endif %}>High</option>
                        <option value="Critical" {% if issue.severity == 'Critical' %}selected{% endif %}>Critical</option>
                    </select>
                </td>
                <td>
                    <select name="status" style="margin:0; padding:5px;">
                        <option value="Not Yet Started" {% if issue.status == 'Not Yet Started' %}selected{% endif %}>Not Yet Started</option>
                        <option value="Under Progress" {% if issue.status == 'Under Progress' %}selected{% endif %}>Under Progress</option>
                        <option value="Resolved" {% if issue.status == 'Resolved' %}selected{% endif %}>Resolved</option>
                    </select>
                    <button type="submit" style="padding: 5px 10px; font-size:12px; margin-left:5px;">Update</button>
                </td>
            </form>
            <td><img class="qr-img" src="{{ issue.qr_code }}" alt="QR"></td>
        </tr>
        {% endfor %}
    </table>
</div>
"""

SUPERVISOR_HTML = BASE_CSS + """
<div class="container">
    <div class="nav-bar">
        <h2>Regional Management Supervisor Override Center</h2>
        <a href="{{ url_for('login') }}"><button class="logout-btn">Log Out</button></a>
    </div>

    <div style="margin-bottom: 30px;">
        <h3>Calculated Live Department Optimization Audits</h3>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:15px;">
            {% for dept, metrics in trust_scores.items() %}
                <div class="trust-card" style="margin:0;">
                    <div class="trust-header">
                        <span class="trust-title">{{ dept }}</span>
                        <span class="trust-score-badge" style="background:#0f172a;">Index: {{ metrics.overall }}</span>
                    </div>
                    <div class="metrics-grid">
                        <div class="metric-item"><span>Resolution Rate:</span><span class="metric-val">{{ metrics.resolution_rate }}%</span></div>
                        <div class="metric-item"><span>Response Speed:</span><span class="metric-val">{{ metrics.response_speed }}%</span></div>
                        <div class="metric-item"><span>SLA Adherence:</span><span class="metric-val">{{ metrics.sla_adherence }}%</span></div>
                        <div class="metric-item"><span>Citizen Satisfaction:</span><span class="metric-val">{{ metrics.citizen_sat }}%</span></div>
                    </div>
                </div>
            {% endfor %}
        </div>
    </div>

    <h3>Supervising Complaint Re-routing Parameters</h3>
    <table>
        <tr>
            <th>ID</th>
            <th>Description Summary</th>
            <th>Category Routing Domain</th>
            <th>Urgency Index Modifier</th>
            <th>QR Handle</th>
        </tr>
        {% for issue in issues %}
        <tr>
            <td>#{{ issue.id }}</td>
            <td><small>{{ issue.description }}</small></td>
            <form method="POST">
                <input type="hidden" name="issue_id" value="{{ issue.id }}">
                <td>
                    <select name="category" style="margin:0; padding:5px;">
                        <option value="Potholes & Road Damage" {% if issue.category == 'Potholes & Road Damage' %}selected{% endif %}>Potholes & Road Damage</option>
                        <option value="Garbage Accumulation" {% if issue.category == 'Garbage Accumulation' %}selected{% endif %}>Garbage Accumulation</option>
                        <option value="Water Leakage" {% if issue.category == 'Water Leakage' %}selected{% endif %}>Water Leakage</option>
                        <option value="Broken Streetlights" {% if issue.category == 'Broken Streetlights' %}selected{% endif %}>Broken Streetlights</option>
                        <option value="Drainage Issues" {% if issue.category == 'Drainage Issues' %}selected{% endif %}>Drainage Issues</option>
                        <option value="Traffic Signal Failures" {% if issue.category == 'Traffic Signal Failures' %}selected{% endif %}>Traffic Signal Failures</option>
                        <option value="Electrical Hazards" {% if issue.category == 'Electrical Hazards' %}selected{% endif %}>Electrical Hazards</option>
                        <option value="Public Safety Risks" {% if issue.category == 'Public Safety Risks' %}selected{% endif %}>Public Safety Risks</option>
                        <option value="Stray Dogs Issue" {% if issue.category == 'Stray Dogs Issue' %}selected{% endif %}>Stray Dogs Issue</option>
                    </select>
                </td>
                <td>
                    <select name="severity" style="margin:0; padding:5px;">
                        <option value="Low" {% if issue.severity == 'Low' %}selected{% endif %}>Low</option>
                        <option value="Medium" {% if issue.severity == 'Medium' %}selected{% endif %}>Medium</option>
                        <option value="High" {% if issue.severity == 'High' %}selected{% endif %}>High</option>
                        <option value="Critical" {% if issue.severity == 'Critical' %}selected{% endif %}>Critical</option>
                    </select>
                    <button type="submit" style="padding: 5px 10px; font-size:12px; margin-left:5px;">Route</button>
                </td>
            </form>
            <td><img class="qr-img" src="{{ issue.qr_code }}" alt="QR"></td>
        </tr>
        {% endfor %}
    </table>
</div>
"""

TRACK_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complaint Status Tracking</title>
    <style>
        body { font-family: system-ui, -apple-system, sans-serif; background: #f1f5f9; color: #1e293b; margin: 0; padding: 40px 20px; }
        .card { max-width: 500px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
        h2 { color: #0f172a; margin-top: 0; border-bottom: 2px solid #e2e8f0; padding-bottom: 15px; }
        .meta-item { margin: 20px 0; font-size: 16px; }
        .label { font-weight: bold; color: #64748b; text-transform: uppercase; font-size: 11px; display: block; margin-bottom: 5px; letter-spacing: 0.5px; }
        .value { font-size: 16px; color: #0f172a; font-weight: 500; }
        .badge { display: inline-block; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 13px; text-transform: uppercase; }
        .status-Resolved { background: #dcfce7; color: #15803d; }
        .status-Under-Progress { background: #fef9c3; color: #a16207; }
        .status-Not-Yet-Started { background: #fee2e2; color: #b91c1c; }
    </style>
</head>
<body>

<div class="card">
    <h2>ResolveX Complaint Tracking</h2>
    
    <div class="meta-item">
        <span class="label">Complaint Record Reference</span>
        <span class="value" style="font-family: monospace; font-size:18px;">#{{ issue.id }}</span>
    </div>
    
    <div class="meta-item">
        <span class="label">Assigned Core Category</span>
        <span class="value">{{ issue.category }}</span>
    </div>
    
    <div class="meta-item">
        <span class="label">AI Verification Diagnostics</span>
        <span class="value" style="font-style: italic; color:#475569;">"{{ issue.description }}"</span>
    </div>
    
    <div class="meta-item">
        <span class="label">System Severity Index</span>
        <span class="value">{{ issue.severity }}</span>
    </div>
    
    <div class="meta-item">
        <span class="label">Live Action Resolution Status</span>
        <span class="value">
            <span class="badge status-{{ issue.status.replace(' ', '-') }}">{{ issue.status }}</span>
        </span>
    </div>
</div>

</body>
</html>
"""

# --- ROUTES ---

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        
        if username in USERS_DB and USERS_DB[username]['password'] == password:
            user_role = USERS_DB[username]['role']
            if user_role == 'citizen': return redirect(url_for('citizen_dashboard'))
            elif user_role == 'admin': return redirect(url_for('admin_dashboard'))
            elif user_role == 'supervisor': return redirect(url_for('supervisor_dashboard'))
        else:
            flash("Invalid credentials. Please try again.", "error")
            
    return render_template_string(LOGIN_HTML)

@app.route('/citizen', methods=['GET', 'POST'])
def citizen_dashboard():
    if request.method == 'POST':
        user_text = request.form.get('description')
        selected_lang = request.form.get('language')
        uploaded_file = request.files.get('image_file')

        ai_category = "Public Safety Risks"
        ai_severity = "Medium"
        ai_analysis_text = "AI could not process the image metadata."

        if uploaded_file and uploaded_file.filename != '':
            try:
                image_bytes = uploaded_file.read()
                mime_type = uploaded_file.content_type if uploaded_file.content_type else "image/jpeg"

                prompt_instruction = f"""
                You are the computer vision core of ResolveX. Analyze the uploaded image and the citizen's notes: "{user_text}".
                
                You must extract and output exactly three lines and absolutely nothing else:
                Line 1 must start with "CATEGORY: " followed by exactly one of these supported categories:
                - Potholes & Road Damage
                - Garbage Accumulation
                - Water Leakage
                - Broken Streetlights
                - Drainage Issues
                - Traffic Signal Failures
                - Electrical Hazards
                - Public Safety Risks
                - Stray Dogs Issue

                Line 2 must start with "SEVERITY: " followed by exactly one word: Low, Medium, High, or Critical.
                Line 3 must start with "ANALYSIS: " followed by a brief summary analysis (max 2 sentences).
                
                CRITICAL TRANSLATION INSTRUCTION: You must write the text for Line 3 completely in this language: {selected_lang}.
                """

                response = ai_client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[
                        types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                        prompt_instruction
                    ]
                )

                response_text = response.text.strip()
                lines = response_text.split('\n')
                
                for line in lines:
                    if line.startswith("CATEGORY:"):
                        ai_category = line.replace("CATEGORY:", "").strip()
                    elif line.startswith("SEVERITY:"):
                        ai_severity = line.replace("SEVERITY:", "").strip()
                    elif line.startswith("ANALYSIS:"):
                        ai_analysis_text = line.replace("ANALYSIS:", "").strip()

            except Exception as e:
                ai_analysis_text = f"Error processing with Gemini API: {str(e)}"
                ai_severity = "Unknown (Error)"
                ai_category = "Public Safety Risks"

        new_issue = {
            "id": len(issues_db) + 1,
            "category": ai_category,
            "description": ai_analysis_text,
            "severity": ai_severity,
            "status": "Not Yet Started"
        }
        issues_db.append(new_issue)
        return redirect(url_for('citizen_dashboard'))

    for issue in issues_db:
        issue['qr_code'] = generate_qr_base64(issue['id'])

    scores = calculate_trust_scores()
    return render_template_string(CITIZEN_HTML, issues=issues_db, trust_scores=scores)

@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if request.method == 'POST':
        issue_id = int(request.form.get('issue_id'))
        new_status = request.form.get('status')
        new_severity = request.form.get('severity')
        
        for issue in issues_db:
            if issue['id'] == issue_id:
                issue['status'] = new_status
                issue['severity'] = new_severity
                break
        return redirect(url_for('admin_dashboard'))

    for issue in issues_db:
        issue['qr_code'] = generate_qr_base64(issue['id'])

    return render_template_string(ADMIN_HTML, issues=issues_db)

@app.route('/supervisor', methods=['GET', 'POST'])
def supervisor_dashboard():
    if request.method == 'POST':
        issue_id = int(request.form.get('issue_id'))
        new_category = request.form.get('category')
        new_severity = request.form.get('severity')
        
        for issue in issues_db:
            if issue['id'] == issue_id:
                issue['category'] = new_category
                issue['severity'] = new_severity
                break
        return redirect(url_for('supervisor_dashboard'))

    for issue in issues_db:
        issue['qr_code'] = generate_qr_base64(issue['id'])

    scores = calculate_trust_scores()
    return render_template_string(SUPERVISOR_HTML, issues=issues_db, trust_scores=scores)

@app.route('/track/<int:issue_id>')
def track_complaint(issue_id):
    matched_issue = next((issue for issue in issues_db if issue['id'] == issue_id), None)
    if not matched_issue:
        return "Complaint record reference parameters not found inside simulated base.", 404
        
    return render_template_string(TRACK_HTML, issue=matched_issue)

if __name__ == '__main__':
    app.run(debug=True)
