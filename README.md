# Hospital Management System

A compact role-based hospital workflow application built with **Python, Flask, SQLAlchemy, SQLite, Jinja2, and Bootstrap 5**.

The system models core workflows for three roles:

- **Admin** — manages departments, doctors, patients, and appointment oversight
- **Doctor** — manages availability, appointments, and treatment records
- **Patient** — manages profile information, browses doctors, books appointments, and reviews treatment history

## What it demonstrates

- Role-based authentication with Flask-Login
- Relational database modelling with SQLAlchemy ORM
- Doctor availability and appointment scheduling
- Double-booking prevention through database constraints and application checks
- Treatment and appointment history
- Profile and medical-information management
- Search and filtering workflows
- Server-rendered role-specific dashboards

## Application flow

```text
Department
    │
    ├── Doctors
    │     │
    │     └── Availability
    │
    └── Patients ──► Appointments ◄── Doctors
                         │
                         ▼
                     Treatment
```

## Database design

The application uses seven main entities:

| Entity | Purpose |
|---|---|
| Admin | Administrative accounts |
| Department | Hospital departments |
| Doctor | Doctor profiles and department assignment |
| Patient | Patient profiles and medical information |
| DoctorAvailability | Available appointment slots |
| Appointment | Patient-doctor bookings |
| Treatment | Visit details and medical records |

The design includes uniqueness constraints on doctor availability and appointment slots to prevent conflicting bookings.

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| ORM | Flask-SQLAlchemy / SQLAlchemy |
| Database | SQLite |
| Authentication | Flask-Login |
| Templates | Jinja2 |
| Frontend | Bootstrap 5, custom CSS |
| Security | Werkzeug password hashing |

## Run locally

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows**
```bash
.venv\Scripts\activate
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
cd Hospital_Management_System
pip install -r requirements.txt
```

### 3. Configure demo credentials

The database seeding script reads these optional environment variables:

```text
ADMIN_USER=admin@example.com
ADMIN_PASS=choose-a-strong-password
```

Doctor and patient demo credentials are also generated during seeding. Change them before using the application outside local development.

### 4. Initialize the database

```bash
python -m database.create_db
```

> **Warning:** the current initialization script recreates the database from scratch. Use it for a fresh local/demo environment, not as a production migration workflow.

### 5. Start the application

```bash
python app.py
```

The application runs locally on:

```text
http://127.0.0.1:5000
```

## Project structure

```text
Hospital_Management_System/
├── app.py
├── config.py
├── requirements.txt
├── models/
├── routes/
├── templates/
├── static/
└── database/
    └── create_db.py
```

## Notes

This is intentionally a lightweight supporting application rather than a production healthcare system. It demonstrates backend development, relational modelling, authentication, scheduling logic, and role-based workflows.

It should **not** be used with real patient data.

---
**Author:** Vihaan Bhambhani
