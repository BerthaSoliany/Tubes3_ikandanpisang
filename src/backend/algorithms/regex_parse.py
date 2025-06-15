import re
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from src.backend.utils.pdf_extract import extract_pdfs

def extract_skills_section(cv_text: str) -> list[str]:

    SKILLS_SECTION_HEADERS = ["Skills", "Skill", "skil"]
    skills_header_pattern = "|".join(re.escape(header) for header in SKILLS_SECTION_HEADERS)

    VALID_SKILL_LINE_PATTERN = r"\s*(?:[•\-]?\s*)?[A-Za-z0-9][^\r\n]*"

    skills_lines_regex = re.compile(
        r"[\r\n]+" + rf"(?:{skills_header_pattern})\s*[:]?\s*[\r\n]+"  
        rf"(?P<line1>{VALID_SKILL_LINE_PATTERN})"               # Capture Line 1
        rf"(?:[\r\n]+(?P<line2>{VALID_SKILL_LINE_PATTERN}))?"   # Capture Line 2
        rf"(?:[\r\n]+(?P<line3>{VALID_SKILL_LINE_PATTERN}))?",  # Capture Line 3
        re.IGNORECASE
    )

    extracted_lines_list = []
    
    for match in skills_lines_regex.finditer(cv_text):
        lines = []
        
        if match.group('line1') is not None:
            lines.append(match.group('line1').strip())
        
        if match.group('line2') is not None:
            lines.append(match.group('line2').strip())

        if match.group('line3') is not None:
            lines.append(match.group('line3').strip())
        
        if lines:
            extracted_lines_list.append("\n".join(lines))
    
    output = []
    for i in range(len(extracted_lines_list)):
        individual_skills = extract_individual_skills(extracted_lines_list[i])
        for skill in individual_skills:
            output.append(skill.strip()) 

    output = sorted(output, key=len)
    return output

def extract_individual_skills(skills_block_text: str) -> list[str]:
    """
    Menguraikan sebuah blok teks yang berisi daftar skill menjadi daftar skill individual.
    Prioritas pemisahan: koma, jika tidak ada, gunakan newline.
    """
    individual_skills = []
    
    temp_block = re.sub(r'^\s*[\•\-]\s*', '', skills_block_text, flags=re.MULTILINE)
    temp_block = re.sub(r'\s+', ' ', temp_block).strip()

    if ',' in temp_block:
        candidates = [s.strip() for s in temp_block.split(',') if s.strip()]
    else:
        candidates = [s.strip() for s in skills_block_text.splitlines() if s.strip()]

    for candidate in candidates:
        if candidate:
            is_excluded = False
            lower_candidate = candidate.lower()
            
            if not is_excluded:
                if re.fullmatch(r'[^A-Za-z]*', lower_candidate): # Jika hanya non-huruf
                    continue 
                if len(lower_candidate) < 2: # Skill terlalu pendek
                    continue
                if len(lower_candidate.split()) > 10: # Mungkin ini kalimat, bukan skill tunggal (heuristik)
                    pass

                individual_skills.append(candidate)
    
    return individual_skills

def extract_filtered_experience_lines(cv_text: str) -> list[str]:
    """
    Mengekstrak baris string dari bagian 'Experience'/'Work History' hingga 'Education'
    yang memenuhi kriteria: memiliki dua tahun 4 digit DAN panjang karakternya <= 10.

    Args:
        cv_text (str): Seluruh teks dari dokumen CV.

    Returns:
        list[str]: Sebuah list berisi string dari baris-baris yang lolos filter.
                   Akan mengembalikan list kosong jika tidak ditemukan.
    """
    EXPERIENCE_SECTION_HEADERS = ["Experience", "Work History"]
    EDUCATION_SECTION_HEADERS = ["Education"]
    experience_header_pattern = "|".join(re.escape(header) for header in EXPERIENCE_SECTION_HEADERS)
    education_header_pattern = "|".join(re.escape(header) for header in EDUCATION_SECTION_HEADERS)

    # Regex untuk menangkap seluruh blok pengalaman kerja
    # Dimulai dari Experience/Work History, dan berakhir TEPAT sebelum Education
    experience_block_regex = re.compile(
        r"[\s\r\n]*" + rf"(?:{experience_header_pattern}):?\s*[\r\n]+"  
        r"(?P<experience_block>[\s\S]+?)"
        rf"(?=^[ \t]*(?:{education_header_pattern})|\Z)",
        re.IGNORECASE | re.DOTALL | re.MULTILINE
    )

    filtered_output_lines = []
    FOUR_DIGIT_YEAR_PATTERN = re.compile(
        r"\b\d{4}\b.*?\b(?:\d{4}|current|present)\b",
        re.IGNORECASE
    )

    job_title = True
    for block_match in experience_block_regex.finditer(cv_text):
        experience_block_content = block_match.group('experience_block')
        
        if experience_block_content:
            lines_in_block = [line.strip() for line in experience_block_content.splitlines() if line.strip()] # Ambil hanya baris non-kosong

            for line in lines_in_block:
                if (job_title):
                    # Kondisi: memiliki 2 angka berukuran 4 digit (tahun)
                    has_two_four_digit_years = bool(FOUR_DIGIT_YEAR_PATTERN.search(line))
        
                    if has_two_four_digit_years:
                        filtered_output_lines.append(line)
                        job_title = False
                
                else:
                    filtered_output_lines.append(line)
                    job_title = True


    output = []
    for i in range(0, len(filtered_output_lines), 2):
        output.append([filtered_output_lines[i], filtered_output_lines[i+1]])
    return output

