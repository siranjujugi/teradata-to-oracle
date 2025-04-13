import teradata
import cx_Oracle
from concurrent.futures import ThreadPoolExecutor
from config import TERADATA_CONFIG, ORACLE_CONFIG, CHUNK_SIZE
from security import decrypt_password
from logger import get_logger

logger = get_logger()

def fetch_from_teradata(query: str):
    logger.info("Connecting to Teradata using UDAExec...")
    udaexec = teradata.UdaExec(appName="ETLApp", version="1.0", logConsole=False)
    with udaexec.connect(
        method="odbc",
        system=TERADATA_CONFIG["host"],
        username=TERADATA_CONFIG["user"],
        password=decrypt_password(TERADATA_CONFIG["password_encrypted"]),
        database=TERADATA_CONFIG["database"]
    ) as session:
        logger.info("Executing Teradata query...")
        cursor = session.execute(query)
        columns = [desc[0] for desc in cursor.description]
        while True:
            rows = cursor.fetchmany(CHUNK_SIZE)
            if not rows:
                break
            yield columns, rows

def truncate_oracle_table(conn, table_name):
    with conn.cursor() as cur:
        logger.info(f"Truncating Oracle table: {table_name}")
        cur.execute(f"TRUNCATE TABLE {table_name}")

def insert_batch(table_name, columns, rows):
    try:
        with cx_Oracle.connect(
            user=ORACLE_CONFIG["user"],
            password=decrypt_password(ORACLE_CONFIG["password_encrypted"]),
            dsn=ORACLE_CONFIG["dsn"]
        ) as conn:
            with conn.cursor() as cur:
                placeholders = ','.join([f':{i+1}' for i in range(len(columns))])
                sql = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"
                cur.executemany(sql, rows)
                conn.commit()
                logger.info(f"Inserted batch of {len(rows)} rows.")
    except Exception as e:
        logger.exception(f"Batch insert failed: {e}")

def load_to_oracle_parallel(columns_and_rows):
    logger.info("Connecting to Oracle for truncate...")
    with cx_Oracle.connect(
        user=ORACLE_CONFIG["user"],
        password=decrypt_password(ORACLE_CONFIG["password_encrypted"]),
        dsn=ORACLE_CONFIG["dsn"]
    ) as conn:
        truncate_oracle_table(conn, ORACLE_CONFIG["target_table"])

    logger.info("Starting parallel Oracle insert...")
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for columns, rows in columns_and_rows:
            futures.append(executor.submit(insert_batch, ORACLE_CONFIG["target_table"], columns, rows))
        for f in futures:
            f.result()