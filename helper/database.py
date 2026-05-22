import mysql.connector
import hashlib
import os

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "enter yours",
    "database": "resume_analyze"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# ==================================================
# PASSWORD HASHING
# ==================================================

def hash_password(password):
    password = password.strip()
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()

# ==================================================
# SETUP DATABASE
# ==================================================

def setup_database():
    connection = None
    cursor = None
    try:
        # ----------------------------------------------
        # CONNECT WITHOUT DATABASE
        # ----------------------------------------------
        connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
        cursor = connection.cursor()
        # ----------------------------------------------
        # CREATE DATABASE
        # ----------------------------------------------

        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS resume_analyze"
        )
        cursor.execute(
            "USE resume_analyze"
        )
        # ----------------------------------------------
        # USERS TABLE
        # ----------------------------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP )
        """)

        # ----------------------------------------------
        # HISTORY TABLE
        # ----------------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                filename VARCHAR(255),
                predicted_category VARCHAR(150),
                confidence_score FLOAT,
                missing_skills TEXT,
                analyzed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE  )
        """)
        connection.commit()
        return True
    except Exception as error:
        print("Database Setup Error:", error)
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# ==================================================
# REGISTER USER
# ==================================================

def register_user(username, password):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO users (username, password )
            VALUES (%s, %s)
        """
        values = (
            username.strip().lower(),
            hash_password(password)
        )
        cursor.execute(query, values)
        connection.commit()
        return True, "Registration successful"
    except mysql.connector.errors.IntegrityError:
        return False, "Username already exists"
    except Exception as error:
        return False, str(error)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# ==================================================
# LOGIN USER
# ==================================================

def login_user(username, password):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(
            dictionary=True
        )
        query = """
            SELECT * FROM users
            WHERE username = %s
            AND password = %s
        """
        values = (
            username.strip().lower(),
            hash_password(password)
        )
        cursor.execute(query, values)
        user = cursor.fetchone()
        return user
    except Exception as error:
        print("Login Error:", error)
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# ==================================================
# SAVE HISTORY
# ==================================================

def save_to_history(
    user_id,
    filename,
    category,
    score,
    missing_skills
):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO history (
                user_id,
                filename,
                predicted_category,
                confidence_score,
                missing_skills
            )
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            user_id,
            filename,
            category,
            round(float(score), 2), ", ".join(missing_skills)
            if missing_skills
            else "None"
        )
        cursor.execute(query, values)
        connection.commit()
        return True
    except Exception as error:
        print("Save Error:", error)
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# ==================================================
# FETCH HISTORY
# ==================================================

def fetch_history(user_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(
            dictionary=True
        )
        query = """
            SELECT * FROM history
            WHERE user_id = %s
            ORDER BY analyzed_at DESC
        """
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
        return rows
    except Exception as error:
        print("Fetch Error:", error)
        return []
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
