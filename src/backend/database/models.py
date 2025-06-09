from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CVExtractionResult(Base):
    __tablename__ = 'cv_extraction_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    skills = Column(Text, nullable=True)
    experience = Column(Text, nullable=True)
    education = Column(Text, nullable=True)
    created_at = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<CVExtractionResult(name={self.name}, email={self.email})>"