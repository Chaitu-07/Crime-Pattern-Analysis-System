from models.activity import Activity
from models import db

import os

from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    request,
    flash,
    current_app
)

from werkzeug.utils import secure_filename
from sqlalchemy import or_, String

from models.crime import Crime
from services.csv_service import import_csv

upload_bp = Blueprint("upload", __name__)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


@upload_bp.route("/upload", methods=["GET", "POST"])
def upload():

    if "admin" not in session:
        return redirect("/login")

    # ===========================
    # Upload CSV
    # ===========================

    if request.method == "POST":

        if "file" not in request.files:
            flash("No file selected.", "danger")
            return redirect("/upload")

        file = request.files["file"]

        if file.filename == "":
            flash("Please choose a CSV file.", "warning")
            return redirect("/upload")

        if not allowed_file(file.filename):
            flash("Only CSV files are allowed.", "danger")
            return redirect("/upload")

        filename = secure_filename(file.filename)

        filepath = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            filename
        )

        file.save(filepath)

        try:

            imported, skipped = import_csv(filepath)

            db.session.add(

            Activity(

                action=f"Uploaded dataset ({imported} records)"

            )

        )

            db.session.commit()

            flash(
                f"Dataset uploaded successfully. "
                f"{imported} records imported, "
                f"{skipped} duplicate records skipped.",
                "success"
            )

        except Exception as e:

            flash(f"Import failed: {str(e)}", "danger")

        return redirect("/upload")

    # ===========================
    # Display Crime Records
    # ===========================

    page = request.args.get("page", 1, type=int)

    search = request.args.get("search", "").strip()

    query = Crime.query

    if search:

        query = query.filter(

            or_(

                Crime.crime_type.ilike(f"%{search}%"),

                Crime.district.ilike(f"%{search}%"),

                Crime.police_station.ilike(f"%{search}%"),

                Crime.crime_id.cast(String).ilike(f"%{search}%")

            )

        )

    crimes = query.order_by(

        Crime.crime_id.asc()

    ).paginate(

        page=page,

        per_page=20,

        error_out=False

    )

    return render_template(

        "dashboard/upload.html",

        crimes=crimes,

        search=search

    )