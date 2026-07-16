import json
from flask import Blueprint, render_template, session, redirect
from sqlalchemy import func

from models.crime import Crime

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/analytics")
def analytics():

    if "admin" not in session:
        return redirect("/login")

    crime_types = (
        Crime.query.with_entities(
            Crime.crime_type,
            func.count(Crime.id)
        )
        .group_by(Crime.crime_type)
        .order_by(func.count(Crime.id).desc())
        .all()
    )

    status = (
        Crime.query.with_entities(
            Crime.status,
            func.count(Crime.id)
        )
        .group_by(Crime.status)
        .all()
    )

    months = (
        Crime.query.with_entities(
            Crime.month,
            func.count(Crime.id)
        )
        .group_by(Crime.month)
        .all()
    )

    districts = (
        Crime.query.with_entities(
            Crime.district,
            func.count(Crime.id)
        )
        .group_by(Crime.district)
        .order_by(func.count(Crime.id).desc())
        .limit(10)
        .all()
    )

    crime_locations = Crime.query.with_entities(

    Crime.latitude,

    Crime.longitude,

    Crime.crime_type,

    Crime.district,

    Crime.status

    ).all()

    locations = [

    {

        "lat": c.latitude,

        "lng": c.longitude,

        "crime": c.crime_type,

        "district": c.district,

        "status": c.status

    }

    for c in crime_locations

    if c.latitude and c.longitude

   ]

    return render_template(
        "dashboard/analytics.html",

        crime_labels=[x[0] for x in crime_types],
        crime_values=[x[1] for x in crime_types],

        status_labels=[x[0] for x in status],
        status_values=[x[1] for x in status],

        month_labels=[x[0] for x in months],
        month_values=[x[1] for x in months],

        district_labels=[x[0] for x in districts],
        district_values=[x[1] for x in districts],
        locations=json.dumps(locations),
    )