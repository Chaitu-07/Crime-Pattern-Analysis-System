from models.activity import Activity
from models import db
from flask import Blueprint, render_template, request, redirect, session
from sqlalchemy import func

from models.admin import Admin
from models.crime import Crime

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def home():

    # Total Crimes
    total = Crime.query.count()

    # Total Districts
    districts = db.session.query(
        func.count(func.distinct(Crime.district))
    ).scalar() or 0

    # Total Police Stations
    stations = db.session.query(
        func.count(func.distinct(Crime.police_station))
    ).scalar() or 0

    # Solved Cases
    solved_cases = Crime.query.filter(
        Crime.status.ilike("%closed%")
    ).count()

    solved = round((solved_cases / total) * 100, 1) if total > 0 else 0

    return render_template(
        "index.html",
        total=total,
        districts=districts,
        stations=stations,
        solved=solved
    )


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        admin = Admin.query.filter_by(
            username=username
        ).first()

        if admin and admin.verify_password(password):

            session["admin"] = admin.username

            db.session.add(

                Activity(

                    action="Administrator logged in"

                )

            )

            db.session.commit()

        return redirect("/dashboard")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/")