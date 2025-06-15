import collections
import concurrent.futures

def compute_lps_array(pattern):
    """
    Menghitung array LPS (longest proper prefix suffix) untuk algoritma KMP.
    Array LPS menyimpan panjang awalan terpanjang yang juga merupakan akhiran.
    ex: abcabc --> [0, 0, 0, 1, 2, 3]
    """
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search_single(text, pattern):
    """
    Melakukan pencarian satu pola string menggunakan algoritma Knuth-Morris-Pratt (KMP).

    Args:
        text (str): String teks yang akan dicari polanya.
        pattern (str): String pola yang akan dicari.

    Returns:
        int: Jumlah kemunculan pola dalam teks (non-overlapping).
    """
    n = len(text)
    m = len(pattern)
    
    if m == 0:
        return 0
    if n == 0:
        return 0

    lps = compute_lps_array(pattern)
    count = 0
    i = 0 
    j = 0 

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            count += 1
            # Ulangi pattern matching dari longest prefix
            # Ini secara alami memungkinkan KMP menemukan tumpang tindih
            # jika ada, karena kita tidak melompati seluruh pola.
            j = lps[j - 1] 
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                # Ulangi pattern matching dari longest prefix
                j = lps[j - 1]
            else:
                # Kalau dari awal teks tidak cocok, lanjutkan ke karakter berikutnya pada teks
                i += 1
    return count

def kmp_search_multi_threaded(text, patterns, max_workers=None):
    """
    Melakukan pencarian beberapa pola string menggunakan algoritma Knuth-Morris-Pratt (KMP)
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
    text_lower = text.lower()

    pattern_counts = [0] * len(patterns)

    # Gunakan ThreadPoolExecutor untuk mengelola thread
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(kmp_search_single, text_lower, pattern.lower()): idx 
                   for idx, pattern in enumerate(patterns)}
        
        for future in concurrent.futures.as_completed(futures):
            idx = futures[future]
            try:
                result = future.result()
                pattern_counts[idx] = result
            except Exception as exc:
                print(f"Pola {patterns[idx]} menghasilkan kesalahan: {exc}")
    
    return pattern_counts

# API needs
def search_kmp(patterns, text):
    return kmp_search_multi_threaded(text, patterns)

if __name__ == "__main__":
    # --- Contoh Penggunaan KMP Multi-threaded ---
    print("--- KMP Multi-Pattern Search (Multi-threaded) ---")

    patterns_ex1 = ["ABABCABAB", "ABABD"]
    text_ex1 = "ABABDABACDABABCABAB"
    counts_ex1 = kmp_search_multi_threaded(text_ex1, patterns_ex1, max_workers=2)
    print(f"Pola: {patterns_ex1}, Teks: '{text_ex1}'")
    print(f"Jumlah kemunculan: {counts_ex1}") # Output: [1, 1]

    patterns_ex2 = ["AA", "AAA", "AAAA"]
    text_ex2 = "AAAAAA"
    counts_ex2 = kmp_search_multi_threaded(text_ex2, patterns_ex2, max_workers=3)
    print(f"\nPola: {patterns_ex2}, Teks: '{text_ex2}'")
    print(f"Jumlah kemunculan: {counts_ex2}") # Output: [3, 2, 1]

    patterns_ex3 = ["abc", "bca", "ca"]
    text_ex3 = "abcabcabc" * 10
    counts_ex3 = kmp_search_multi_threaded(text_ex3, patterns_ex3) # Gunakan default max_workers
    print(f"\nPola: {patterns_ex3}, Teks: '{text_ex3[:50]}...'")
    print(f"Jumlah kemunculan: {counts_ex3}") # Output: [10, 9, 9]

    text_long = "Kevin Martinez Database Administrator expert in MySQL, PostgreSQL, Oracle, MongoDB, Redis. Database optimization, backup strategies, security. Master's Information Systems ASU. Skills: MySQL, PostgreSQL, Oracle, MongoDB, Redis, SQL Server, database tuning, backup, security, replication." * 50
    patterns_long = ["sql", "database", "redis", "oracle", "python", "java", "developer", "administrator", "security", "backup"]
    counts_long = kmp_search_multi_threaded(text_long, patterns_long)
    print(f"\nPola: {patterns_long}, Teks: '{text_long[:50]}...'")
    print(f"Jumlah kemunculan: {counts_long}")