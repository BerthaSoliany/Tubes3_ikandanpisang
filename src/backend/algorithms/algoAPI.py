from aho_corasick import search_aho
from boyer_moore import search_bm
from kmp import search_kmp
import time

patterns = ["he", "she", "his", "hers"]
text = "ushers"

def stringMatching(patterns, text, switch):
    if (switch < 0 or switch > 2):
        raise ValueError("Invalid switch value. Use 0 for KMP, 2 for Boyer-Moore, or 3 for Aho-Corasick.")
        return None
    
    start_time = time.perf_counter()
    match switch:
        case 0:
            res = search_kmp(patterns, text)
        case 1:
            res = search_bm(patterns, text)
        case 2:
            res = search_aho(patterns, text)
        case _:
            return None
    end_time = time.perf_counter()

    print(f"Result: {res}")
    print(f"Execution time: {end_time - start_time:.2f} seconds")
    return None

if __name__ == "__main__":
    stringMatching(patterns, text, 2)  # Ganti switch sesuai kebutuhan