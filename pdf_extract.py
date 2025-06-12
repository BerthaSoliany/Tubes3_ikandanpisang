import os
import sys
from datetime import datetime
from src.backend.utils.pdf_extractor import extract_text

def extract_pdf_to_file(pdf_path, output_file=None):
    """
    Ekstrak PDF dan simpan hasil ke file teks
    
    Args:
        pdf_path (str): Path ke file PDF
        output_file (str): Path output file (optional)
    """
    
    if not os.path.exists(pdf_path):
        print(f"File PDF tidak ditemukan: {pdf_path}")
        return False
    
    # generate nama file output jika tidak diberikan
    if output_file is None:
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"extracted_{pdf_name}_{timestamp}.txt"
    
    print(f"Extracting: {pdf_path}")
    print(f"Output: {output_file}")
    
    try:
        print("Extracting raw text...")
        raw_text = extract_text(pdf_path)
        if raw_text is None:
            raw_text = "No text could be extracted from the PDF."
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"PDF EXTRACTION RESULTS\n")
            f.write(f"Source: {pdf_path}\n")
            f.write(f"Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

            f.write("RAW EXTRACTED TEXT:\n")
            f.write(raw_text)
            
            f.write("END OF EXTRACTION\n")
        
        print(f"Extraction completed!")
        print(f"Results saved to: {os.path.abspath(output_file)}")
        print(f"Text length: {len(raw_text)} characters")
    except Exception as e:
        print(f"Error: {str(e)}")
        
        # simpan error ke file
        error_file = f"error_{os.path.splitext(os.path.basename(pdf_path))[0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(error_file, 'w', encoding='utf-8') as f:
            f.write(f"Error extracting: {pdf_path}\n")
            f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Error: {str(e)}\n")
        
        print(f"Error log saved to: {error_file}")
        return False

def main():
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        extract_pdf_to_file(pdf_path, output_file)
    else:
        cv_dir = "data/cv_samples"
        pdf_found = False
        
        if os.path.exists(cv_dir):
            pdf_files = [f for f in os.listdir(cv_dir) if f.lower().endswith('.pdf')]
            if pdf_files:
                pdf_path = os.path.join(cv_dir, pdf_files[0])
                print(f"Using first PDF found: {pdf_files[0]}")
                extract_pdf_to_file(pdf_path)
                pdf_found = True
        
        if not pdf_found:
            print("No PDF files found!")

if __name__ == "__main__":
    main()