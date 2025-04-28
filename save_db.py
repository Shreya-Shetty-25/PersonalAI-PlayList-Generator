import sqlite3

def create_database():
    conn = sqlite3.connect("spotify_sessions.db")
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_data (
            spotify_id TEXT PRIMARY KEY,
            display_name TEXT,
            top_tracks TEXT,
            top_artists TEXT,
            top_genres TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Call this function when your app starts
create_database()
