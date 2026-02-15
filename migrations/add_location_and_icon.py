import sqlite3

def upgrade():
    conn = sqlite3.connect('part3/hbnb_dev.db')
    cursor = conn.cursor()
    
    # Check and add 'location' to 'places'
    try:
        cursor.execute("SELECT location FROM places LIMIT 1")
    except sqlite3.OperationalError:
        print("Adding 'location' column to 'places' table...")
        cursor.execute("ALTER TABLE places ADD COLUMN location TEXT")
        
    # Check and add 'icon' to 'amenities'
    try:
        cursor.execute("SELECT icon FROM amenities LIMIT 1")
    except sqlite3.OperationalError:
        print("Adding 'icon' column to 'amenities' table...")
        cursor.execute("ALTER TABLE amenities ADD COLUMN icon TEXT")

    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    upgrade()
