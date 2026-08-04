import sqlite3

def seed_database(db_name="trips.db", seed_file="seed_data.sql"):
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        # Turn on foreign keys
        cursor.execute("PRAGMA foreign_keys = ON;")

        with open(seed_file, "r") as f:
            sql_script = f.read()

        cursor.executescript(sql_script)
        connection.commit()
        print("Database successfully seeded with mock data!")

    except sqlite3.Error as error:
        print(f"An error occurred while seeding the database: {error}")

    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    seed_database()