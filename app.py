import os
import re
from functools import wraps
from datetime import datetime, date

from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

from config import Config

# -------------------------------------
# App setup
# -------------------------------------
app = Flask(__name__)
app.config.from_object(Config)
bcrypt = Bcrypt(app)

# Upload configuration
UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# -------------------------------------
# Database helpers
# -------------------------------------
def get_db():
    return mysql.connector.connect(
        host=app.config["MYSQL_HOST"],
        user=app.config["MYSQL_USER"],
        password=app.config["MYSQL_PASSWORD"],
        database=app.config["MYSQL_DATABASE"],
        port=app.config.get("MYSQL_PORT", 3306),
    )

_TABLE_COLUMNS_CACHE = {}

def get_table_columns(table: str) -> set[str]:
    if table in _TABLE_COLUMNS_CACHE:
        return _TABLE_COLUMNS_CACHE[table]

    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute(f"SHOW COLUMNS FROM {table}")
    cols = {row["Field"] for row in cur.fetchall()}
    cur.close()
    conn.close()

    _TABLE_COLUMNS_CACHE[table] = cols
    return cols


# -------------------------------------
# Auth decorator
# -------------------------------------
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "doctor_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


# -------------------------------------
# Static / Home
# -------------------------------------
@app.route("/")
def home():
    if session.get("doctor_id"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/ehr_info")
def ehr_info():
    return render_template("ehr_info.html")


# -------------------------------------
# Password policy
# -------------------------------------
def is_strong_password(pw: str) -> bool:
    if not pw or len(pw) < 8:
        return False
    has_upper = re.search(r"[A-Z]", pw) is not None
    has_lower = re.search(r"[a-z]", pw) is not None
    has_num = re.search(r"\d", pw) is not None
    return has_upper and has_lower and has_num


# -------------------------------------
# Auth routes
# -------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("register.html")

        if not is_strong_password(password):
            flash("Password too weak. Use 8+ chars with upper, lower and a number.", "warning")
            return render_template("register.html")

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        conn = get_db()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT doctor_id FROM doctors WHERE email=%s", (email,))
        if cur.fetchone():
            cur.close()
            conn.close()
            flash("Email already registered.", "warning")
            return render_template("register.html")

        cur.execute(
            "INSERT INTO doctors (name, email, password_hash) VALUES (%s, %s, %s)",
            (name, email, hashed_password),
        )
        conn.commit()
        cur.close()
        conn.close()

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM doctors WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and bcrypt.check_password_hash(user["password_hash"], password):
            session["doctor_id"] = user["doctor_id"]
            session["doctor_name"] = user["name"]
            flash("Logged in successfully.", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("login"))


# -------------------------------------
# Dashboard
# -------------------------------------
from datetime import date

@app.route("/dashboard")
@login_required
def dashboard():
    from datetime import date, timedelta

    conn = get_db()
    cur = conn.cursor(dictionary=True)

    # Total patients for this doctor
    cur.execute(
        "SELECT COUNT(*) AS cnt FROM patients WHERE doctorid = %s",
        (session["doctor_id"],)
    )
    row = cur.fetchone()
    total_patients = (row["cnt"] if row and "cnt" in row else 0)

    # Recent patients (latest 5)
    cur.execute(
        """
        SELECT patientid, name, gender, dateofbirth, symptoms
        FROM patients
        WHERE doctorid = %s
        ORDER BY patientid DESC
        LIMIT 5
        """,
        (session["doctor_id"],)
    )
    recent_patients = cur.fetchall() or []

    # Date buckets
    today_dt = date.today()
    yesterday_dt = today_dt - timedelta(days=1)
    tomorrow_dt = today_dt + timedelta(days=1)

    # 7-day window: today -> today+7 (inclusive)
    week_start_dt = today_dt
    week_end_dt = today_dt + timedelta(days=7)

    today = today_dt.isoformat()
    yesterday = yesterday_dt.isoformat()
    tomorrow = tomorrow_dt.isoformat()
    week_start = week_start_dt.isoformat()
    week_end = week_end_dt.isoformat()

       # --- Appointments by buckets ---

    # YESTERDAY (visited + not visited)
    cur.execute(
        """
        SELECT
            patientid,
            name,
            gender,
            dateofbirth,
            smoker,
            weight,
            height,
            allergies,
            symptoms,
            visit_date,
            visit_time,
            visited
        FROM patients
        WHERE doctorid = %s
          AND visit_date IS NOT NULL
          AND DATE(visit_date) = %s
        ORDER BY
          visited ASC,
          visit_time IS NULL,
          visit_time ASC,
          patientid ASC
        """,
        (session["doctor_id"], yesterday)
    )
    appt_yesterday = cur.fetchall() or []

    # TODAY (upcoming only)
    cur.execute(
        """
        SELECT
            patientid,
            name,
            gender,
            dateofbirth,
            smoker,
            weight,
            height,
            allergies,
            symptoms,
            visit_date,
            visit_time,
            visited
        FROM patients
        WHERE doctorid = %s
          AND visit_date IS NOT NULL
          AND DATE(visit_date) = %s
          AND visited = 0
        ORDER BY
          visit_time IS NULL,
          visit_time ASC,
          patientid ASC
        """,
        (session["doctor_id"], today)
    )
    appt_today = cur.fetchall() or []

    # TOMORROW (upcoming only)
    cur.execute(
        """
        SELECT
            patientid,
            name,
            gender,
            dateofbirth,
            smoker,
            weight,
            height,
            allergies,
            symptoms,
            visit_date,
            visit_time,
            visited
        FROM patients
        WHERE doctorid = %s
          AND visit_date IS NOT NULL
          AND DATE(visit_date) = %s
          AND visited = 0
        ORDER BY
          visit_time IS NULL,
          visit_time ASC,
          patientid ASC
        """,
        (session["doctor_id"], tomorrow)
    )
    appt_tomorrow = cur.fetchall() or []

    # NEXT 7 DAYS (upcoming only)
    cur.execute(
        """
        SELECT
            patientid,
            name,
            gender,
            dateofbirth,
            smoker,
            weight,
            height,
            allergies,
            symptoms,
            visit_date,
            visit_time,
            visited
        FROM patients
        WHERE doctorid = %s
          AND visit_date IS NOT NULL
          AND DATE(visit_date) BETWEEN %s AND %s
          AND visited = 0
        ORDER BY
          DATE(visit_date) ASC,
          visit_time IS NULL,
          visit_time ASC,
          patientid ASC
        """,
        (session["doctor_id"], week_start, week_end)
    )
    appt_7day = cur.fetchall() or []


    cur.close()
    conn.close()

    # Basic alerts
    alerts = []
    for p in recent_patients:
        s = (p.get("symptoms") or "").lower()
        if "chest" in s or "shortness" in s or "dyspnea" in s:
            alerts.append(f"Possible urgent symptom in recent record: {p.get('name')}")

    stats = {
        "total_patients": total_patients,
        "recent_count": len(recent_patients),
    }

    return render_template(
        "dashboard.html",
        doctor=session.get("doctor_name"),
        stats=stats,
        recent_patients=recent_patients,
        appointments_today=appt_today,
        appointments_yesterday=appt_yesterday,
        appointments_tomorrow=appt_tomorrow,
        appointments_7day=appt_7day,
        week_start=week_start_dt.strftime("%d.%m"),
        week_end=week_end_dt.strftime("%d.%m"),
        alerts=alerts
    )

# -------------------------------------
# Patients helpers
# -------------------------------------
def allergies_options_list():
    return ["Peanuts", "Dust", "Latex", "Pollen", "Gluten", "None"]


# -------------------------------------
# Patients list (Upcoming + Visited)
# -------------------------------------
@app.route("/patients")
@login_required
def patients():
    import datetime as dt

    conn = get_db()
    cur = conn.cursor(dictionary=True)

    # If you have auto-move logic based on visit_date in the past,
    # keep it EXACTLY like you had it. This is a safe example:
    today = dt.date.today()

    # OPTIONAL: if your app already marks past appointments as visited, keep it.
    # If you don't have this in your current function, remove this block.
    try:
        cur.execute(
            """
            UPDATE patients
            SET visited = 1
            WHERE doctorid = %s
              AND visited = 0
              AND visit_date IS NOT NULL
              AND DATE(visit_date) < %s
            """,
            (session["doctor_id"], today.isoformat())
        )
        conn.commit()
    except Exception:
        # If your DB doesn't like DATE(visit_date) because visit_date isn't a date,
        # or if you didn't want auto-update, comment out the UPDATE block above.
        pass

    # Upcoming
    cur.execute(
        """
        SELECT *
        FROM patients
        WHERE doctorid = %s AND visited = 0
        ORDER BY
          (visit_date IS NULL) ASC,
          DATE(visit_date) ASC,
          (visit_time IS NULL) ASC,
          visit_time ASC,
          patientid DESC
        """,
        (session["doctor_id"],)
    )
    upcoming = cur.fetchall() or []

    # Visited
    cur.execute(
        """
        SELECT *
        FROM patients
        WHERE doctorid = %s AND visited = 1
        ORDER BY
          DATE(visit_date) DESC,
          (visit_time IS NULL) ASC,
          visit_time ASC,
          patientid DESC
        """,
        (session["doctor_id"],)
    )
    visited = cur.fetchall() or []

    cur.close()
    conn.close()

    return render_template(
        "patients.html",
        upcoming=upcoming,
        visited=visited,
        current_year=dt.date.today().year
    )


# -------------------------------------
# Add patient
# -------------------------------------
@app.route("/add_patient", methods=["GET", "POST"])
@login_required
def add_patient():
    allergies_options = allergies_options_list()
    patient_cols = get_table_columns("patients")

    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        gender = request.form.get("gender")
        dob = request.form.get("dob")  # YYYY-MM-DD
        weight = request.form.get("weight")
        height = request.form.get("height")
        visit_date = request.form.get("visit_date")
        smoker = 1 if request.form.get("smoker") else 0
        visit_time = (request.form.get("visit_time") or "").strip()

        symptoms = (request.form.get("symptoms") or "").strip()
        diagnosis = (request.form.get("diagnosis") or "").strip()

        # ✅ SOAP notes
        soap_subjective = (request.form.get("soap_subjective") or "").strip()
        soap_objective = (request.form.get("soap_objective") or "").strip()
        soap_assessment = (request.form.get("soap_assessment") or "").strip()
        soap_plan = (request.form.get("soap_plan") or "").strip()

        allergies_list = request.form.getlist("allergies")
        extra_allergies = (request.form.get("extra_allergies") or "").strip()

        if not name or not gender or not dob:
            flash("Name, gender, and date of birth are required.", "danger")
            return render_template("add_patient.html", allergies_options=allergies_options)

        allergies = ", ".join(allergies_list)
        if extra_allergies:
            allergies = f"{allergies}, {extra_allergies}" if allergies else extra_allergies

        # Optional radiology upload
        radiology_filename = None
        file = request.files.get("radiology_image")
        if file and file.filename:
            if not allowed_file(file.filename):
                flash("Only png/jpg/jpeg/webp images allowed.", "danger")
                return render_template("add_patient.html", allergies_options=allergies_options)

            safe = secure_filename(file.filename)
            stamp = datetime.now().strftime("%Y%m%d%H%M%S")
            radiology_filename = f"doc{session['doctor_id']}_{stamp}_{safe}"
            file.save(os.path.join(UPLOAD_FOLDER, radiology_filename))

        # Dynamic INSERT (safe if columns missing)
        cols = ["doctorid", "name", "gender", "dateofbirth", "weight", "allergies"]
        vals = [session["doctor_id"], name, gender, dob, weight, allergies]

        if "height" in patient_cols:
            cols.append("height"); vals.append(height)
        if "visit_date" in patient_cols:
            cols.append("visit_date"); vals.append(visit_date)
        if "visit_time" in patient_cols:
            cols.append("visit_time"); vals.append(visit_time if visit_time else None)

        if "smoker" in patient_cols:
            cols.append("smoker"); vals.append(smoker)
        if "symptoms" in patient_cols:
            cols.append("symptoms"); vals.append(symptoms)
        if "visited" in patient_cols:
            cols.append("visited"); vals.append(0)

        if "diagnosis" in patient_cols:
            cols.append("diagnosis"); vals.append(diagnosis)

        # ✅ SOAP notes only if the columns exist
        if "soap_subjective" in patient_cols:
            cols.append("soap_subjective"); vals.append(soap_subjective)
        if "soap_objective" in patient_cols:
            cols.append("soap_objective"); vals.append(soap_objective)
        if "soap_assessment" in patient_cols:
            cols.append("soap_assessment"); vals.append(soap_assessment)
        if "soap_plan" in patient_cols:
            cols.append("soap_plan"); vals.append(soap_plan)

        if radiology_filename and "radiology_image" in patient_cols:
            cols.append("radiology_image"); vals.append(radiology_filename)

        placeholders = ", ".join(["%s"] * len(cols))
        col_sql = ", ".join(cols)

        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute(f"INSERT INTO patients ({col_sql}) VALUES ({placeholders})", tuple(vals))
        conn.commit()
        cur.close()
        conn.close()

        flash("Patient created.", "success")
        return redirect(url_for("patients"))

    return render_template("add_patient.html", allergies_options=allergies_options)

# -------------------------------------
# Edit patient
# -------------------------------------
@app.route("/edit_patient/<int:patient_id>", methods=["GET", "POST"])
@login_required
def edit_patient(patient_id):
    allergies_options = allergies_options_list()
    patient_cols = get_table_columns("patients")

    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM patients WHERE patientid=%s AND doctorid=%s", (patient_id, session["doctor_id"]))
    patient = cur.fetchone()

    if not patient:
        cur.close()
        conn.close()
        flash("Patient not found (or not yours).", "danger")
        return redirect(url_for("patients"))

    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        gender = request.form.get("gender")
        dob = request.form.get("dob")
        weight = request.form.get("weight")
        height = request.form.get("height")
        visit_date = request.form.get("visit_date")
        smoker = 1 if request.form.get("smoker") else 0
        visit_time = (request.form.get("visit_time") or "").strip()

        symptoms = (request.form.get("symptoms") or "").strip()
        visited_flag = 1 if request.form.get("visited") else 0

        diagnosis = (request.form.get("diagnosis") or "").strip()

        # ✅ SOAP notes
        soap_subjective = (request.form.get("soap_subjective") or "").strip()
        soap_objective = (request.form.get("soap_objective") or "").strip()
        soap_assessment = (request.form.get("soap_assessment") or "").strip()
        soap_plan = (request.form.get("soap_plan") or "").strip()

        allergies_list = request.form.getlist("allergies")
        extra_allergies = (request.form.get("extra_allergies") or "").strip()

        if not name or not gender or not dob:
            flash("Name, gender, and date of birth are required.", "danger")
            cur.close()
            conn.close()
            return render_template("edit_patient.html", patient=patient, allergies_options=allergies_options)

        allergies = ", ".join(allergies_list)
        if extra_allergies:
            allergies = f"{allergies}, {extra_allergies}" if allergies else extra_allergies

        # Optional new radiology upload
        radiology_filename = None
        file = request.files.get("radiology_image")
        if file and file.filename:
            if not allowed_file(file.filename):
                flash("Only png/jpg/jpeg/webp images allowed.", "danger")
                cur.close()
                conn.close()
                return render_template("edit_patient.html", patient=patient, allergies_options=allergies_options)

            safe = secure_filename(file.filename)
            stamp = datetime.now().strftime("%Y%m%d%H%M%S")
            radiology_filename = f"doc{session['doctor_id']}_p{patient_id}_{stamp}_{safe}"
            file.save(os.path.join(UPLOAD_FOLDER, radiology_filename))

        # Dynamic UPDATE
        set_parts = ["name=%s", "gender=%s", "dateofbirth=%s", "weight=%s", "allergies=%s"]
        vals = [name, gender, dob, weight, allergies]

        if "height" in patient_cols:
            set_parts.append("height=%s"); vals.append(height)
        if "visit_date" in patient_cols:
            set_parts.append("visit_date=%s"); vals.append(visit_date)
        if "visit_time" in patient_cols:
            set_parts.append("visit_time=%s"); vals.append(visit_time if visit_time else None)

        if "smoker" in patient_cols:
            set_parts.append("smoker=%s"); vals.append(smoker)
        if "symptoms" in patient_cols:
            set_parts.append("symptoms=%s"); vals.append(symptoms)
        if "visited" in patient_cols:
            set_parts.append("visited=%s"); vals.append(visited_flag)

        if "diagnosis" in patient_cols:
            set_parts.append("diagnosis=%s"); vals.append(diagnosis)

        # ✅ SOAP notes only if the columns exist
        if "soap_subjective" in patient_cols:
            set_parts.append("soap_subjective=%s"); vals.append(soap_subjective)
        if "soap_objective" in patient_cols:
            set_parts.append("soap_objective=%s"); vals.append(soap_objective)
        if "soap_assessment" in patient_cols:
            set_parts.append("soap_assessment=%s"); vals.append(soap_assessment)
        if "soap_plan" in patient_cols:
            set_parts.append("soap_plan=%s"); vals.append(soap_plan)

        if radiology_filename and "radiology_image" in patient_cols:
            set_parts.append("radiology_image=%s"); vals.append(radiology_filename)

        vals.extend([patient_id, session["doctor_id"]])

        cur.execute(
            f"UPDATE patients SET {', '.join(set_parts)} WHERE patientid=%s AND doctorid=%s",
            tuple(vals),
        )
        conn.commit()
        cur.close()
        conn.close()

        flash("Patient updated.", "success")
        return redirect(url_for("patients"))

    cur.close()
    conn.close()
    return render_template("edit_patient.html", patient=patient, allergies_options=allergies_options)

# -------------------------------------
# Delete patient
# -------------------------------------
@app.route("/delete_patient/<int:patient_id>")
@login_required
def delete_patient(patient_id):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("DELETE FROM patients WHERE patientid=%s AND doctorid=%s", (patient_id, session["doctor_id"]))
    conn.commit()
    cur.close()
    conn.close()

    flash("Patient deleted.", "info")
    return redirect(url_for("patients"))

from datetime import date

@app.route("/patient/<int:patient_id>/revisit", methods=["POST"])
@login_required
def revisit_patient(patient_id):
    import datetime as dt

    when = (request.form.get("when") or "").strip()
    days_map = {"1w": 7, "2w": 14, "1m": 30}

    if when not in days_map:
        flash("Invalid revisit option.", "danger")
        return redirect(url_for("patients"))

    new_date = (dt.date.today() + dt.timedelta(days=days_map[when])).isoformat()

    patient_cols = get_table_columns("patients")

    conn = get_db()
    cur = conn.cursor(dictionary=True)

    # Fetch the original (visited) record
    cur.execute(
        "SELECT * FROM patients WHERE patientid=%s AND doctorid=%s",
        (patient_id, session["doctor_id"])
    )
    old = cur.fetchone()
    if not old:
        cur.close()
        conn.close()
        flash("Patient not found (or not yours).", "danger")
        return redirect(url_for("patients"))

    # Build a new row (clone demographics + schedule)
    # NOTE: We intentionally DO NOT copy diagnosis; revisit is a new encounter.
    cols = ["doctorid", "name", "gender", "dateofbirth", "weight", "allergies"]
    vals = [
        session["doctor_id"],
        old.get("name"),
        old.get("gender"),
        old.get("dateofbirth"),
        old.get("weight"),
        old.get("allergies"),
    ]

    # Optional columns if they exist
    if "height" in patient_cols:
        cols.append("height"); vals.append(old.get("height"))

    if "smoker" in patient_cols:
        cols.append("smoker"); vals.append(old.get("smoker"))

    if "symptoms" in patient_cols:
        cols.append("symptoms"); vals.append(old.get("symptoms"))

    # Scheduling
    if "visit_date" in patient_cols:
        cols.append("visit_date"); vals.append(new_date)

    if "visit_time" in patient_cols:
        cols.append("visit_time"); vals.append(None)

    if "visited" in patient_cols:
        cols.append("visited"); vals.append(0)

    # Mark revisit + link back
    if "is_revisit" in patient_cols:
        cols.append("is_revisit"); vals.append(1)

    if "revisit_from" in patient_cols:
        cols.append("revisit_from"); vals.append(patient_id)

    # Optionally carry radiology image forward (usually you DON'T, but you can)
    if "radiology_image" in patient_cols and old.get("radiology_image"):
        cols.append("radiology_image"); vals.append(old.get("radiology_image"))

    placeholders = ", ".join(["%s"] * len(cols))
    col_sql = ", ".join(cols)

    cur.execute(
        f"INSERT INTO patients ({col_sql}) VALUES ({placeholders})",
        tuple(vals)
    )
    conn.commit()

    cur.close()
    conn.close()

    flash("Revisit scheduled (new upcoming appointment created).", "success")
    return redirect(url_for("patients"))


# -------------------------------------
# Debug route
# -------------------------------------
@app.route("/dbtest")
def dbtest():
    try:
        conn = get_db()
        conn.close()
        return "DB Connected ✔"
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(debug=True)
