import os
from datetime import datetime, date, time, timedelta
from models.models import db, Department, Doctor, Patient, Appointment, DoctorAvailability, Admin
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from sqlalchemy import func, or_
from werkzeug.security import generate_password_hash
from routes.auth import role_required

admin_bp = Blueprint("admin", __name__, template_folder="../templates")


# ---------- helpers ----------

def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


# ---------- dashboard ----------

@admin_bp.route("/dashboard")
@role_required("admin")
def dashboard():
    counts = {
        "doctors": Doctor.query.count(),
        "patients": Patient.query.count(),
        "appointments": Appointment.query.count(),
    }

    upcoming = (
        Appointment.query.filter(Appointment.status == "Booked")
        .order_by(Appointment.date.asc(), Appointment.start_time.asc())
        .limit(10)
        .all()
    )

    return render_template("admin/dashboard.html", counts=counts, upcoming=upcoming)


# ---------- doctor CRUD + default availability ----------

@admin_bp.route("/doctors", methods=["GET", "POST"])
@role_required("admin")
def doctors():
    depts = Department.query.order_by(Department.name.asc()).all()

    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip()
        dept_id = to_int(request.form.get("department_id"))
        years = to_int(request.form.get("years_experience"))
        password = request.form.get("password") or os.environ.get("DOCTOR_DEFAULT_PASSWORD") or "local-development-only-change-me"

        if not name or not email or not dept_id:
            flash("Name, email and department are required.", "warning")
            return redirect(url_for("admin.doctors"))

        if Doctor.query.filter_by(email=email).first():
            flash("Doctor already exists with this email.", "warning")
            return redirect(url_for("admin.doctors"))

        hashed_pw = generate_password_hash(password)

        # create doctor
        doc = Doctor(
            name=name,
            email=email,
            department_id=dept_id,
            years_experience=years,
            password_hash=hashed_pw,
        )
        db.session.add(doc)
        db.session.commit()

        # seed 7 days x 2 slots/day default availability
        today = date.today()
        slot_defs = [
            (time(10, 0), time(12, 0)),
            (time(16, 0), time(18, 0)),
        ]

        for offset in range(7):
            day = today + timedelta(days=offset)
            for start, end in slot_defs:
                exists = DoctorAvailability.query.filter_by(
                    doctor_id=doc.id,
                    date=day,
                    start_time=start,
                    end_time=end,
                ).first()
                if exists:
                    continue

                db.session.add(
                    DoctorAvailability(
                        doctor_id=doc.id,
                        date=day,
                        start_time=start,