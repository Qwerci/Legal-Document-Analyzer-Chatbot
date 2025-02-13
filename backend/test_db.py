from database import engine
from sqlalchemy import text

print(" Checking Database Connection...")
print("Database URL:", engine.url)

with engine.connect() as conn:
    result = conn.execute(text("SELECT current_database();"))  # <== Fix
    print(" Connected to:", result.fetchone()[0])
