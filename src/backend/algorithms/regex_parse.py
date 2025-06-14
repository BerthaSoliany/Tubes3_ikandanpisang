import re
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from src.backend.utils.pdf_extract import extract_pdfs

def extract_skills_section(cv_text: str) -> list[str]:

    SKILLS_SECTION_HEADERS = ["Skills", "Skill", "skil"]
    skills_header_pattern = "|".join(re.escape(header) for header in SKILLS_SECTION_HEADERS)

    # Pola untuk satu baris skill yang valid:
    #   \s* : Nol atau lebih spasi di awal baris
    #   (?:[•\-]?\s*)? : Opsional bullet point (• atau -) diikuti spasi, grup ini opsional
    #   [A-Za-z0-9] : Baris harus dimulai dengan huruf (besar/kecil) atau angka
    #   [^\r\n]* : Sisa dari baris tersebut (apapun kecuali newline)
    # Tujuan: Menghindari menangkap baris kosong atau baris yang hanya spasi, atau baris yang bukan item daftar.
    VALID_SKILL_LINE_PATTERN = r"\s*(?:[•\-]?\s*)?[A-Za-z0-9][^\r\n]*"

    skills_lines_regex = re.compile(
        # Cari judul 'Skills' atau 'Skill' secara case-insensitive
        r"[\r\n]+" + rf"(?:{skills_header_pattern})\s*[:]?\s*[\r\n]+"  
        rf"(?P<line1>{VALID_SKILL_LINE_PATTERN})"               # Capture Line 1
        rf"(?:[\r\n]+(?P<line2>{VALID_SKILL_LINE_PATTERN}))?"   # Capture Line 2 (optional)
        rf"(?:[\r\n]+(?P<line3>{VALID_SKILL_LINE_PATTERN}))?",  # Capture Line 3 (optional)
        re.IGNORECASE # Mengaktifkan pencocokan case-insensitive
    )

    extracted_lines_list = []
    
    # Menggunakan finditer untuk menemukan semua kemunculan judul 'Skills'
    for match in skills_lines_regex.finditer(cv_text):
        lines = []
        # Ambil setiap grup yang ditangkap (line1, line2, line3)
        # Regex sudah memastikan mereka sesuai pola "valid skill line" dan tidak None.
        # Kita masih perlu .strip() untuk menghilangkan spasi di awal/akhir baris yang ditangkap.
        
        if match.group('line1') is not None:
            lines.append(match.group('line1').strip())
        
        if match.group('line2') is not None:
            lines.append(match.group('line2').strip())

        if match.group('line3') is not None:
            lines.append(match.group('line3').strip())
        
        # Gabungkan baris yang ditemukan menjadi satu string, dipisahkan oleh newline
        if lines: # Hanya tambahkan jika ada baris yang berhasil diekstrak
            extracted_lines_list.append("\n".join(lines))
    
    output = []
    for i in range(len(extracted_lines_list)):
        # Menguraikan setiap blok teks skill menjadi daftar skill individual
        individual_skills = extract_individual_skills(extracted_lines_list[i])
        # Ganti blok teks dengan daftar skill individual
        for skill in individual_skills:
            output.append(skill.strip())  # .strip() untuk menghilangkan spasi di awal/akhir skill

    output = sorted(output, key=len)
    return output

