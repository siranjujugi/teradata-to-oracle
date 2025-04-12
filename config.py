from pathlib import Path

TERADATA_CONFIG = {
    "host": "your-teradata-host",
    "user": "your-teradata-username",
    "password_encrypted": b"gAAAAABlxxx...",  # Use encrypt_password() to generate this
    "database": "your-teradata-db"
}

ORACLE_CONFIG = {
    "dsn": "your-oracle-dsn",  # host:port/service_name
    "user": "your-oracle-username",
    "password_encrypted": b"gAAAAABlxxx...",  # Use encrypt_password() to generate this
    "target_table": "your_target_table"
}

CHUNK_SIZE = 10000
ENCRYPTION_KEY_PATH = Path("secret.key")
