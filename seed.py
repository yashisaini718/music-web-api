from app import create_app
from app.extensions import db
from app.utils.hardcode_db import seed_songs

app = create_app()

with app.app_context():
    seed_songs()