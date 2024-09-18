import psycopg2

DB_CONFIG = "dbname=github_ranking user=mjomba password=1234 host=localhost"

def test_connection():
    try:
        conn = psycopg2.connect(DB_CONFIG)
        print("Successfully connected to the database!")
        conn.close()
    except Exception as e:
        print(f"Unable to connect to the database. Error: {e}")

if __name__ == "__main__":
    test_connection()