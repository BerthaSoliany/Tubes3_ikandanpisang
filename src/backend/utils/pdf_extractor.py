# ini ada beberapa fungsi untuk ekstraksi, untuk yang biasa aja pake PyPDF2
import PyPDF2
import pdfplumber
import re
from typing import Optional, Dict, List
import os
from pathlib import Path

class PDFExtractor:
    def __init__(self):
        self.extracted_text = ""
        self.extraction_method = None

    def extract_text_pypdf2(self, pdf_path: str) -> Optional[str]:
        """
        Extract text using PyPDF2 library
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                
                self.extraction_method = "PyPDF2"
                return text.strip()
        except Exception as e:
            print(f"Error extracting with PyPDF2: {e}")
            return None
    
    def extract_text_pdfplumber(self, pdf_path: str) -> Optional[str]:
        """
        Extract text using pdfplumber library
        ini untuk yang lebih kompleks (might delete later)
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                
                self.extraction_method = "pdfplumber"
                return text.strip()
        except Exception as e:
            print(f"Error extracting with pdfplumber: {e}")
            return None
    
    def extract_text(self, pdf_path: str, method: str = "auto") -> Optional[str]:
        """
        Main extraction method dengan fallback support
        Args:
            pdf_path: Path to PDF file
            method: 'auto', 'pypdf2', 'pdfplumber'
        Returns:
            Extracted text or None if extraction fails
        """
        if not os.path.exists(pdf_path):
            print(f"PDF file not found: {pdf_path}")
            return None
        if not pdf_path.lower().endswith('.pdf'):
            print(f"File is not a PDF: {pdf_path}")
            return None
        
        extracted_text = None
        
        # defaultnya pake pypdf2 for now
        if method == "auto":
            extracted_text = self.extract_text_pypdf2(pdf_path)
        
        elif method == "pypdf2":
            extracted_text = self.extract_text_pypdf2(pdf_path)
        
        elif method == "pdfplumber":
            extracted_text = self.extract_text_pdfplumber(pdf_path)
        
        else:
            raise ValueError("Method must be 'auto', 'pypdf2', or 'pdfplumber'")
        
        if extracted_text:
            self.extracted_text = extracted_text
            return self.clean_text(extracted_text)
        
        return None
    
    def clean_text(self, text: str) -> str:
        """
        Clean extracted text untuk better pattern matching
        """
        if not text:
            return ""
        
        # remove whitespace berlebihan
        text = re.sub(r'\s+', ' ', text)
        
        # remove special character kecuali yang umum digunakan
        text = re.sub(r'[^\w\s\.\,\-\(\)\@\+\#\&\%\$\!]', ' ', text)
        
        # remove spaces berlebihan
        text = re.sub(r' +', ' ', text)
        
        # bersihin line breaks
        text = text.replace('\n\n', '\n').replace('\r', '')
        
        return text.strip()
    
    def get_extraction_info(self) -> Dict[str, str]:
        """ Info hasil ekstraksi """
        return {
            'method': self.extraction_method or "None",
            'text_length': str(len(self.extracted_text)),
            'word_count': str(len(self.extracted_text.split()) if self.extracted_text else 0)
        }

# util functions
def extract_text(pdf_path: str, method: str = "auto") -> Optional[str]:
    """    
    Args:
        pdf_path: Path to PDF file
        method: Extraction method ('auto', 'pypdf2', 'pdfplumber')
    
    Returns:
        Extracted text or None
    """
    extractor = PDFExtractor()
    return extractor.extract_text(pdf_path, method)