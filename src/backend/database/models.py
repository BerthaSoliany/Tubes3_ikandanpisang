from datetime import datetime, date
from typing import Optional, Dict, Any

class ApplicantProfile:
    """ Ini untuk menyimpan applicant basic information """
    def __init__(self, applicant_id: Optional[int] = None, 
                 first_name: Optional[str] = None, 
                 last_name: Optional[str] = None,
                 date_of_birth: Optional[date] = None, 
                 address: Optional[str] = None, 
                 phone_number: Optional[str] = None):
        self.applicant_id = applicant_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.address = address
        self.phone_number = phone_number
    
    def to_dict(self):
        """ Convert ke dictionary untuk JSON """
        return {
            'applicant_id': self.applicant_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth is not None else None,
            'address': self.address,
            'phone_number': self.phone_number
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """ Buat instance dari dictionary """
        obj = cls()
        obj.applicant_id = data.get('applicant_id')
        obj.first_name = data.get('first_name')
        obj.last_name = data.get('last_name')
        obj.address = data.get('address')
        obj.phone_number = data.get('phone_number')
        
        if data.get('date_of_birth'):
            if isinstance(data['date_of_birth'], str):
                obj.date_of_birth = datetime.fromisoformat(data['date_of_birth']).date()        
        return obj
    
    @classmethod
    def from_row(cls, row: tuple):
        """ Buat instance dari database row"""
        if len(row) >= 6:
            return cls(
                applicant_id=row[0],
                first_name=row[1],
                last_name=row[2],
                date_of_birth=row[3],
                address=row[4],
                phone_number=row[5]
            )
        return cls()

class ApplicationDetail:
    """ Model untuk menyimpan job application details dan isi dari CV """
    def __init__(self, detail_id: Optional[int] = None, 
                 applicant_id: Optional[int] = None,
                 application_role: Optional[str] = None, 
                 cv_path: Optional[str] = None):
        self.detail_id = detail_id
        self.applicant_id = applicant_id
        self.application_role = application_role
        self.cv_path = cv_path

    def to_dict(self):
        """ Convert ke dictionary untuk JSON"""
        return {
            'detail_id': self.detail_id,
            'applicant_id': self.applicant_id,
            'application_role': self.application_role,
            'cv_path': self.cv_path
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """ Buat instance dari dictionary """
        obj = cls()
        obj.detail_id = data.get('detail_id')
        obj.applicant_id = data.get('applicant_id')
        obj.application_role = data.get('application_role')
        obj.cv_path = data.get('cv_path')
        
        return obj
    
    @classmethod
    def from_row(cls, row: tuple):
        """ Buat instance dari database row"""
        if len(row) >= 4:
            return cls(
                detail_id=row[0],
                applicant_id=row[1],
                application_role=row[2],
                cv_path=row[3]
            )
        return cls()