def extract_content_after_education(cv_text: str) -> list[str]:
    """
    Mengekstrak blok teks yang dimulai dari baris yang mengandung header 'Education'
    hingga akhir dokumen atau bagian CV berikutnya.

    Args:
    cv_text (str): Seluruh teks dari dokumen CV.

    Returns:
    list[str]: Sebuah list berisi string dari blok konten 'Education' yang ditemukan. 
    Akan mengembalikan list kosong jika tidak ada yang ditemukan.
    """
    EDUCATION_SECTION_HEADERS = ["Education", "Education and Training"]
    education_header_pattern = "|".join(re.escape(h) for h in EDUCATION_SECTION_HEADERS)

    education_block_regex = re.compile(
        r"(?P<education_block>[\s\S]+?)"
        rf"(?=\Z)",
        re.IGNORECASE | re.DOTALL | re.MULTILINE
    )
        
    for block_match in education_block_regex.finditer(cv_text):
        experience_block_content = block_match.group('education_block')
        
        if experience_block_content:
            lines_in_block = [line.strip() for line in experience_block_content.splitlines() if line.strip()] # Ambil hanya baris non-kosong
            return lines_in_block[0]
    
    return ""

def extract_content_after_summary(cv_text: str) -> str:
    """
    Mengekstrak blok teks yang dimulai dari baris yang mengandung header 'Summary'
    hingga akhir dokumen atau bagian CV berikutnya.

    Args:
        cv_text (str): Seluruh teks dari dokumen CV.

    Returns:
        str: String dari blok konten 'Summary' yang ditemukan.
             Akan mengembalikan string kosong jika tidak ada yang ditemukan.
    """
    SUMMARY_SECTION_HEADERS = ["Summary", "Professional Summary"] 
    summary_header_pattern = "|".join(re.escape(h) for h in SUMMARY_SECTION_HEADERS)

    summary_block_regex = re.compile(
        rf"^(?:{summary_header_pattern})\s*[:]?\s*[\r\n]+" 
        r"(?P<summary_block>[\s\S]+?)"
        rf"(?=\Z)", 
        re.IGNORECASE | re.DOTALL | re.MULTILINE 
    )
        
    for block_match in summary_block_regex.finditer(cv_text):
        summary_block_content = block_match.group('summary_block')
        
        if summary_block_content:
            lines_in_block = [line.strip() for line in summary_block_content.splitlines() if line.strip()]
            if lines_in_block:
                return lines_in_block[0]
    
    return ""

