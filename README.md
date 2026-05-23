# ResolveX

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Gemini AI](https://img.shields.io/badge/Gemini_AI-4285F4?style=for-the-badge&logo=google&logoColor=white)
![HTML](https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![QR_Code](https://img.shields.io/badge/QR_Tracking-111827?style=for-the-badge)
![Hackathon](https://img.shields.io/badge/Hackathon_Project-FF6B00?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Prototype-success?style=for-the-badge)

ResolveX is an AI-powered civic issue reporting platform that enables citizens to report infrastructure issues through image submission and AI-assisted analysis.

# Problem Statement

Urban civic issues are often:
- Difficult to report
- Slow to resolve
- Hard to track
- Lacking transparency

Citizens frequently experience:
- Delayed action
- No visibility into progress
- Poor communication with authorities

ResolveX addresses this using AI-assisted issue analysis and transparent tracking.

# Project Objective

ResolveX aims to:

- Simplify complaint reporting
- Automate issue categorization
- Improve operational transparency
- Enable complaint tracking
- Support multilingual accessibility

# Features

## AI Complaint Analysis
Citizens upload an image.

Gemini AI automatically:
- Detects civic issue category
- Estimates severity
- Generates complaint summary
- Produces output in selected language

Supported categories:
- Potholes & Road Damage
- Garbage Accumulation
- Water Leakage
- Broken Streetlights
- Drainage Issues
- Traffic Signal Failures
- Electrical Hazards
- Public Safety Risks
- Stray Dogs Issue

Severity Levels:
- Low
- Medium
- High
- Critical

## Citizen Dashboard

Citizens can:

- Upload issue images
- Add issue description
- Select preferred language
- Submit complaints
- View complaint history
- Track complaints using QR code
- View Civic Trust Scores

## Admin Dashboard

Admins can:
- View complaint records
- Update complaint severity
- Change complaint resolution status

Statuses:
- Not Yet Started
- Under Progress
- Resolved

## Supervisor Dashboard

Supervisors can:
- Reassign issue categories
- Adjust severity
- Monitor department trust metrics
- Review complaint routing

## QR Complaint Tracking

Each complaint generates a QR code.
Scanning opens:

```text
/track/<issue_id>
```

Users can view:
- Complaint ID
- Category
- AI Summary
- Severity
- Resolution Status

## Civic Trust Score

ResolveX calculates department trust using:

- Resolution Rate
- Response Speed
- SLA Adherence
- Citizen Satisfaction

Departments:
- Public Works
- Waste Management
- Water Supply
- Electrical
- Traffic Control
- Public Safety

## Multi-Language Support

Supported languages:
- English
- Hindi
- Kannada
AI analysis is returned in the selected language.

# Tech Stack

| Category | Technology |
|----------|------------|
| Frontend | ![HTML](https://img.shields.io/badge/HTML-E34F26?logo=html5&logoColor=white) ![CSS](https://img.shields.io/badge/CSS-1572B6?logo=css3&logoColor=white) |
| Backend | ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-black?logo=flask&logoColor=white) |
| AI | ![Gemini](https://img.shields.io/badge/Gemini_AI-4285F4?logo=google&logoColor=white) |
| Storage | ![Memory](https://img.shields.io/badge/In_Memory-34A853?style=flat) |
| Deployment | ![Render](https://img.shields.io/badge/Render-46E3B7?logo=render&logoColor=black) |

## Frontend
- HTML  
## Backend
- Python
- Flask
## AI
- Google Gemini API
## Libraries
- google-genai
- qrcode
- Pillow
- python-dotenv
## Data Storage
- Temporary in-memory Python structures

# Project Structure

```text
ResolveX/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── templates/
│   ├── login.html
│   ├── citizen.html
│   ├── admin.html
│   ├── supervisor.html
│   └── track.html
│
└── .env (local only)
```

---

# Installation

Clone:

```bash
git clone <repo_url>
cd ResolveX
```

Install:

```bash
pip install -r requirements.txt
```

Create `.env`

```env
GEMINI_API_KEY=your_api_key
```

Run:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

# Demo Credentials

Citizen:
```text
citizen1
password123
```

Admin:
```text
admin1
admin123
```

Supervisor:
```text
super1
super123
```

---

# Future Improvements
- Database integration
- Authentication system
- Complaint notifications
- File storage
- Government integration
- Analytics dashboard

# Hackathon Highlights
- AI Vision Analysis
- QR Complaint Tracking
- Role-Based Dashboards
- Department Trust Metrics
- Multi-language Support
  
# Project Status

🟢 Core Platform Complete  
🟢 Gemini AI Integrated  
🟢 QR Tracking Implemented  
🟢 Multi-language Support Enabled  
🟢 Deployment Ready  
🟡 Database Integration (Future)  


# Vision
Report → Analyze → Track → Resolve
Building smarter and more transparent civic management.

Report → Analyze → Track → Resolve

Building smarter and more transparent civic management.
