try:
    from .connection import db_manager
    from .models import ApplicantProfile, ApplicationDetail
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from connection import db_manager
    from models import ApplicantProfile, ApplicationDetail

from datetime import date
import mysql.connector

def seed_data():
    if not db_manager.initialize_connection():
        print("Failed to initialize database")
        return False
    
    print("Starting database seeding with new schema...")
    sample_data = [
        {
            "applicant": {
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "+1234567890",
                "address": "123 Tech Street, Silicon Valley, CA",
                "date_of_birth": date(1995, 5, 15)
            },
            "applications": [
                {
                    "application_role": "Software Engineer",
                    "cv_path": "data/cv_samples/john_doe_software_engineer.pdf"
                }
            ]
        },
        {
            "applicant": {
                "first_name": "Jane",
                "last_name": "Smith", 
                "phone_number": "+1234567891",
                "address": "456 Data Lane, Boston, MA",
                "date_of_birth": date(1992, 8, 22)
            },       
            "applications": [
                {
                    "application_role": "Data Scientist",
                    "cv_path": "data/cv_samples/jane_smith_data_scientist.pdf"
                }
            ]
        },
        {
            "applicant": {
                "first_name": "Mike",
                "last_name": "Johnson",
                "phone_number": "+1234567892", 
                "address": "789 Frontend Ave, Seattle, WA",
                "date_of_birth": date(1994, 12, 10)
            },            
            "applications": [
                {
                    "application_role": "Frontend Developer",
                    "cv_path": "data/cv_samples/mike_johnson_frontend.pdf"
                }
            ]
        },
        {
            "applicant": {
                "first_name": "Sarah",
                "last_name": "Wilson",
                "phone_number": "+1234567893",
                "address": "321 Backend Blvd, Austin, TX", 
                "date_of_birth": date(1993, 3, 8)
            },            
            "applications": [
                {
                    "application_role": "Backend Developer",
                    "cv_path": "data/cv_samples/sarah_wilson_backend.pdf"
                }
            ]
        },
        {
            "applicant": {
                "first_name": "David",
                "last_name": "Brown",
                "phone_number": "+1234567894",
                "address": "654 Cloud St, Denver, CO",
                "date_of_birth": date(1990, 7, 25)
            },            
            "applications": [
                {
                    "application_role": "DevOps Engineer", 
                    "cv_path": "data/cv_samples/david_brown_devops.pdf"
                }
            ]
        }
    ]
    
    connection = db_manager.get_connection()
    if not connection:
        print("Failed to get database connection")
        return False
    
    cursor = connection.cursor()
    success_count = 0
    error_count = 0
    
    try:
        for data in sample_data:
            try:
                applicant_data = data["applicant"]
                insert_applicant_sql = """
                INSERT INTO ApplicantProfile (first_name, last_name, date_of_birth, address, phone_number)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_applicant_sql, (
                    applicant_data["first_name"],
                    applicant_data["last_name"], 
                    applicant_data["date_of_birth"],
                    applicant_data["address"],
                    applicant_data["phone_number"]
                ))
                
                applicant_id = cursor.lastrowid
                print(f"Created applicant: {applicant_data['first_name']} {applicant_data['last_name']} (ID: {applicant_id})")

                for app_data in data["applications"]:
                    insert_application_sql = """
                    INSERT INTO ApplicationDetail (applicant_id, application_role, cv_path)
                    VALUES (%s, %s, %s)
                    """
                    cursor.execute(insert_application_sql, (
                        applicant_id,
                        app_data["application_role"],
                        app_data["cv_path"]
                    ))
                    
                    detail_id = cursor.lastrowid
                    print(f"Created application: {app_data['application_role']} (Detail ID: {detail_id})")
                    success_count += 1
            except mysql.connector.Error as e:
                print(f"Error processing {data['applicant']['first_name']}: {e}")
                error_count += 1
                
        connection.commit()
        
    except Exception as e:
        print(f"General error: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
    
    print(f"\nSeeding Complete!")
    print(f"Successful operations: {success_count}")
    print(f"Errors: {error_count}")
    
    return error_count == 0

def clear_database():
    connection = db_manager.get_connection()
    if not connection:
        print("Failed to get database connection")
        return False
        
    cursor = connection.cursor()
    
    try:
        cursor.execute("DELETE FROM ApplicationDetail")
        cursor.execute("DELETE FROM ApplicantProfile")
        connection.commit()
        print("Database cleared successfully")
        return True
    except mysql.connector.Error as e:
        print(f"Error clearing database: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()

def main():
    """ Main seeding function"""
    print("1. Seed sample data (5 applicants)")
    print("2. Clear database")
    print("3. Show statistics")
    print("0. Exit")
    
    while True:
        choice = input("\nEnter your choice (0-3): ").strip()
        if choice == "1":
            seed_data()
        elif choice == "2":
            confirm = input("Are you sure you want to clear all data? (y/n): ").strip().lower()
            if confirm == 'y':
                clear_database()
        elif choice == "3":
            if db_manager.initialize_connection():
                pass
            else:
                print("Failed to connect to database")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()