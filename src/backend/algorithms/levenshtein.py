class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        # Inisialisasi cache (tabel DP) dengan nilai 'inf' (infinity)
        # Ukuran tabel adalah (len(word1) + 1) x (len(word2) + 1)
        cache = [[float("inf")] * (len(word2) + 1) for _ in range(len(word1) + 1)]

        # Mengisi baris terakhir dan kolom terakhir dari tabel cache
        # Ini adalah kasus dasar: mengubah string kosong menjadi string non-kosong
        # atau sebaliknya.
        # Baris terakhir: mengubah word1 menjadi string kosong (hapus semua karakter)
        for j in range(len(word2) + 1):
            cache[len(word1)][j] = len(word2) - j
        
        # Kolom terakhir: mengubah string kosong menjadi word2 (sisipkan semua karakter)
        for i in range(len(word1) + 1):
            cache[i][len(word2)] = len(word1) - i

        # Mengisi tabel cache dari bawah ke atas (bottom-up) dan kanan ke kiri
        # Melakukan iterasi mundur dari akhir string
        for i in range(len(word1) - 1, -1, -1):
            for j in range(len(word2) - 1, -1, -1):
                # Jika karakter saat ini cocok
                if word1[i] == word2[j]:
                    # Tidak ada biaya, ambil nilai dari diagonal (karakter berikutnya)
                    cache[i][j] = cache[i + 1][j + 1]
                else:
                    # Jika karakter tidak cocok, ambil minimum dari 3 operasi + 1 (biaya operasi)
                    # 1. Penghapusan (delete): cache[i + 1][j] -> hapus word1[i]
                    # 2. Penyisipan (insert): cache[i][j + 1] -> sisipkan karakter di word1[i] untuk match word2[j]
                    # 3. Substitusi (replace): cache[i + 1][j + 1] -> ganti word1[i] dengan word2[j]
                    cache[i][j] = 1 + min(cache[i + 1][j], cache[i][j + 1], cache[i + 1][j + 1])
        
        # Hasil akhir ada di cache[0][0], yaitu jarak Levenshtein antara seluruh word1 dan word2
        return cache[0][0]

# --- Contoh Penggunaan ---

# Inisialisasi objek Solution
sol = Solution()

# Contoh 1
word1_1 = "horse"
word2_1 = "ros"
distance_1 = sol.minDistance(word1_1, word2_1)
print(f"Jarak Levenshtein antara '{word1_1}' dan '{word2_1}': {distance_1}") # Output: 3

# Contoh 2
word1_2 = "intention"
word2_2 = "execution"
distance_2 = sol.minDistance(word1_2, word2_2)
print(f"Jarak Levenshtein antara '{word1_2}' dan '{word2_2}': {distance_2}") # Output: 5

# Contoh 3
word1_3 = "saturday"
word2_3 = "sunday"
distance_3 = sol.minDistance(word1_3, word2_3)
print(f"Jarak Levenshtein antara '{word1_3}' dan '{word2_3}': {distance_3}") # Output: 3

# Contoh 4 (kasus string kosong)
word1_4 = ""
word2_4 = "abc"
distance_4 = sol.minDistance(word1_4, word2_4)
print(f"Jarak Levenshtein antara '{word1_4}' dan '{word2_4}': {distance_4}") # Output: 3

# Contoh 5 (kasus string sama)
word1_5 = "apple"
word2_5 = "apple"
distance_5 = sol.minDistance(word1_5, word2_5)
print(f"Jarak Levenshtein antara '{word1_5}' dan '{word2_5}': {distance_5}") # Output: 0