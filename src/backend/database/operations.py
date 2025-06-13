import mysql.connector
from mysql.connector import Error
from .models import ApplicantProfile, ApplicationDetail
from .connection import get_db_connection
from datetime import datetime, date
from typing import Optional, List

class DatabaseOperations:
    @staticmethod
    def create_applicant(first_name: str, last_name: str, date_of_birth: Optional[date] = None, address: Optional[str] = None, phone_number: Optional[str] = None) -> Optional[int]:
        connection = get_db_connection()
        if not connection:
            return None
            
        try:
            cursor = connection.cursor()
            insert_query = """
                INSERT INTO ApplicantProfile (first_name, last_name, date_of_birth, address, phone_number)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (first_name, last_name, date_of_birth, address, phone_number))
            connection.commit()
            applicant_id = cursor.lastrowid
            return applicant_id
        except Error as e:
            connection.rollback()
            print(f"Error creating applicant: {e}")
            return None
        finally:
            cursor.close()
    
    @staticmethod
    def create_application(applicant_id: int, application_role: str, cv_path: str) -> Optional[int]:
        connection = get_db_connection()
        if not connection:
            return None
            
        try:
            cursor = connection.cursor()
            
            insert_query = """
                INSERT INTO ApplicationDetail (applicant_id, application_role, cv_path)
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (applicant_id, application_role, cv_path))
            connection.commit()
            application_id = cursor.lastrowid # ambil ID untuk application yang baru dibuat
            return application_id
        except Error as e:
            connection.rollback()
            print(f"Error creating application: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_all_applications() -> List[ApplicationDetail]:
        connection = get_db_connection()
        if not connection:
            return []
            
        try:
            cursor = connection.cursor()
            query = """
                SELECT detail_id, applicant_id, application_role, cv_path
                FROM ApplicationDetail
                ORDER BY detail_id DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            
            applications = []
            for row in rows:
                app = ApplicationDetail.from_row(tuple(row))
                applications.append(app)
            
            return applications
        except Error as e:
            print(f"Error getting applications: {e}")
            return []
        finally:
            cursor.close()
    
    @staticmethod
    def get_application_by_id(application_id: int) -> Optional[ApplicationDetail]:
        connection = get_db_connection()
        if not connection:
            return None
            
        try:
            cursor = connection.cursor()
            query = """
                SELECT detail_id, applicant_id, application_role, cv_path
                FROM ApplicationDetail
                WHERE detail_id = %s
            """
            cursor.execute(query, (application_id,))
            row = cursor.fetchone()
            if row:
                return ApplicationDetail.from_row(tuple(row))
            return None
        except Error as e:
            print(f"Error getting application: {e}")
            return None
        finally:
            cursor.close()
    
    @staticmethod
    def get_applicant_by_id(applicant_id: int) -> Optional[ApplicantProfile]:
        connection = get_db_connection()
        if not connection:
            return None
            
        try:
            cursor = connection.cursor()
            query = """
                SELECT applicant_id, first_name, last_name, date_of_birth, address, phone_number
                FROM ApplicantProfile
                WHERE applicant_id = %s
            """
            cursor.execute(query, (applicant_id,))
            row = cursor.fetchone()
            if row:
                return ApplicantProfile.from_row(tuple(row))
            return None
        except Error as e:
            print(f"Error getting applicant: {e}")
            return None
        finally:
            cursor.close()
    
    @staticmethod
    def delete_application(application_id: int) -> bool:
        connection = get_db_connection()
        if not connection:
            return False
    
        try:
            cursor = connection.cursor()
            delete_query = "DELETE FROM ApplicationDetail WHERE detail_id = %s"
            cursor.execute(delete_query, (application_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            connection.rollback()
            print(f"Error deleting application: {e}")
            return False
        finally:
            cursor.close()
    
    @staticmethod
    def delete_applicant(applicant_id: int) -> bool:
        """ Delete applicant and all related applications (CASCADE) """
        connection = get_db_connection()
        if not connection:
            return False
            
        try:
            cursor = connection.cursor()
            delete_query = "DELETE FROM ApplicantProfile WHERE applicant_id = %s"
            cursor.execute(delete_query, (applicant_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            connection.rollback()
            print(f"Error deleting applicant: {e}")
            return False
        finally:
            cursor.close()

    @staticmethod
    def clear_all_data() -> bool:
        """ Clear all data from database """
        connection = get_db_connection()
        if not connection:
            return False
            
        try:
            cursor = connection.cursor()
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            
            # hapus semua data dari tabel
            cursor.execute("DELETE FROM ApplicationDetail")
            cursor.execute("DELETE FROM ApplicantProfile")
            
            # reset untuk auto-increment
            cursor.execute("ALTER TABLE ApplicationDetail AUTO_INCREMENT = 1")
            cursor.execute("ALTER TABLE ApplicantProfile AUTO_INCREMENT = 1")
            
            # aktifkan kembali foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            
            connection.commit()
            print("All data cleared successfully")
            return True
        except Error as e:
            connection.rollback()
            print(f"Error clearing data: {e}")
            return False
        finally:
            cursor.close()