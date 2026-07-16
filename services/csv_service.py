import pandas as pd

from models import db
from models.crime import Crime


def clean(value):

    if pd.isna(value):
        return None

    return value


def import_csv(filepath):

    df = pd.read_csv(filepath)

    imported = 0

    skipped = 0

    existing_ids = set(

        crime_id[0]

        for crime_id in db.session.query(Crime.crime_id).all()

    )

    crimes = []

    for row in df.itertuples(index=False):

        crime_id = int(row.crime_id)

        if crime_id in existing_ids:

            skipped += 1

            continue

        crimes.append(

            Crime(

    crime_id=crime_id,

    crime_type=clean(row.crime_type),

    category=clean(row.category),

    crime_date=str(clean(row.crime_date)),

    crime_time=str(clean(row.crime_time)),

    day=clean(row.day),

    month=clean(row.month),

    year=int(row.year),

    district=clean(row.district),

    police_station=clean(row.police_station),

    latitude=float(row.latitude),

    longitude=float(row.longitude),

    victim_age=int(row.victim_age),

    victim_gender=clean(row.victim_gender),

    suspect_age=int(row.suspect_age),

    suspect_gender=clean(row.suspect_gender),

    weapon_used=clean(row.weapon_used),

    severity=clean(row.severity),

    status=clean(row.status),

    arrest_made=clean(row.arrest_made),

    case_closed=clean(row.case_closed),

    description=clean(row.description)

)

        )

        imported += 1

    if crimes:

        db.session.bulk_save_objects(crimes)

        db.session.commit()

    return imported, skipped