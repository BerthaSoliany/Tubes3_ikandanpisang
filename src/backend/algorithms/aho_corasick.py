import collections

class TrieNode:
    def __init__(self):
        self.children = {}  # Kamus untuk menyimpan transisi karakter ke node anak
        self.output = []    # Daftar indeks pola yang berakhir di node ini
        self.failure_link = None # Link kegagalan (akan diatur nanti)
        self.parent = None  # Parent node (digunakan untuk membangun failure links)
        self.char_from_parent = None # Karakter dari parent ke node ini

class AhoCorasick:
    def __init__(self, patterns):
        self.root = TrieNode()
        self.patterns = patterns
        self._build_trie()
        self._build_failure_links()

    def _build_trie(self):
        """
        Membangun struktur Trie dari semua pola yang diberikan (Fase Go-to).
        """
        for i, pattern in enumerate(self.patterns):
            current_node = self.root
            for char in pattern:
                if char not in current_node.children:
                    new_node = TrieNode()
                    new_node.parent = current_node
                    new_node.char_from_parent = char
                    current_node.children[char] = new_node
                current_node = current_node.children[char]
            current_node.output.append(i) # Tambahkan indeks pola ke node akhir

    def _build_failure_links(self):
        """
        Membangun failure links untuk setiap node dalam Trie menggunakan BFS.
        """
        queue = collections.deque()

        # Atur failure link untuk anak-anak root ke root itu sendiri
        for char, child_node in self.root.children.items():
            child_node.failure_link = self.root
            queue.append(child_node)

        while queue:
            current_node = queue.popleft()

            # Untuk setiap anak dari current_node
            for char, next_node in current_node.children.items():
                # Cari failure link untuk next_node
                # Dimulai dari failure link dari current_node
                failure_state = current_node.failure_link

                # Cari di sepanjang failure links sampai menemukan karakter yang cocok
                while failure_state is not None and char not in failure_state.children:
                    if failure_state == self.root: # Jika sudah kembali ke root dan tidak ada transisi
                        failure_state = None # Berarti tidak ada failure link yang cocok selain root
                        break
                    failure_state = failure_state.failure_link

                if failure_state is None: # Jika tidak ditemukan, arahkan ke root
                    next_node.failure_link = self.root
                else: # Jika ditemukan, arahkan ke anak dari failure_state dengan karakter yang sama
                    next_node.failure_link = failure_state.children[char]
                
                # Warisi output dari failure link
                # Ini penting agar pola yang ditemukan melalui failure link juga dilaporkan
                next_node.output.extend(next_node.failure_link.output)

                queue.append(next_node)

    def search(self, text):
        """
        Mencari semua kemunculan pola dalam teks menggunakan automaton Aho-Corasick
        dan mengembalikan array of integer yang berkorelasi dengan jumlah kemunculan
        setiap pola sesuai dengan urutan pola yang diberikan.

        Args:
            text (str): Teks input yang akan dipindai.

        Returns:
            list: Array of integer, di mana setiap elemen adalah jumlah kemunculan
                  dari pola yang sesuai (berdasarkan indeks `self.patterns`).
        """
        # Inisialisasi array untuk menyimpan hitungan kemunculan untuk setiap pola
        # Ukurannya sama dengan jumlah pola, dan semua nilai dimulai dari 0
        pattern_counts = [0] * len(self.patterns)
        
        current_state = self.root

        for i, char in enumerate(text):
            # Ikuti transisi atau failure links
            while current_state is not None and char not in current_state.children:
                if current_state == self.root:
                    current_state = None
                    break
                current_state = current_state.failure_link

            if current_state is None:
                current_state = self.root
            else:
                current_state = current_state.children[char]

            # Periksa apakah ada pola yang berakhir di node saat ini atau melalui failure link
            for pattern_idx in current_state.output:
                # Tambahkan hitungan untuk pola yang sesuai
                pattern_counts[pattern_idx] += 1
        
        return pattern_counts

# API needs
def search_aho(patterns, text):
    ac_automaton = AhoCorasick(patterns)
    return ac_automaton.search(text)

# --- Contoh Penggunaan ---

if __name__ == "__main__":
    patterns = ["he", "she", "his", "hers"]
    text = "ushers"
    print(f"hasil dari search_aho: {search_aho(patterns, text)}")