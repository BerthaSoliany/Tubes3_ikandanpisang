import re

class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        # Inisialisasi cache dengan nilai infinity
        cache = [[float("inf")] * (len(word2) + 1) for _ in range(len(word1) + 1)]

        # Baris terakhir: mengubah word1 menjadi string kosong
        for j in range(len(word2) + 1):
            cache[len(word1)][j] = len(word2) - j
        
        # Kolom terakhir: mengubah string kosong menjadi word2
        for i in range(len(word1) + 1):
            cache[i][len(word2)] = len(word1) - i

        # Mengisi tabel cache dari bawah ke atas (bottom-up) dan kanan ke kiri
        for i in range(len(word1) - 1, -1, -1):
            for j in range(len(word2) - 1, -1, -1):
                if word1[i] == word2[j]:
                    cache[i][j] = cache[i + 1][j + 1]
                else:
                    cache[i][j] = 1 + min(cache[i + 1][j], cache[i][j + 1], cache[i + 1][j + 1])
        
        # Hasil akhir ada di cache[0][0]
        return cache[0][0]
    
    def countThreshold(self, word: str) -> int:
        """
        Menghitung threshold untuk jarak Levenshtein.
        Threshold adalah panjang string dibagi 2, dibulatkan ke atas.
        """
        length = len(word)
        if length <= 3:
            return 0  # Kata sangat pendek, harus persis sama (jarak 0)
        elif 3 < length <= 6:
            return 1
        elif 6 < length <= 10:
            return 2
        else:
            return 3
        
    def countFuzzy(self, pattern, text) -> int:
        threshold = self.countThreshold(pattern)
        fuzzy_count = 0

        pattern_lower = pattern.lower()
        text_lower = text.lower()

        # Menggunakan regex untuk memisahkan kata-kata (mengabaikan tanda baca, spasi, newline, dll.)
        words_in_text = re.findall(r'\b\w+\b', text_lower)

        for word_in_cv in words_in_text:
            distance = self.minDistance(pattern_lower, word_in_cv)
            if distance <= threshold:
                fuzzy_count += 1
                
        return fuzzy_count

# API needs
def count_fuzzy(pattern, text):
    """
    Fungsi untuk menghitung jumlah fuzzy match dari pattern dalam teks.
    Ini adalah fungsi pembungkus untuk memudahkan penggunaan.
    """
    sol = Solution()
    return sol.countFuzzy(pattern, text)

if __name__ == "__main__":

    # Inisialisasi objek Solution
    sol = Solution()

    text1 = "Saya suka python, dan belajar pyhton di kampus."
    pattern1 = "python"
    fuzzy_matches1 = sol.countFuzzy(pattern1, text1)
    print(f"Pola '{pattern1}' dalam '{text1}': {fuzzy_matches1} fuzzy match") 

    text2 = "Administratr dan sekertaris adalah posisi yang berbeda."
    pattern2_a = "administrator"
    pattern2_b = "sekretaris"
    fuzzy_matches2_a = sol.countFuzzy(pattern2_a, text2)
    fuzzy_matches2_b = sol.countFuzzy(pattern2_b, text2)
    print(f"Pola '{pattern2_a}' dalam '{text2}': {fuzzy_matches2_a} fuzzy match") # Diharapkan: 1 (Administratr)
    print(f"Pola '{pattern2_b}' dalam '{text2}': {fuzzy_matches2_b} fuzzy match") # Diharapkan: 1 (sekertaris)