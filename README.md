# Teradata to Oracle ETL (Secure & Scalable)

This Python 3.12.9 project performs a secure, high-performance ETL process:
- 🔄 Extracts 1M+ rows from Teradata
- 🧹 Truncates and loads into Oracle
- 🔐 Uses encryption for password security
- ⚡ Optimized with parallel inserts and batch processing
- 📜 Logs all operations

## 🔧 Requirements

- Python 3.12.9
- Teradata native drivers or ODBC
- Oracle Instant Client (`cx_Oracle`)
- Virtualenv (optional)

## 📦 Installation

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🔐 Secure Your Passwords

### 1. Generate a Key (once)

```bash
python -c "from security import generate_key; generate_key()"
```

### 2. Encrypt Your Password

```bash
python -c "from security import encrypt_password; print(encrypt_password('YourPassword123'))"
```

Paste the encrypted value into `config.py`.

## ▶️ Run the ETL Script

```bash
python main.py
```

## ⚙️ Configuration

- `CHUNK_SIZE`: Controls batch size (default: 10,000)
- `max_workers`: Adjust threads for parallelism (default: 4)

## 📢 Note

Never commit `secret.key` to Git. Use secure storage in production.
