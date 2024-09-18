# data_storage.py

import psycopg2
from psycopg2.extras import execute_batch


DB_CONFIG = "dbname=github_ranking user=mjomba password=1234 host=localhost"


def create_tables():
    conn = psycopg2.connect(DB_CONFIG)
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS repositories (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        stars INTEGER NOT NULL,
        language TEXT,
        last_updated TIMESTAMP
    )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS repo_categories (
        repo_id INTEGER REFERENCES repositories(id),
        category_id INTEGER REFERENCES categories(id),
        PRIMARY KEY (repo_id, category_id)
    )
    """)
    
    conn.commit()
    cur.close()
    conn.close()

def insert_repos(repos):
    conn = psycopg2.connect(DB_CONFIG)
    cur = conn.cursor()
    
    insert_query = """
    INSERT INTO repositories (name, description, stars, language, last_updated)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (name) DO UPDATE SET
    stars = EXCLUDED.stars,
    last_updated = EXCLUDED.last_updated
    """
    
    repo_data = [
        (
            repo["name"],
            repo["description"],
            repo["stargazerCount"],
            repo["primaryLanguage"]["name"] if repo["primaryLanguage"] else None,
            repo["updatedAt"]
        )
        for repo in repos
    ]
    
    execute_batch(cur, insert_query, repo_data)
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully")