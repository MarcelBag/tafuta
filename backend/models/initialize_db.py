from database import Base, engine
import os

db_path = os.path.abspath("tafuta.db")
print(f"SQLAlchemy is targeting database at: {db_path}")

print("Forcing table creation...")
Base.metadata.create_all(bind=engine)
print("Tables created!")
