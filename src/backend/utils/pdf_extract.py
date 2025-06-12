import os
import re
import PyPDF2
from typing import Optional
import concurrent.futures

def extract_pdfs(directory, max_workers=None):    
    if not os.path.exists(directory):
        print(f"Direktori tidak ditemukan: {directory}")
        return False
    
    pdf_files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("Tidak ada file PDF ditemukan di direktori ini.")
        return False
    
    extracted_data = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        pdf_paths = [os.path.join(directory, f) for f in pdf_files]
        for result_tuple in executor.map(extract_pdf_to_file, pdf_paths):
            if result_tuple is not False:
                pdf_name, extracted_text = result_tuple
                extracted_data[pdf_name] = extracted_text

    if not extracted_data:
        print("Tidak ada teks yang berhasil diekstrak dari PDF manapun.")
        return False
        
    return extracted_data

def extract_pdf_to_file(pdf_path, output_file=None):
    if not os.path.exists(pdf_path):
        print(f"File PDF tidak ditemukan: {pdf_path}")
        return False
    
    try:
        raw_text = extract_text(pdf_path)
        if raw_text is None:
            raw_text = "No text could be extracted from the PDF."
        
        print(f"Extraction completed!")
        return pdf_path, raw_text

    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def extract_text(pdf_path: str) -> Optional[str]:
    if not os.path.exists(pdf_path):
        print(f"PDF file not found: {pdf_path}")
        return None
    
    if not pdf_path.lower().endswith('.pdf'):
        print(f"File is not a PDF: {pdf_path}")
        return None
    
    extracted_text = None

    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            extracted_text = text.strip()
        
    except Exception as e:
        print(f"Error extracting with PyPDF2: {e}")
    
    if extracted_text:
        return clean_text(extracted_text)
    return None

def clean_text(text: str) -> str:
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