# ResolveX
ResolveX is an AI-powered civic issue reporting platform that lets users report problems by uploading an image, location, and description. Gemini AI automatically detects the issue category and severity, helping prioritize cases. It improves transparency, speeds up reporting, and enables efficient resolution by connecting citizens with authorities.

# 📌 Problem Statement

Cities face thousands of unresolved civic issues every day such as:
- Garbage overflow
- Water leakage
- Road damage
- Broken street lights
- Drainage issues
- Stray animal complaints

Citizens often struggle to:
- Report issues easily
- Track complaint progress
- Receive timely updates
- Trust civic management systems

ResolveX provides a smart and transparent platform where citizens can report civic issues, track progress, and authorities can manage complaints efficiently using AI-powered analysis.

---

# 🎯 Project Objective

ResolveX aims to:
- Simplify civic issue reporting
- Improve transparency
- Reduce complaint resolution delays
- Use AI for automatic issue analysis
- Build trust between citizens and authorities

---

# 🧠 Features

## 👤 User Authentication
- Signup/Login system
- Flask session authentication
- Password hashing
- Role-based access

### Roles:
- Citizen
- Official
- Supervisor

---

# 🏠 Role-Based Dashboards

## 👥 Citizen Dashboard
- Report civic issues
- Track complaint status
- View complaint history
- Civic Trust Score
- Notifications
- Download complaint reports

## 🏢 Official Dashboard
- View assigned complaints
- Update complaint status
- Upload resolution proof
- Mark complaints resolved

## 🛡️ Supervisor Dashboard
- Monitor all complaints
- View analytics dashboard
- Reassign complaints
- Track SLA delays
- Monitor official performance

---

# 📍 Issue Reporting System

Citizens can:
- Upload complaint image
- Enter issue title
- Add description
- Add location
- Use auto geolocation


### Categories
- Garbage
- Water Leakage
- Road Damage
- Street Light
- Drainage
- Stray Dogs
- Others

### Severity Levels
| Severity | Color |
|---|---|
| High | 🔴 Red |
| Medium | 🟡 Yellow |
| Low | 🟢 Green |

Uploaded files are stored locally in:
```text
static/uploads/
```

# 🤖 AI Image Analysis (Google Gemini API)

When a user uploads an image:
- Gemini AI analyzes the complaint image
- Detects issue category
- Predicts severity
- Suggests department
- Detects spam/fake images


### Example AI Output

```text
Issue Detected: Garbage Overflow
Severity: High
Department: Sanitation
```

# 🌐 Multi-Language Support

Supported Languages:
- English
- Hindi
- Kannada

Gemini AI generates responses in the user-selected language for a more accessible and inclusive experience.
Confidence: 92%

# 📱 QR Code Complaint Tracking

Every complaint generates a unique QR code.

When scanned:
- Opens the complaint tracking page directly

QR codes are stored locally in:

```text
static/qr_codes/
```
# 📊 Public Transparency Dashboard

A public analytics dashboard displaying real-time civic complaint statistics and transparency reports.

### Features:
- Total complaints
- Resolved complaints
- Pending complaints
- Average response time
- Most common issue categories

### Dashboard Includes:
- 📈 Charts
- 📋 Analytics cards
- 📊 Statistics
- 📉 Visual reports

Built using:
- Chart.js
# ⏰ SLA Escalation System

If a complaint is not updated within:

```text
48 hours
```

The system automatically:
- Flags the complaint
- Notifies the supervisor
- Highlights delayed cases for faster resolution
