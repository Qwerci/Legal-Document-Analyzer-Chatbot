from sqlalchemy import text
from database import engine, Base


print(" Attempting to create tables...")

try:
    with engine.connect() as conn:
        print(" Connected to:", conn.execute(text("SELECT current_database();")).fetchone()[0])

    Base.metadata.create_all(bind=engine)
    print(" Tables created successfully!")
except Exception as e:
    print("Error creating tables:", e)
