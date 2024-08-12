import sqlite3
import os

def create_users_table():
    """Create the users table if it doesn't already exist."""
    db_path = os.path.join('data', 'users.db')  # Update this path if necessary

    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

def create_predictions_table():
    """Create the predictions table if it doesn't already exist."""
    db_path = os.path.join('data', 'predictions.db')  # Update this path if necessary

    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                area REAL NOT NULL,
                bedrooms INTEGER NOT NULL,
                bathrooms INTEGER NOT NULL,
                stories INTEGER NOT NULL,
                mainroad INTEGER NOT NULL,
                guestroom INTEGER NOT NULL,
                basement INTEGER NOT NULL,
                hotwaterheating INTEGER NOT NULL,
                airconditioning INTEGER NOT NULL,
                parking REAL NOT NULL,
                prefarea INTEGER NOT NULL,
                furnishingstatus TEXT NOT NULL,
                predicted_price REAL NOT NULL
            )
        ''')
        conn.commit()

if __name__ == '__main__':
    create_users_table()
    create_predictions_table()
    print("Database tables created successfully.")
