import sqlite3

def initialize_database(db_name="trips.db", schema_file="schema.sql"):
    try:
        # connect to the sqlite database
        connection = sqlite3.connect(db_name)

        connection.isolation_level = None

        cursor = connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        print(f"Connected to database: {db_name}")

        connection.isolation_level = ""

        # read the SQL commands from schema.sql
        with open(schema_file, "r") as f:
            sql_script = f.read()

        # execute
        cursor.executescript(sql_script)

        # save (commit) changes
        connection.commit()
        print("Database schema successfully created")

    except sqlite3.Error as error:
        print(f"An error occurred while setting up the database: {error}")

    finally:
        # always close connection when finished
        if connection:
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    initialize_database()