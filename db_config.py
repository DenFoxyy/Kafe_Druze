import pymysql

DB_CONFIG = {
    'host': '10.200.15.15',
    'user': 'forprojects',
    'password': 'Den28062009db',
    'database': 'kafe_druze',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}


def get_db_connection():
    return pymysql.connect(**DB_CONFIG)


def init_database():
    connection = get_db_connection()
    cursor = connection.cursor()
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
    cursor.close()
    connection.close()
    print("Database initialized successfully!")


def save_booking(booking_data):
    connection = get_db_connection()
    cursor = connection.cursor()
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
    new_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return new_id


def get_all_bookings():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT * FROM bookings 
        ORDER BY booking_date DESC, booking_time DESC
    """)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results


def get_booking_by_id(booking_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM bookings WHERE id = %s", (booking_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result


def delete_booking(booking_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
    connection.commit()
    affected = cursor.rowcount
    cursor.close()
    connection.close()
    return affected > 0
