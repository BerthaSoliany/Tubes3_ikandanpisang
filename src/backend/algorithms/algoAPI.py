from .aho_corasick import search_aho
from .boyer_moore import search_bm
from .kmp import search_kmp
from .levenshtein import count_fuzzy

import concurrent.futures
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from src.backend.utils.pdf_extract import extract_pdfs

def stringMatching(patterns: list[str], algorithm: int):
    if not (0 <= algorithm <= 2):
        raise ValueError("Invalid algorithm value. Use 0 for KMP, 1 for Boyer-Moore, or 2 for Aho-Corasick.")
    
    # dir_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', '11152490.pdf')

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
    data_dir = os.path.join(project_root, 'data')
    
    if not os.path.exists(data_dir):
        print(f"Folder data tidak ditemukan: {data_dir}")
        return None
    print(f"Mengekstrak PDF dari direktori: {data_dir}")
    dict_of_cv_texts = extract_pdfs(data_dir, max_workers=os.cpu_count()) 
    
    if not dict_of_cv_texts:
        print("Tidak ada teks CV yang berhasil diekstrak. Menghentikan proses.")
        return None

    print(f"Berhasil mengekstrak {len(dict_of_cv_texts)} CV.")

    search_algorithm_func = None
    if algorithm == 0:
        search_algorithm_func = search_kmp
    elif algorithm == 1:
        search_algorithm_func = search_bm
    else:
        search_algorithm_func = search_aho 
    
    # --- exact matching ---
    print("Memulai pencarian exact matching...")
    results_per_cv_akumulatif = {}
    exact_cv_processed_count = 0

    start_exact_time = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        def _run_exact_search_on_cv(cv_item_tuple):
            cv_name, cv_text = cv_item_tuple
            exact_counts_for_patterns = search_algorithm_func(patterns, cv_text)
            return cv_name, exact_counts_for_patterns

        exact_futures = [executor.submit(_run_exact_search_on_cv, item) 
                         for item in dict_of_cv_texts.items()]

        for future in concurrent.futures.as_completed(exact_futures):
            exact_cv_processed_count += 1 
            cv_path, exact_counts_for_current_cv = future.result()
            
            # Inisialisasi entri untuk CV ini di results
            results_per_cv_akumulatif[cv_path] = {
                "counter": [0] * len(patterns), 
                "match_flags": [0] * len(patterns),
            }
            
            # Akumulasikan hasil exact untuk CV ini ke struktur data per CV
            for i, count in enumerate(exact_counts_for_current_cv):
                results_per_cv_akumulatif[cv_path]["counter"][i] = count 
                if count > 0:
                    results_per_cv_akumulatif[cv_path]["match_flags"][i] = 1
    
    end_exact_time = time.perf_counter()
    exact_time = end_exact_time - start_exact_time 

    print(f"Exact matching selesai. {exact_cv_processed_count} CVs diproses dalam {exact_time:.4f} detik.")
    
    # --- fuzzy matching ---
    print("Memulai pencarian fuzzy matching...")
    fuzzy_cv_processed_count = 0 
    all_fuzzy_tasks = [] 
    
    start_fuzzy_time = time.perf_counter()

    for cv_path, cv_text in dict_of_cv_texts.items():
        needs_fuzzy_processing_for_this_cv = False
        
        # Tentukan pola mana yang perlu di-fuzzy untuk CV ini
        patterns_for_fuzzy_this_cv = []
        for i in range(len(patterns)):
            if results_per_cv_akumulatif[cv_path]["counter"][i] == 0:
                patterns_for_fuzzy_this_cv.append(patterns[i])
                needs_fuzzy_processing_for_this_cv = True
        
        if needs_fuzzy_processing_for_this_cv:
            fuzzy_cv_processed_count += 1

            for pattern_item in patterns_for_fuzzy_this_cv:
                all_fuzzy_tasks.append((cv_path, pattern_item, cv_text))

    if all_fuzzy_tasks:
        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as fuzzy_executor:
            def _run_fuzzy_search_on_single_pattern_in_cv(task_tuple):
                cv_path, pattern_item, cv_text = task_tuple
                fuzzy_count_for_pattern = count_fuzzy(pattern_item, cv_text)
                return cv_path, pattern_item, fuzzy_count_for_pattern
            
            fuzzy_futures = [fuzzy_executor.submit(_run_fuzzy_search_on_single_pattern_in_cv, task) for task in all_fuzzy_tasks]
            
            for future in concurrent.futures.as_completed(fuzzy_futures):
                cv_path, fuzzy_pattern, fuzzy_count_for_pattern = future.result()
                
                if fuzzy_count_for_pattern > 0:
                    idx = patterns.index(fuzzy_pattern)
                    results_per_cv_akumulatif[cv_path]["counter"][idx] = fuzzy_count_for_pattern
                    results_per_cv_akumulatif[cv_path]["match_flags"][i] = 2

    end_fuzzy_time = time.perf_counter()
    fuzzy_time = end_fuzzy_time - start_fuzzy_time
    print(f"Fuzzy matching selesai. {fuzzy_cv_processed_count} CVs diproses dalam {fuzzy_time:.4f} detik.")

    # --- final output ---
    print("Menyusun hasil akhir...")
    final_output_results = {}
    for cv_path, data in results_per_cv_akumulatif.items():
        final_output_results[cv_path] = (
            data["counter"],
            data["match_flags"]
        )
    
    return (final_output_results, exact_time, fuzzy_time, exact_cv_processed_count, fuzzy_cv_processed_count, dict_of_cv_texts)

if __name__ == "__main__":
    patterns = ["sales", "Schedulang"]
    (final_output_results, exact_time, fuzzy_time, exact_cv_processed_count, fuzzy_cv_processed_count, dict_of_cv_texts) = stringMatching(patterns, 1)

    print("\n--- Ringkasan Hasil per CV ---")
    for cv_path, res_tuple in final_output_results.items():
        print(f"CV: {cv_path}")
        print(f"  Total Counts per Pattern: {res_tuple[0]}")
        print(f"  Match Flags (Exact OR Fuzzy): {res_tuple[1]} (Corresponding to patterns: {patterns})")

    print(f"\nGlobal Summary:")
    print(f"Exact matching time: {exact_time:.4f} seconds, CVs processed: {exact_cv_processed_count}")
    print(f"Fuzzy matching time: {fuzzy_time:.4f} seconds, CVs processed: {fuzzy_cv_processed_count}")