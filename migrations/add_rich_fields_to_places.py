import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../part3/hbnb_dev.db')

def migrate():
    print(f"Connecting to database at {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    columns_to_add = [
        ("number_of_rooms", "INTEGER DEFAULT 0"),
        ("max_guests", "INTEGER DEFAULT 0"),
        ("tagline", "VARCHAR(255)"),
        ("rules", "TEXT"),
        ("details", "TEXT"), # For 'about' sections in JSON
        ("rooms", "TEXT DEFAULT '[]'"), # For room list in JSON
    ]

    print("Checking existing columns...")
    cursor.execute("PRAGMA table_info(places)")
    existing_columns = [row[1] for row in cursor.fetchall()]

    for col_name, col_type in columns_to_add:
        if col_name not in existing_columns:
            print(f"Adding column '{col_name}'...")
            try:
                cursor.execute(f"ALTER TABLE places ADD COLUMN {col_name} {col_type}")
                print(f"✅ Added {col_name}")
            except sqlite3.OperationalError as e:
                print(f"❌ Failed to add {col_name}: {e}")
        else:
            print(f"ℹ️ Column '{col_name}' already exists.")

    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
