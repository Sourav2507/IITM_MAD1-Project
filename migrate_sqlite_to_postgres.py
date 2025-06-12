from app import create_app
from extensions import db
from models import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --- Step 1: Setup source (SQLite) engine ---
sqlite_engine = create_engine('sqlite:///users.sqlite3')
SQLiteSession = sessionmaker(bind=sqlite_engine)
sqlite_session = SQLiteSession()

# --- Step 2: Setup destination (PostgreSQL) app ---
app = create_app()
with app.app_context():
    db.create_all()  # ensure PostgreSQL tables exist

    # --- Step 3: Copy records table by table ---
    for user in sqlite_session.query(Customer).all():
        db.session.add(Customer(**user.__dict__))

    for prof in sqlite_session.query(ServiceProfessional).all():
        db.session.add(ServiceProfessional(**prof.__dict__))

    for service in sqlite_session.query(Service).all():
        db.session.add(Service(**service.__dict__))

    for req in sqlite_session.query(ServiceRequest).all():
        db.session.add(ServiceRequest(**req.__dict__))

    for review in sqlite_session.query(ServiceReview).all():
        db.session.add(ServiceReview(**review.__dict__))

    for q in sqlite_session.query(UserQuery).all():
        db.session.add(UserQuery(**q.__dict__))

    db.session.commit()
    print("Data migrated successfully!")