def extract_individual_skills(skills_block_text: str) -> list[str]:
    """
    Menguraikan sebuah blok teks yang berisi daftar skill menjadi daftar skill individual.
    Prioritas pemisahan: koma, jika tidak ada, gunakan newline.
    """
    individual_skills = []
    
    # Normalisasi spasi dan bullet points
    # Hapus bullet points/dash jika ada, dan spasi di sekitarnya
    temp_block = re.sub(r'^\s*[\•\-]\s*', '', skills_block_text, flags=re.MULTILINE)
    temp_block = re.sub(r'\s+', ' ', temp_block).strip() # Normalisasi spasi berlebihan menjadi satu spasi

    # Cek apakah blok mengandung koma sebagai pemisah utama
    if ',' in temp_block:
        # Jika ada koma, pecah berdasarkan koma
        candidates = [s.strip() for s in temp_block.split(',') if s.strip()]
    else:
        # Jika tidak ada koma, pecah berdasarkan newline dari teks ASLI (sebelum dinormalisasi penuh)
        # Ini penting agar skill "per baris" tidak bergabung jadi satu string panjang
        candidates = [s.strip() for s in skills_block_text.splitlines() if s.strip()]
        # Tambahan filter untuk baris kosong setelah splitlines

    for candidate in candidates:
        if candidate: # Pastikan kandidat tidak kosong
            is_excluded = False
            lower_candidate = candidate.lower()
            
            if not is_excluded:
                # Validasi tambahan: Pastikan skill tidak hanya angka atau terlalu pendek/terlalu panjang
                # Misalnya, skill harus punya setidaknya 2 huruf
                if re.fullmatch(r'[^A-Za-z]*', lower_candidate): # Jika hanya non-huruf
                    continue # Lewati jika hanya berisi simbol/angka
                if len(lower_candidate) < 2: # Skill terlalu pendek
                    continue
                if len(lower_candidate.split()) > 10: # Mungkin ini kalimat, bukan skill tunggal (heuristik)
                    # Jangan langsung exclude, mungkin ada skill panjang (e.g. "Problem Solving and Decision Making")
                    # Tapi bisa menjadi titik untuk pemecahan lebih lanjut atau filtering
                    pass # Untuk saat ini biarkan saja, tapi pertimbangkan ini.

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
        rf"(?=^[ \t]*(?:{education_header_pattern})|\Z)",  # ini bagian diperbaiki
        re.IGNORECASE | re.DOTALL | re.MULTILINE
    )

    filtered_output_lines = []
    FOUR_DIGIT_YEAR_PATTERN = re.compile(
        r"\b\d{4}\b.*?\b(?:\d{4}|current|present)\b",
        re.IGNORECASE
    )


    # 1. Ekstrak Blok Besar Pengalaman Kerja
    job_title = True
    for block_match in experience_block_regex.finditer(cv_text):
        experience_block_content = block_match.group('experience_block')
        
        if experience_block_content:
            # 2. Ambil semua baris ke dalam list of string
            lines_in_block = [line.strip() for line in experience_block_content.splitlines() if line.strip()] # Ambil hanya baris non-kosong

            # 3. Filter Baris berdasarkan kriteria
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
    EDUCATION_SECTION_HEADERS = ["Education", "Education and Training"] # Pastikan ini mencakup semua varian
    education_header_pattern = "|".join(re.escape(h) for h in EDUCATION_SECTION_HEADERS)


    # Regex untuk menemukan baris header 'Education' dan menangkap semua teks setelahnya
    # hingga awal bagian CV berikutnya atau akhir dokumen.
    # r"^(?:.*?" + rf"(?:{education_header_pattern})") Mencari header di awal baris manapun.
    # re.escape(h) for h in ALL_CV_SECTION_HEADERS if h not in EDUCATION_SECTION_HEADERS
    # Memastikan header yang menjadi penutup tidak termasuk header Education itu sendiri.

    # Pola ini akan mencari baris yang mengandung 'education_header_pattern'
    # dan kemudian menangkap sisanya sebagai 'education_block'.
    
    # Strategi: Tangkap dari *awal baris* yang berisi header education
    #           hingga *awal baris* header berikutnya atau akhir dokumen.
    education_block_regex = re.compile(
        # Cari baris yang mengandung header Education (dimulai dari awal baris)
        # ^ : Awal baris (karena re.MULTILINE)
        # .*? : Karakter apapun (non-greedy) hingga header
        # (?:{education_header_pattern}) : Cocokkan header Education
        # .* : Sisa dari baris header
        # [\r\n]+ : Satu atau lebih newline (untuk melewati baris header itu sendiri)
        # (?P<education_block>[\s\S]+?) : Tangkap semua konten hingga...
        # (?=...) : ...lookahead yang menandakan akhir blok
        
        # Contoh: Jika 'Education' di tengah baris, dan kita ingin seluruh baris itu jadi penanda
        # ^[^\r\n]*(?:{education_header_pattern})[^\r\n]*[\r\n]+(?P<education_block>[\s\S]+?)(?=...|\Z)
        
        # Regex yang paling umum dan robust untuk ini:
        # Cari header, kemudian tangkap blok hingga header berikutnya atau akhir dokumen
        rf"^(?:{education_header_pattern})\s*[:]?\s*[\r\n]+" # Header baris, opsional titik dua, newline
        r"(?P<education_block>[\s\S]+?)"
        rf"(?=\Z)", # Tangkap semua konten (non-greedy)
        re.IGNORECASE | re.DOTALL | re.MULTILINE # DOTALL untuk [\s\S] mencakup \n, MULTILINE untuk ^
    )
        
    for block_match in education_block_regex.finditer(cv_text):
        experience_block_content = block_match.group('education_block')
        
        if experience_block_content:
            # 2. Ambil semua baris ke dalam list of string
            lines_in_block = [line.strip() for line in experience_block_content.splitlines() if line.strip()] # Ambil hanya baris non-kosong
            return lines_in_block[0]
    
    return None

