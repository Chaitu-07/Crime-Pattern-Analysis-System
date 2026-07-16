from sqlalchemy import or_
from flask import Blueprint, render_template, session, redirect
from sqlalchemy import func

from models.crime import Crime
from models.activity import Activity

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect("/login")

    # ===========================
    # Dashboard Statistics
    # ===========================

    total = Crime.query.count()

    districts = Crime.query.with_entities(
        Crime.district
    ).distinct().count()

    stations = Crime.query.with_entities(
        Crime.police_station
    ).distinct().count()

    solved = Crime.query.filter(
    or_(

        Crime.status.ilike("%Solved%"),

        Crime.status.ilike("%Closed%"),

        Crime.status.ilike("%Resolved%")
    )
    ).count()

    unsolved = Crime.query.filter(

    or_(

        Crime.status.ilike("%Unsolved%"),

        Crime.status.ilike("%Pending%"),

        Crime.status.ilike("%Under Investigation%"),

        Crime.status.ilike("%Open%")

    )

).count()

    arrested = Crime.query.filter_by(
        arrest_made="Yes"
    ).count()

    high_severity = Crime.query.filter_by(
        severity="High"
    ).count()

    # ===========================
    # Charts
    # ===========================

    top_crimes = (
        Crime.query.with_entities(
            Crime.crime_type,
            func.count(Crime.id)
        )
        .group_by(Crime.crime_type)
        .order_by(func.count(Crime.id).desc())
        .limit(5)
        .all()
    )

    top_districts = (
        Crime.query.with_entities(
            Crime.district,
            func.count(Crime.id)
        )
        .group_by(Crime.district)
        .order_by(func.count(Crime.id).desc())
        .limit(5)
        .all()
    )

    # ===========================
    # Recent Activity
    # ===========================

    activities = Activity.query.order_by(
        Activity.created_at.desc()
    ).limit(5).all()

    # ===========================
    # AI Quick Insights
    # ===========================

    highest_crime = top_crimes[0][0] if top_crimes else "N/A"

    highest_district = (
        top_districts[0][0]
        if top_districts else "N/A"
    )

    solved_rate = round(
        (solved / total) * 100,
        1
    ) if total else 0

    peak_month = (
        Crime.query.with_entities(
            Crime.month,
            func.count(Crime.id)
        )
        .group_by(Crime.month)
        .order_by(func.count(Crime.id).desc())
        .first()
    )

    peak_month = peak_month[0] if peak_month else "N/A"

    recommendation = (
        f"Increase police patrols in "
        f"{highest_district} due to "
        f"high {highest_crime} activity."
    )

    return render_template(

        "dashboard/dashboard.html",

        total=total,

        districts=districts,

        stations=stations,

        solved=solved,

        unsolved=unsolved,

        arrested=arrested,

        high_severity=high_severity,

        top_crimes=top_crimes,

        top_districts=top_districts,

        activities=activities,

        highest_crime=highest_crime,

        highest_district=highest_district,

        solved_rate=solved_rate,

        peak_month=peak_month,

        recommendation=recommendation

    )