import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Determine environment (default to development if not set)
ENV = os.getenv("ENV", "development")

if ENV in ["development", "test"]:
    # Use SQLite in development or test environments
    DATABASE_DIR = os.path.dirname(os.path.abspath(__file__))

    DATABASE_PATH = os.path.join('/tmp', "documents.db")
    DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


else:
    # In production, use the Heroku/PostgreSQL DATABASE_URL environment variable
    DATABASE_URL = os.environ["DATABASE_URL"]

# Create the engine. For SQLite, add specific connection arguments.
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={
                           "check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI routes


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