def extract_content_after_summary(cv_text: str) -> list[str]:
    """
    Mengekstrak blok teks yang dimulai dari baris yang mengandung header 'Education'
    hingga akhir dokumen atau bagian CV berikutnya.

    Args:
        cv_text (str): Seluruh teks dari dokumen CV.

    Returns:
        list[str]: Sebuah list berisi string dari blok konten 'Education' yang ditemukan.
                   Akan mengembalikan list kosong jika tidak ada yang ditemukan.
    """
    SUMMARY_SECTION_HEADERS = ["Summary", "Professional Summary"] # Pastikan ini mencakup semua varian
    summmary_header_pattern = "|".join(re.escape(h) for h in SUMMARY_SECTION_HEADERS)


    # Regex untuk menemukan baris header 'Education' dan menangkap semua teks setelahnya
    # hingga awal bagian CV berikutnya atau akhir dokumen.
    # r"^(?:.*?" + rf"(?:{summmary_header_pattern})") Mencari header di awal baris manapun.
    # re.escape(h) for h in ALL_CV_SECTION_HEADERS if h not in EDUCATION_SECTION_HEADERS
    # Memastikan header yang menjadi penutup tidak termasuk header Education itu sendiri.

    # Pola ini akan mencari baris yang mengandung 'summmary_header_pattern'
    # dan kemudian menangkap sisanya sebagai 'education_block'.
    
    # Strategi: Tangkap dari *awal baris* yang berisi header education
    #           hingga *awal baris* header berikutnya atau akhir dokumen.
    summary_block_regex = re.compile(
        # Cari baris yang mengandung header Education (dimulai dari awal baris)
        # ^ : Awal baris (karena re.MULTILINE)
        # .*? : Karakter apapun (non-greedy) hingga header
        # (?:{summmary_header_pattern}) : Cocokkan header Education
        # .* : Sisa dari baris header
        # [\r\n]+ : Satu atau lebih newline (untuk melewati baris header itu sendiri)
        # (?P<education_block>[\s\S]+?) : Tangkap semua konten hingga...
        # (?=...) : ...lookahead yang menandakan akhir blok
        
        # Contoh: Jika 'Education' di tengah baris, dan kita ingin seluruh baris itu jadi penanda
        # ^[^\r\n]*(?:{summmary_header_pattern})[^\r\n]*[\r\n]+(?P<education_block>[\s\S]+?)(?=...|\Z)
        
        # Regex yang paling umum dan robust untuk ini:
        # Cari header, kemudian tangkap blok hingga header berikutnya atau akhir dokumen
        rf"^(?:{summmary_header_pattern})\s*[:]?\s*[\r\n]+" # Header baris, opsional titik dua, newline
        r"(?P<education_block>[\s\S]+?)"
        rf"(?=\Z)", # Tangkap semua konten (non-greedy)
        re.IGNORECASE | re.DOTALL | re.MULTILINE # DOTALL untuk [\s\S] mencakup \n, MULTILINE untuk ^
    )
        
    for block_match in summary_block_regex.finditer(cv_text):
        summary_block_content = block_match.group('education_block')
        
        if summary_block_content:
            # 2. Ambil semua baris ke dalam list of string
            lines_in_block = [line.strip() for line in summary_block_content.splitlines() if line.strip()] # Ambil hanya baris non-kosong
            return lines_in_block[0]
    
    return None

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
        "education": extract_content_after_education(cv_text)
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