from datetime import datetime, date
from typing import Optional, Dict, Any
try:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from src.backend.utils.encryption import encrypt, decrypt, encrypt_date, decrypt_date
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
    from src.backend.utils.encryption import encrypt, decrypt, encrypt_date, decrypt_date

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
    
    # properties dengan encryption/decryption
    @property
    def first_name(self) -> Optional[str]:
        return decrypt(self._first_name) if self._first_name else None
    
    @first_name.setter
    def first_name(self, value: Optional[str]):
        self._first_name = encrypt(value) if value else None
    
    @property
    def last_name(self) -> Optional[str]:
        return decrypt(self._last_name) if self._last_name else None
    
    @last_name.setter
    def last_name(self, value: Optional[str]):
        self._last_name = encrypt(value) if value else None

    @property
    def date_of_birth(self) -> Optional[date]:
        if self._date_of_birth:
            if isinstance(self._date_of_birth, (date, datetime)):
                print(f"Date already a date object: {self._date_of_birth}")
                if isinstance(self._date_of_birth, datetime):
                    return decrypt_date(self._date_of_birth.date())
                return decrypt_date(self._date_of_birth.isoformat())
            else:
                print(f"Unexpected date_of_birth type: {type(self._date_of_birth)}")
                return None
        return None
    
    @date_of_birth.setter
    def date_of_birth(self, value: Optional[date]):
        if value:
            date_str = value.isoformat()
            self._date_of_birth = encrypt_date(date_str)
        else:
            self._date_of_birth = None
    
    @property
    def address(self) -> Optional[str]:
        return decrypt(self._address) if self._address else None
    
    @address.setter
    def address(self, value: Optional[str]):
        self._address = encrypt(value) if value else None
    
    @property
    def phone_number(self) -> Optional[str]:
        return decrypt(self._phone_number) if self._phone_number else None
    
    @phone_number.setter
    def phone_number(self, value: Optional[str]):
        self._phone_number = encrypt(value) if value else None

    # metode untuk database operations (encrypted data)
    def get_encrypted_first_name(self) -> Optional[str]:
        return self._first_name
    
    def get_encrypted_last_name(self) -> Optional[str]:
        return self._last_name
    
    def get_encrypted_date_of_birth(self) -> Optional[str]:
        return self._date_of_birth
    
    def get_encrypted_address(self) -> Optional[str]:
        return self._address
    
    def get_encrypted_phone_number(self) -> Optional[str]:
        return self._phone_number
    
    def set_encrypted_first_name(self, encrypted_value: Optional[str]):
        self._first_name = encrypted_value
    
    def set_encrypted_last_name(self, encrypted_value: Optional[str]):
        self._last_name = encrypted_value

    def set_encrypted_date_of_birth(self, encrypted_value: Optional[str]):
        self._date_of_birth = encrypted_value
    
    def set_encrypted_address(self, encrypted_value: Optional[str]):
        self._address = encrypted_value
    
    def set_encrypted_phone_number(self, encrypted_value: Optional[str]):
        self._phone_number = encrypted_value

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
            obj = cls()
            obj.applicant_id = row[0]
            obj.set_encrypted_first_name(row[1])
            obj.set_encrypted_last_name(row[2])
            obj.set_encrypted_date_of_birth(row[3])
            obj.set_encrypted_address(row[4])
            obj.set_encrypted_phone_number(row[5])
            return obj
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