def extract_education_details(cv_text: str) -> list[list[str]]:
    """
    Mengekstrak informasi pendidikan dari bagian 'Education' CV yang memiliki:
    - Tahun (format 4 digit, MM/YYYY, atau range tahun)
    - Universitas/Institusi 
    - Jurusan/Degree
    
    Args:
    cv_text (str): Seluruh teks dari dokumen CV.

    Returns:
    list[list[str]]: List berisi pasangan [tahun_info, detail_pendidikan] dari setiap entry pendidikan yang ditemukan.
    """
    
    EDUCATION_SECTION_HEADERS = ["Education", "Education and Training", "Educational Background", "Academic Background"] # semoga ga ada lagi plspls
    education_header_pattern = "|".join(re.escape(header) for header in EDUCATION_SECTION_HEADERS)

    education_block_regex = re.compile(
        r"[\s\r\n]*" + rf"(?:{education_header_pattern}):?\s*[\r\n]+"  
        r"(?P<education_block>[\s\S]+?)"
        rf"(?=^[ \t]*(?:Skills|Experience|Work History|Projects|Certifications|References|Languages)|\Z)", # ini juga pls
        re.IGNORECASE | re.DOTALL | re.MULTILINE
    )

    filtered_education_lines = []
    
    EDUCATION_YEAR_PATTERN = re.compile(
        r"\b(?:\d{1,2}\/\d{4}|\d{4})\s*[-–—]\s*(?:\d{4}|present|current)|\b(?:\d{1,2}\/\d{4}|\d{4})\b",
        re.IGNORECASE
    )
    
    DEGREE_KEYWORDS = [ # udah sesemua ini gaksih
        r"\b(?:bachelor|master|phd|doctorate|diploma|certificate|degree)\b",
        r"\b(?:b\.?a\.?|b\.?s\.?|b\.?sc\.?|m\.?a\.?|m\.?s\.?|m\.?sc\.?|ph\.?d\.?)\b",
        r"\b(?:sarjana|magister|doktor|diploma|sertifikat)\b",
        r"\b(?:master of science|bachelor of science|bachelor of arts|master of arts)\b",
        r"\b(?:cfa|mba|certification|certified)\b",
        r"\b(?:some college|no degree)\b"
    ]
    degree_pattern = "|".join(DEGREE_KEYWORDS)
    DEGREE_PATTERN = re.compile(degree_pattern, re.IGNORECASE)

    INSTITUTION_KEYWORDS = [
        r"\buniversity\b", r"\buniversitas\b", r"\bcollege\b", r"\binstitute\b", 
        r"\binstitut\b", r"\bacademy\b", r"\bakademi\b", r"\bschool\b", r"\bsekolah\b",
        r"\budemy\b", r"\bcoursera\b", r"\bqau\b" # ini juga amin
    ]
    institution_pattern = "|".join(INSTITUTION_KEYWORDS)
    INSTITUTION_PATTERN = re.compile(institution_pattern, re.IGNORECASE)

    for block_match in education_block_regex.finditer(cv_text):
        education_block_content = block_match.group('education_block')
        
        if education_block_content:
            lines_in_block = [line.strip() for line in education_block_content.splitlines() if line.strip()]
            
            i = 0
            while i < len(lines_in_block):
                current_line = lines_in_block[i]
                
                year_only_match = re.match(r'^\s*(\d{1,2}/\d{4}|\d{4})\s*$', current_line)
                if year_only_match:
                    year = year_only_match.group(1)
                    if i + 1 < len(lines_in_block):
                        education_info = lines_in_block[i + 1]
                        filtered_education_lines.append([year, education_info])
                        i += 2
                    else:
                        i += 1
                else:
                    year_match = EDUCATION_YEAR_PATTERN.search(current_line)
                    if year_match and (DEGREE_PATTERN.search(current_line) or INSTITUTION_PATTERN.search(current_line)):
                        year = year_match.group()
                        education_info = re.sub(EDUCATION_YEAR_PATTERN, '', current_line).strip()
                        if education_info:
                            filtered_education_lines.append([year, education_info])
                    i += 1

    return filtered_education_lines

def get_summary(cv_text: str) -> dict[str, list[str]]:
    """
    Mengambil ringkasan dari teks CV, termasuk bagian 'Skills', 'Experience', dan 'Education'.

    Args:
        cv_text (str): Teks lengkap dari CV.

    Returns:
        dict[str, list[str]]: Ringkasan yang berisi bagian-bagian yang relevan.
    """
    summary = {
        "summary": extract_content_after_summary(cv_text),
        "skills": extract_skills_section(cv_text),
        "experience": extract_filtered_experience_lines(cv_text),
        "education": extract_education_details(cv_text),
    }
    
    return summary

if __name__ == "__main__":

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
    data_dir = os.path.join(project_root, 'data')

    dict_of_cv_texts = extract_pdfs(data_dir, max_workers=os.cpu_count()) 

    res = get_summary(dict_of_cv_texts[data_dir + '\\70892619.pdf'])
    print(res)
    
    # if outputs:
    #     print(f"Ditemukan {len(outputs)} bagian 'Skills':")
    #     for i, output in enumerate(outputs):
    #         if i < 3:
    #             print(f"\n--- Skill {i+1} ---")
    #             print(output.strip()) # .strip() untuk menghilangkan spasi/newline ekstra di awal/akhir
    #             print("---------------")
    #         else: break
    # else:
    #     print("Tidak ditemukan bagian 'Skills' yang sesuai dengan pola regex.")

    # if job_history:
    #     print(f"Ditemukan {len(job_history)} bagian 'Job_history':")
    #     for i, job in enumerate(job_history):
    #         print(f"\n--- Job {i+1} ---")
    #         print(job[0].strip()) # .strip() untuk menghilangkan spasi/newline ekstra di awal/akhir
    #         print(job[1].strip())
    #         print("---------------")
    # else:
    #     print("Tidak ditemukan bagian 'Job_history' yang sesuai dengan pola regex.")

    # if edu:
    #     print(f"\n--- latest education ---")
    #     print(edu)
    #     print("---------------")
    # else:
    #     print("Tidak ditemukan bagian 'edu' yang sesuai dengan pola regex.")