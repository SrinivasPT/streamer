"""
Database operations for scan records
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime
from db_config import DB_CONFIG


class ScanDB:
    def __init__(self):
        """Initialize database connection"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor(dictionary=True)
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            self.connection = None
            self.cursor = None

    def __del__(self):
        """Close database connection when object is destroyed"""
        if self.connection and self.connection.is_connected():
            if self.cursor:
                self.cursor.close()
            self.connection.close()

    def connect(self):
        """Connect to database if not already connected"""
        if not self.connection or not self.connection.is_connected():
            try:
                self.connection = mysql.connector.connect(**DB_CONFIG)
                self.cursor = self.connection.cursor(dictionary=True)
                return True
            except Error as e:
                print(f"Error reconnecting to MySQL database: {e}")
                return False
        return True

    def insert_scan(
        self,
        patient_id,
        consent_given=False,
        image_path=None,
        referring_physician_id=None,
        scan_result=None,
    ):
        """
        Insert a new scan record into the database

        Args:
            patient_id (str): Patient ID (must exist in patient table)
            scan_datetime (datetime, optional): Time of scan. Defaults to current time.
            consent_given (bool, optional): If consent was given. Defaults to False.
            image_path (str, optional): Path to scan image. Defaults to None.
            referring_physician_id (int, optional): ID of referring physician. Defaults to None.
            scan_result (str, optional): Result of the scan. Defaults to None.

        Returns:
            int: ID of the inserted record or None if insertion failed
        """
        if not self.connect():
            return None

        try:
            scan_datetime = datetime.now()

            query = """
            INSERT INTO scan 
            (patient_id, scan_datetime, consent_given, image_path, referring_physician_id, scan_result) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            self.cursor.execute(
                query,
                (
                    patient_id,
                    scan_datetime,
                    consent_given,
                    image_path,
                    referring_physician_id,
                    scan_result,
                ),
            )

            self.connection.commit()
            return self.cursor.lastrowid

        except Error as e:
            print(f"Error inserting scan record: {e}")
            return None
