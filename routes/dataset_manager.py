from flask import Blueprint, render_template, session, redirect, flash
from models import db
from models.crime import Crime

dataset_bp = Blueprint("dataset", __name__)


@dataset_bp.route("/dataset-manager")
def dataset_manager():

    if "admin" not in session:
        return redirect("/login")

    total_records = Crime.query.count()

    return render_template(
        "dashboard/dataset_manager.html",
        total_records=total_records
    )


@dataset_bp.route("/clear-records")
def clear_records():

    if "admin" not in session:
        return redirect("/login")

    deleted = Crime.query.delete()

    db.session.commit()

    flash(
        f"{deleted} crime records deleted successfully.",
        "success"
    )

    return redirect("/dataset-manager")