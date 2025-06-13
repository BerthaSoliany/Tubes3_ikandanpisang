import sys
import os
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.backend.utils.pdf_extractor import PDFExtractor

def test_pdf_extraction():
    cv_samples_path = Path("data/cv_samples")
    pdf_files = list(cv_samples_path.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in data/cv_samples/")
        print("Please add some PDF CV files to test extraction")
        return
    
    print(f"Found {len(pdf_files)} PDF files for testing:")
    
    for pdf_file in pdf_files:
        print(f"\n{'='*60}")
        print(f"Testing: {pdf_file.name}")
        print(f"{'='*60}")
        
        try:
            extractor = PDFExtractor()
            raw_text = extractor.extract_text(str(pdf_file))
            
            if raw_text:
                info = extractor.get_extraction_info()
                print(f"Extraction successful!")
                print(f"   Method: {info['method']}")
                print(f"   Text length: {info['text_length']} characters")
                print(f"   Word count: {info['word_count']} words")    
            else:
                print("❌ Extraction failed!")
        except Exception as e:
            print(f"❌ Error processing {pdf_file.name}: {e}")

def demonstrate_extraction_methods():
    """Demonstrate different extraction methods"""
    
    print("\n" + "="*60)
    print("EXTRACTION METHODS DEMONSTRATION")
    print("="*60)
    
    # Look for any PDF file
    cv_samples_path = Path("data/cv_samples")
    pdf_files = list(cv_samples_path.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files available for method demonstration")
        return
    
    test_file = pdf_files[0]
    print(f"Testing with: {test_file.name}")
    
    extractor = PDFExtractor()
    
    # Test PyPDF2
    print(f"\n1. PyPDF2 Method:")
    text1 = extractor.extract_text_pypdf2(str(test_file))
    if text1:
        print(f"   ✅ Success - {len(text1)} characters")
        print(f"   Preview: {text1[:100]}...")
    else:
        print(f"   ❌ Failed")
    
    # Test pdfplumber
    print(f"\n2. pdfplumber Method:")
    text2 = extractor.extract_text_pdfplumber(str(test_file))
    if text2:
        print(f"   ✅ Success - {len(text2)} characters")
        print(f"   Preview: {text2[:100]}...")
    else:
        print(f"   ❌ Failed")
    
    # Test auto method
    print(f"\n3. Auto Method (with fallback):")
    text3 = extractor.extract_text(str(test_file), method="auto")
    if text3:
        info = extractor.get_extraction_info()
        print(f"   ✅ Success - Selected method: {info['method']}")
        print(f"   Text length: {info['text_length']} characters")
    else:
        print(f"   ❌ Failed")