# EVCS Threat Intelligence API

## Overview

This API simulates a **security monitoring system for EV Charging Stations (EVCS)**. Charging stations can report detected threats (such as ransomware, denial-of-service attacks, or unauthorised access attempts) to a central Flask API, which stores and exposes them for operator review.

This project was built as part of **CFG Assignment 4 — Creating APIs in Python**.

---

## Project Structure

```
evcs_threat_api/
├── app.py          # Flask API — defines all 3 endpoints
├── db_utils.py     # Database connection and query helpers
├── config.py       # Database and Flask configuration (edit this first!)
├── main.py         # Client-side simulation — run to test the API
├── schema.sql      # MySQL database and table setup
└── README.md       # This file
```

---

## Setup Instructions

### 1. Prerequisites

Make sure you have the following installed:

- Python 3.8+
- MySQL (accessible via DBeaver or MySQL CLI)
- pip

### 2. Install Python dependencies

```bash
pip install flask mysql-connector-python requests python-dotenv
```

### 3. Set up the database

Open **DBeaver**, connect to your local MySQL server, and run the contents of `schema.sql`. This will:

- Create a database called `evcs_security`
- Create the `threats` table

Alternatively, from the MySQL CLI:

```bash
mysql -u your_username -p < schema.sql
```

### 4. Set up your credentials

Copy `.env.example` to a new file called `.env` in the same directory:

```bash
cp .env.example .env
```

Then open `.env` and fill in your real MySQL credentials:

```
DB_USER=root
DB_PASSWORD=your_actual_password
```

> ⚠️ The `.env` file is listed in `.gitignore` and will NOT be pushed to GitHub. Your credentials stay on your machine. Share the `.env` file directly with your instructor for marking.

---

## Running the API

### Step 1 — Start the Flask server

In one terminal:

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### Step 2 — Run the client simulation

In a second terminal:

```bash
python main.py
```

This simulates charging stations reporting threats, an operator viewing all active threats, and drilling into a specific station's incident history.

---

## API Endpoints

### `POST /report-threat`

Report a new security threat from a charging station.

**Request body (JSON):**
```json
{
  "station_id": "EVCS-UK-001",
  "threat_type": "ransomware",
  "severity": "critical",
  "description": "Ransomware detected on billing subsystem."
}
```

**Valid threat types:** `ransomware`, `dos`, `mitm`, `unauthorised_access`, `malware`, `unknown`  
**Valid severities:** `low`, `medium`, `high`, `critical`

**Response (201):**
```json
{
  "message": "Threat reported successfully.",
  "threat_id": 1,
  "station_id": "EVCS-UK-001"
}
```

---

### `GET /threats`

Retrieve all threats. Optionally filter by status.

**Optional query parameter:** `?status=active` or `?status=resolved`

**Example:**
```
GET http://127.0.0.1:5000/threats?status=active
```

**Response (200):**
```json
{
  "count": 2,
  "threats": [
    {
      "id": 1,
      "station_id": "EVCS-UK-001",
      "threat_type": "ransomware",
      "severity": "critical",
      "description": "...",
      "status": "active",
      "detected_at": "2025-01-01 12:00:00"
    }
  ]
}
```

---

### `GET /threats/<station_id>`

Retrieve all threats for a specific station, plus a severity breakdown.

**Example:**
```
GET http://127.0.0.1:5000/threats/EVCS-UK-001
```

**Response (200):**
```json
{
  "station_id": "EVCS-UK-001",
  "total_threats": 2,
  "severity_summary": [
    { "severity": "critical", "count": 1 },
    { "severity": "medium", "count": 1 }
  ],
  "threats": [...]
}
```

---

## Testing with Postman

You can test all endpoints in Postman:

1. **POST** `http://127.0.0.1:5000/report-threat` — set Body to raw JSON
2. **GET** `http://127.0.0.1:5000/threats` — add `status` as a query param if needed
3. **GET** `http://127.0.0.1:5000/threats/EVCS-UK-001`

---

## Git & GitHub Submission

1. Create a branch: `assignment-4-APIs`
2. Commit all `.py` and `.sql` files
3. Open a Pull Request against `main` with a title and description