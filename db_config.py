import pymysql
from contextlib import contextmanager

DB_CONFIG = {
    'host': '10.200.15.15',
    'user': 'forprojects',
    'password': 'Den28062009db',
    'database': 'kafe_druze',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}


@contextmanager
def get_db_connection():
    connection = pymysql.connect(**DB_CONFIG)
    try:
        yield connection
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()


def init_database():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bookings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    first_name VARCHAR(100) NOT NULL,
                    last_name VARCHAR(100) NOT NULL,
                    phone VARCHAR(20) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    guests INT NOT NULL,
                    booking_date DATE NOT NULL,
                    booking_time TIME NOT NULL,
                    comment TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_booking_date (booking_date),
                    INDEX idx_email (email)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
        connection.commit()
    print("Database initialized successfully!")


def save_booking(booking_data):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO bookings 
                (first_name, last_name, phone, email, guests, booking_date, booking_time, comment)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                booking_data['first_name'],
                booking_data['last_name'],
                booking_data['phone'],
                booking_data['email'],
                booking_data['guests'],
                booking_data['date'],
                booking_data['time'],
                booking_data.get('comment', '')
            ))
        connection.commit()
        return cursor.lastrowid


def get_all_bookings():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM bookings 
                ORDER BY booking_date DESC, booking_time DESC
            """)
            return cursor.fetchall()


def get_booking_by_id(booking_id):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM bookings WHERE id = %s", (booking_id,))
            return cursor.fetchone()


def delete_booking(booking_id):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
        connection.commit()
        return cursor.rowcount > 0
