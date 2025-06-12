import collections
import concurrent.futures # Untuk ThreadPoolExecutor

# --- Fungsi build_last dan bm_search_single tetap sama ---
def build_last(pattern):
    """
    Membangun tabel kemunculan terakhir (last occurrence) untuk algoritma Boyer-Moore.
    """
    last = [-1] * 128
    for i in range(len(pattern)):
        last[ord(pattern[i])] = i
    return last

def bm_search_single(text, pattern):
    """
    Melakukan pencarian satu pola string menggunakan algoritma Boyer-Moore (non-overlapping).
    """
    # Catatan: lowercase sudah diasumsikan dilakukan di level panggilan multi-thread
    # atau di fungsi pemanggil `bm_search_multi_threaded`
    n = len(text)
    m = len(pattern)
    
    if m == 0:
        return 0 
    if n == 0:
        return 0 
    if m > n:
        return 0

    last = build_last(pattern) 
    count = 0 
    i = m - 1
    
    if i > n - 1:
        return 0

    while i < n:
        j = m - 1 
        k = i       

        while j >= 0 and text[k] == pattern[j]:
            k -= 1 
            j -= 1 

        if j < 0:
            count += 1 
            i += m 
        else:
            text_char = text[k]
            lo = last[ord(text_char)] if ord(text_char) < 128 else -1
            shift = max(1, j - lo)
            i += shift 

    return count

# --- Fungsi Multi-Threading Boyer-Moore ---
def bm_search(text, patterns, max_workers=None):
    """
    Melakukan pencarian beberapa pola string menggunakan algoritma Boyer-Moore (non-overlapping)
    dengan multithreading.

    Args:
        text (str): String teks yang akan dicari polanya.
        patterns (list[str]): List string pola yang akan dicari.
        max_workers (int, optional): Jumlah thread maksimum yang akan digunakan. 
                                      Jika None, default-nya adalah jumlah CPU.

    Returns:
        list[int]: Array of integer, di mana setiap elemen adalah jumlah kemunculan
                   dari pola yang sesuai (berdasarkan indeks `patterns` input).
    """
    text_lower = text.lower() # Ubah teks ke lowercase sekali saja

    # Inisialisasi array untuk menyimpan hitungan kemunculan untuk setiap pola
    # Akan diisi secara asinkron oleh thread
    pattern_counts = [0] * len(patterns)

    # Gunakan ThreadPoolExecutor untuk mengelola thread
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Peta setiap pola ke fungsi pencarian tunggal yang akan dijalankan oleh thread
        # `executor.submit` mengembalikan objek Future
        futures = {executor.submit(bm_search_single, text_lower, pattern.lower()): idx 
                   for idx, pattern in enumerate(patterns)}
        
        # Iterasi melalui hasil saat mereka selesai
        for future in concurrent.futures.as_completed(futures):
            idx = futures[future] # Dapatkan indeks pola asli
            try:
                result = future.result() # Dapatkan hasil (jumlah kemunculan) dari thread
                pattern_counts[idx] = result
            except Exception as exc:
                print(f"Pola {patterns[idx]} menghasilkan kesalahan: {exc}")
    
    return pattern_counts

# API needs
def search_bm(patterns, text):
    return bm_search(text, patterns)

# --- Contoh Penggunaan ---

if __name__ == "__main__":
    print("--- Boyer-Moore Multi-Pattern Search (Multi-threaded) ---")

    patterns_ex1 = ["TEST", "THIS"]
    text_ex1 = "THIS IS A TEST TEXT"
    counts_ex1 = bm_search(text_ex1, patterns_ex1, max_workers=2)
    print(f"Pola: {patterns_ex1}, Teks: '{text_ex1}'")
    print(f"Jumlah kemunculan: {counts_ex1}")

    patterns_ex2 = ["COAL", "MY", "ME", "WELCOME", "LISION"]
    text_ex2 = "WELCOMETOMYCOALLISION"
    counts_ex2 = bm_search(text_ex2, patterns_ex2, max_workers=3)
    print(f"\nPola: {patterns_ex2}, Teks: '{text_ex2}'")
    print(f"Jumlah kemunculan: {counts_ex2}")

    patterns_ex3 = ["GEEKS", "FOR", "APPLE", "BANANA", "ORANGE"]
    text_ex3 = "GEEKSFORGEEKS AND SOME OTHER WORDS LIKE APPLE BANANA" * 10 # Teks lebih panjang untuk simulasi
    counts_ex3 = bm_search(text_ex3, patterns_ex3) # Gunakan default max_workers
    print(f"\nPola: {patterns_ex3}, Teks: '{text_ex3[:50]}...'")
    print(f"Jumlah kemunculan: {counts_ex3}")

    text_long = "Kevin Martinez Database Administrator expert in MySQL, PostgreSQL, Oracle, MongoDB, Redis. Database optimization, backup strategies, security. Master's Information Systems ASU. Skills: MySQL, PostgreSQL, Oracle, MongoDB, Redis, SQL Server, database tuning, backup, security, replication." * 100
    patterns_long = ["sql", "database", "redis", "oracle", "python", "java", "developer", "administrator", "security", "backup"]
    counts_long = bm_search(text_long, patterns_long)
    print(f"\nPola: {patterns_long}, Teks: '{text_long[:50]}...'")
    print(f"Jumlah kemunculan: {counts_long}")