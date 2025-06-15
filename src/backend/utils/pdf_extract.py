import os
import re
import pdfplumber
from typing import Optional
import concurrent.futures

def extract_pdfs(directory, max_workers=None):    
    if not os.path.exists(directory):
        print(f"Direktori tidak ditemukan: {directory}")
        return False
    
    pdf_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    
    if not pdf_files:
        print("Tidak ada file PDF ditemukan di direktori dan subfoldernya.")
        return False
    
    print(f"Ditemukan {len(pdf_files)} file PDF di direktori dan subfoldernya.")
    
    extracted_data = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for result_tuple in executor.map(extract_pdf_to_file, pdf_files):
            if result_tuple is not False:
                pdf_path, extracted_text = result_tuple
                relative_path = os.path.relpath(pdf_path, directory)
                extracted_data[relative_path] = extracted_text

    if not extracted_data:
        print("Tidak ada teks yang berhasil diekstrak dari PDF manapun.")
        return False
        
    print(f"Berhasil mengekstrak teks dari {len(extracted_data)} file PDF.")
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
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            extracted_text = text.strip()
        
    except Exception as e:
        print(f"Error extracting with pdfplumber: {e}")

    return extracted_text if extracted_text else None