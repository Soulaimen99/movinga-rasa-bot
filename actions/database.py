# -*- coding: utf-8 -*-
import logging
import os
from typing import List, Optional, Tuple, Dict, Any

import pymysql.cursors
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)


class Database:
    """Service to use the database"""

    HOST = os.getenv("DB_HOST", "localhost")
    USER = os.getenv("DB_USER", "root")
    PASSWORD = os.getenv("DB_PASSWORD", "")
    DB = os.getenv("DB_NAME", "movingabot")

    def write_to_db(self, data: List) -> List:
        """
        Write booking data to the database

        Args:
            data: List containing booking information
                [0]: departure
                [1]: arrival
                [2]: date
                [3]: name
                [4]: volume
                [5]: phone
                [6]: email
                [7]: currentdatetime
                [8]: orderstatus

        Returns:
            Empty list for compatibility with Rasa actions
        """
        name = data[3]
        phone = data[5]
        departure = data[0]
        arrival = data[1]
        email = data[6]
        date = data[2]
        volume = data[4]
        currentdatetime = data[7]
        orderstatus = data[8]

        connection = None
        try:
            connection = pymysql.connect(
                host=self.HOST,
                user=self.USER,
                password=self.PASSWORD,
                db=self.DB,
                autocommit=True
            )

            with connection.cursor() as cursor:
                sql_insert = """
                    INSERT INTO booking 
                    (Name, Phone, Departure, Arrival, Email, Date, Volume, CurrentDateTime, OrderStatus) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(
                    sql_insert,
                    (name, phone, departure, arrival, email, date, volume, currentdatetime, orderstatus)
                )
                logger.info(f"Booking created for {name} ({phone})")

        except pymysql.Error as e:
            logger.error(f"Database error when writing booking: {e}")
        finally:
            if connection:
                connection.close()

        return []

    def update_db(self, data: List, update_type: str) -> List:
        """
        Update booking data in the database

        Args:
            data: List containing update information
                [0]: name
                [1]: phone
                [2]: changes (new value)
                [3]: currentdatetime
            update_type: Type of update to perform
                "time": Update booking date
                "volume": Update moving volume
                "requirement": Update requirements
                "cancel": Cancel booking

        Returns:
            Empty list for compatibility with Rasa actions
        """
        name = data[0]
        phone = data[1]
        changes = data[2]
        currentdatetime = data[3]

        # Convert list to string if needed
        if isinstance(changes, list):
            changes = ''.join(changes)

        connection = None
        try:
            connection = pymysql.connect(
                host=self.HOST,
                user=self.USER,
                password=self.PASSWORD,
                db=self.DB,
                autocommit=True
            )

            with connection.cursor() as cursor:
                if update_type == "time":
                    orderstatus = "modified"
                    sql_update = """
                        UPDATE booking 
                        SET Date=%s, CurrentDateTime=%s, OrderStatus=%s 
                        WHERE Name=%s AND Phone=%s
                    """
                    cursor.execute(sql_update, (changes, currentdatetime, orderstatus, name, phone))
                    logger.info(f"Updated booking time for {name} ({phone})")

                elif update_type == "volume":
                    sql_update = """
                        UPDATE booking 
                        SET Volume=%s, CurrentDateTime=%s 
                        WHERE Name=%s AND Phone=%s
                    """
                    cursor.execute(sql_update, (changes, currentdatetime, name, phone))
                    logger.info(f"Updated booking volume for {name} ({phone})")

                elif update_type == "requirement":
                    sql_update = """
                        UPDATE booking 
                        SET Requirement=%s, CurrentDateTime=%s 
                        WHERE Name=%s AND Phone=%s
                    """
                    cursor.execute(sql_update, (changes, currentdatetime, name, phone))
                    logger.info(f"Updated booking requirements for {name} ({phone})")

                elif update_type == "cancel":
                    sql_update = """
                        UPDATE booking 
                        SET OrderStatus=%s, CurrentDateTime=%s 
                        WHERE Name=%s AND Phone=%s
                    """
                    cursor.execute(sql_update, (changes, currentdatetime, name, phone))
                    logger.info(f"Cancelled booking for {name} ({phone})")

                else:
                    logger.warning(f"Unknown update type: {update_type}")

        except pymysql.Error as e:
            logger.error(f"Database error when updating booking: {e}")
        finally:
            if connection:
                connection.close()

        return []

    def exist_in_db(self, customer: List) -> bool:
        """
        Check if a customer exists in the database with an active booking

        Args:
            customer: List containing customer information
                [0]: name
                [1]: phone

        Returns:
            bool: True if customer exists with an active booking, False otherwise
        """
        name = customer[0]
        phone = customer[1]
        result = True

        connection = None
        try:
            connection = pymysql.connect(
                host=self.HOST,
                user=self.USER,
                password=self.PASSWORD,
                db=self.DB,
                autocommit=True
            )

            with connection.cursor() as cursor:
                sql = """
                    SELECT * FROM booking 
                    WHERE Name = %s AND Phone = %s
                """
                cursor.execute(sql, (name, phone))
                row_count = cursor.rowcount

                if row_count == 0:
                    logger.info(f"Customer not found: {name} ({phone})")
                    result = False
                    return result

                order = self.order_status(name, phone)
                if order == "cancelled":
                    logger.info(f"Customer found but booking is cancelled: {name} ({phone})")
                    result = False
                else:
                    logger.info(f"Customer found with active booking: {name} ({phone})")

        except pymysql.Error as e:
            logger.error(f"Database error when checking customer existence: {e}")
            result = False
        finally:
            if connection:
                connection.close()

        return result

    def order_status(self, name: str, phone: str) -> Optional[str]:
        """
        Get the order status for a customer

        Args:
            name: Customer name
            phone: Customer phone number

        Returns:
            str: Order status if found, None otherwise
        """
        order = None
        connection = None

        try:
            connection = pymysql.connect(
                host=self.HOST,
                user=self.USER,
                password=self.PASSWORD,
                db=self.DB,
                autocommit=True
            )

            with connection.cursor() as cursor:
                status_sql = """
                    SELECT OrderStatus FROM booking 
                    WHERE Name = %s AND Phone = %s
                """
                cursor.execute(status_sql, (name, phone))
                result = cursor.fetchone()

                if result:
                    order = result[0]
                    logger.info(f"Order status for {name} ({phone}): {order}")
                else:
                    logger.info(f"No order found for {name} ({phone})")

        except pymysql.Error as e:
            logger.error(f"Database error when getting order status: {e}")
        finally:
            if connection:
                connection.close()

        return order
