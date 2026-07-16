from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    request
)

from sqlalchemy import or_

from models import db
from models.crime import Crime

crime_bp = Blueprint("crime", __name__)


@crime_bp.route("/crimes")
def crimes():

    if "admin" not in session:
        return redirect("/login")

    page = request.args.get("page", 1, type=int)

    search = request.args.get("search", "").strip()

    query = Crime.query

    if search:

        query = query.filter(

            or_(

                Crime.crime_type.ilike(f"%{search}%"),

                Crime.district.ilike(f"%{search}%"),

                Crime.police_station.ilike(f"%{search}%"),

                Crime.crime_id.cast(db.String).ilike(f"%{search}%")

            )

        )

    crimes = query.order_by(
        Crime.crime_id
    ).paginate(
        page=page,
        per_page=20
    )

    return render_template(
        "dashboard/crimes.html",
        crimes=crimes,
        search=search
    )


@crime_bp.route("/crime/<int:id>")
def crime_details(id):

    if "admin" not in session:
        return redirect("/login")

    crime = Crime.query.get_or_404(id)

    return render_template(
        "dashboard/crime_details.html",
        crime=crime
    )


@crime_bp.route("/crime/delete/<int:id>")
def delete_crime(id):

    if "admin" not in session:
        return redirect("/login")

    crime = Crime.query.get_or_404(id)

    db.session.delete(crime)

    db.session.commit()

    return redirect("/crimes")