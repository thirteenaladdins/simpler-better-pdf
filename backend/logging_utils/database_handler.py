import logging
import psycopg2
import json

# Database connection details
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "xbTZzV3INnDtDC5B"
DATABASE_HOST = "db.dymrldumaipoatsslbyv.supabase.co"
DATABASE_PORT = "5432"
DATABASE_NAME = "postgres"

DATABASE_URL = f"postgres://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

class DatabaseLogHandler(logging.Handler):
    def emit(self, record):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO logs (log_level, json_data) VALUES (%s, %s)",
            (record.levelname, json.dumps(record.msg))
        )

        conn.commit()
        cur.close()
        conn.close()
    
    def update_access_log(self, record):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO logs (log_level, json_data) VALUES (%s, %s)",
            (record.levelname, json.dumps(record.msg))
        )

        conn.commit()
        cur.close()
        conn.close()
    
    def log_access(access_time, ip_address, user_agent, environment, user_token=None):
        with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
            with conn.cursor() as cur:
                # Insert into the table
                cur.execute(
                    "INSERT INTO access_logs (access_time, ip_address, user_agent, environment) VALUES (%s, %s, %s, %s)",
                    (access_time, ip_address, user_agent, environment)
                )
                conn.commit()

    



file_name = "your_filename_here"  # Adjust accordingly
logger = logging.getLogger(file_name)
logger.setLevel(logging.INFO)  # or your desired level
logger.addHandler(DatabaseLogHandler())
