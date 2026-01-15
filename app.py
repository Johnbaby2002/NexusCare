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
    # --- DB: totals, recent patients, and REAL appointments for today ---
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

    # REAL upcoming appointments for TODAY (only not visited)
    today = date.today().isoformat()
    cur.execute(
        """
        SELECT patientid, name, symptoms, visit_time
        FROM patients
        WHERE doctorid = %s
          AND visit_date = %s
          AND visited = 0
        ORDER BY visit_time IS NULL, visit_time ASC, patientid ASC
        """,
        (session["doctor_id"], today)
    )
    appointments = cur.fetchall() or []

    cur.close()
    conn.close()

    # Basic alerts (optional: keep simple)
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
        appointments=appointments,
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
    conn = get_db()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        "SELECT * FROM patients WHERE doctorid=%s ORDER BY patientid DESC",
        (session["doctor_id"],)
    )
    all_patients = cur.fetchall() or []

    cur.close()
    conn.close()

    today = date.today()
    upcoming = []
    visited = []

    for p in all_patients:
        vd = p.get("visit_date")
        is_visited = int(p.get("visited") or 0)

        vd_date = None
        if vd:
            try:
                vd_date = vd if hasattr(vd, "year") else date.fromisoformat(str(vd)[:10])
            except Exception:
                vd_date = None

        if is_visited == 1:
            visited.append(p)
        else:
            if vd_date and vd_date < today:
                visited.append(p)
            else:
                upcoming.append(p)

    return render_template("patients.html", upcoming=upcoming, visited=visited)


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
        if "smoker" in patient_cols:
            cols.append("smoker"); vals.append(smoker)
        if "symptoms" in patient_cols:
            cols.append("symptoms"); vals.append(symptoms)
        if "visited" in patient_cols:
            cols.append("visited"); vals.append(0)

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
            set_parts.append("visit_time=%s")
            vals.append(visit_time if visit_time else None)

        if "smoker" in patient_cols:
            set_parts.append("smoker=%s"); vals.append(smoker)
        if "symptoms" in patient_cols:
            set_parts.append("symptoms=%s"); vals.append(symptoms)
        if "visited" in patient_cols:
            set_parts.append("visited=%s"); vals.append(visited_flag)

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
