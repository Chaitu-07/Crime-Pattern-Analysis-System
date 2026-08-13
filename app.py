import os
from routes.dataset_manager import dataset_bp
from flask import Flask

from config import Config

from models import db

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.upload import upload_bp
from routes.crimes import crime_bp
from routes.analytics import analytics_bp

from models.admin import Admin


app = Flask(__name__)

app.config.from_object(Config)
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

db.init_app(app)


app.register_blueprint(auth_bp)

app.register_blueprint(dashboard_bp)

app.register_blueprint(upload_bp)

app.register_blueprint(crime_bp)

app.register_blueprint(analytics_bp)

app.register_blueprint(dataset_bp)


with app.app_context():

    db.create_all()

    admin_username = os.getenv("ADMIN_USERNAME", "admin")
admin_password = os.getenv("ADMIN_PASSWORD")

if (
    admin_password
    and not Admin.query.filter_by(
        username=admin_username
    ).first()
):
    admin = Admin(
        username=admin_username
    )

    admin.set_password(
        admin_password
    )

    db.session.add(admin)
    db.session.commit()


if __name__ == "__main__":

    app.run(debug=True)
