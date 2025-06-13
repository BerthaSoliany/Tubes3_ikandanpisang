import mysql.connector
from mysql.connector import Error
from typing import Optional
import os

class MySQLDatabaseManager:
    def __init__(self, host="localhost", user="root", password="", database="cv_analyzer"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        
    def create_database_if_not_exists(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            print(f"Database '{self.database}' created or already exists")
            cursor.close()
            connection.close()
        except Error as e:
            print(f"Error creating database: {e}")

    def create_tables(self):
        connection = self.get_connection()
        if not connection:
            return False
            
        try:
            cursor = connection.cursor()
            create_applicants_table = """
            CREATE TABLE IF NOT EXISTS ApplicantProfile (
                applicant_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                first_name VARCHAR(50) DEFAULT NULL,
                last_name VARCHAR(50) DEFAULT NULL,
                date_of_birth DATE DEFAULT NULL,
                address VARCHAR(255) DEFAULT NULL,
                phone_number VARCHAR(20) DEFAULT NULL
            )
            """
            create_applications_table = """
            CREATE TABLE IF NOT EXISTS ApplicationDetail (
                detail_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                applicant_id INT NOT NULL,
                application_role VARCHAR(100) DEFAULT NULL,
                cv_path TEXT,
                FOREIGN KEY (applicant_id) REFERENCES ApplicantProfile(applicant_id) ON DELETE CASCADE
            )
            """
            cursor.execute(create_applicants_table)
            cursor.execute(create_applications_table)
            connection.commit()
            print("Database tables created successfully")
            return True
        except Error as e:
            print(f"Error creating tables: {e}")
            return False
        finally:
            cursor.close()
    
    def initialize_connection(self):
        try:
            self.create_database_if_not_exists()
            if self.create_tables():
                print("Database connection initialized successfully")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Error initializing database connection: {e}")
            return False
    
    def get_connection(self):
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
            return self.connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")

db_manager = MySQLDatabaseManager()

def get_db_connection():
    return db_manager.get_connection()

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection