from etl import fetch_from_teradata, load_to_oracle_parallel
from logger import get_logger

logger = get_logger()
QUERY = "SELECT * FROM your_table SAMPLE 1000000"

def main():
    try:
        logger.info("ETL job started.")
        data = fetch_from_teradata(QUERY)
        load_to_oracle_parallel(data)
        logger.info("ETL job completed successfully.")
    except Exception as e:
        logger.exception(f"ETL failed: {e}")

if __name__ == "__main__":
    main()
