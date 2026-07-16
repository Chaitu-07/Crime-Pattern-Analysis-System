from models import db


class Crime(db.Model):

    __tablename__ = "crimes"

    id = db.Column(db.Integer, primary_key=True)

    crime_id = db.Column(db.Integer, unique=True)

    crime_type = db.Column(db.String(100))

    category = db.Column(db.String(100))

    crime_date = db.Column(db.String(30))

    crime_time = db.Column(db.String(30))

    day = db.Column(db.String(20))

    month = db.Column(db.String(20))

    year = db.Column(db.Integer)

    district = db.Column(db.String(100))

    police_station = db.Column(db.String(150))

    latitude = db.Column(db.Float)

    longitude = db.Column(db.Float)

    victim_age = db.Column(db.Integer)

    victim_gender = db.Column(db.String(20))

    suspect_age = db.Column(db.Integer)

    suspect_gender = db.Column(db.String(20))

    weapon_used = db.Column(db.String(100))

    severity = db.Column(db.String(50))

    status = db.Column(db.String(50))

    arrest_made = db.Column(db.String(10))

    case_closed = db.Column(db.String(10))

    description = db.Column(db.Text)