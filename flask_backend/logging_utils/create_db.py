import psycopg2


# TODO: move to .env
# Database connection details
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "xbTZzV3INnDtDC5B"
DATABASE_HOST = "db.dymrldumaipoatsslbyv.supabase.co"
DATABASE_PORT = "5432"
DATABASE_NAME = "postgres"

# DATABASE_URL = f"postgres://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

def create_table():
    # Set up database connection
    conn = psycopg2.connect(
        dbname=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT
    )
    
    # Create a new cursor
    cur = conn.cursor()

    # Write the SQL query to create a table
    create_table_query = """
    CREATE TABLE logs (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        log_level VARCHAR(10) NOT NULL,
        json_data JSONB NOT NULL
    );
    """

    # Execute the query
    cur.execute(create_table_query)

    # Commit the changes
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_table()
