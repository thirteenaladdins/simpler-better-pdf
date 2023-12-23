import psycopg2

# Database connection details
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "xbTZzV3INnDtDC5B"
DATABASE_HOST = "db.dymrldumaipoatsslbyv.supabase.co"
DATABASE_PORT = "5432"
DATABASE_NAME = "postgres"

DATABASE_URL = f"postgres://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# Connect to the database
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

# SQL to create the 'access_logs' table with the 'environment' column
create_table_sql = """
CREATE TABLE IF NOT EXISTS access_logs (
    id SERIAL PRIMARY KEY,
    access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(50),
    user_agent TEXT,
    environment VARCHAR(10) CHECK (environment IN ('dev', 'test', 'prod'))
);
"""

cur.execute(create_table_sql)

# Commit changes and close connection
conn.commit()
cur.close()
conn.close()
