class Encryption:
    """
    1. Caesar cipher shift 47
    2. Character position swapping (last - first, second-last - second, etc.)
    """
    
    def __init__(self):
        # printable ASCII characters (32-126)
        self.charset = ''.join(chr(i) for i in range(32, 127))
        self.charset_size = len(self.charset)
        self.shift = 47

    def _caesar_encrypt(self, text: str) -> str:
        result = ""
        for char in text:
            if char == '-':
                result += char
            elif char in self.charset:
                old_index = self.charset.index(char)
                new_index = (old_index + self.shift) % self.charset_size
                result += self.charset[new_index]
            else:
                result += char
        return result
    
    def _caesar_decrypt(self, text: str) -> str:
        result = ""
        for char in text:
            if char == '-':
                result += char
            elif char in self.charset:
                old_index = self.charset.index(char)
                new_index = (old_index - self.shift) % self.charset_size
                result += self.charset[new_index]
            else:
                result += char
        return result
    
    def _swap_positions(self, text: str) -> str:
        if len(text) <= 1:
            return text
        
        text_list = list(text)
        length = len(text_list)
        
        for i in range(length // 2):
            left_index = i
            right_index = length - 1 - i
            
            text_list[left_index], text_list[right_index] = text_list[right_index], text_list[left_index] # swap
        
        return ''.join(text_list)
    
    def _encrypt_date(self, date_str: str) -> str:
        if not date_str or '-' not in date_str:
            return date_str
        try:
            parts = date_str.split('-')
            if len(parts) != 3:
                return date_str
            
            year, month, day = parts
            
            # tahun dibalik
            encrypted_year = year[::-1]

            # bulan dishift 4
            month_int = int(month)

            encrypted_month_int = ((month_int - 1 + 4) % 12) + 1
            encrypted_month = f"{encrypted_month_int:02d}"
            
            # hari dishift 7
            day_int = int(day)
            encrypted_day_int = ((day_int - 1 + 7) % 28) + 1
            encrypted_day = f"{encrypted_day_int:02d}"
            
            return f"{encrypted_year}-{encrypted_month}-{encrypted_day}"
        except:
            return date_str
    
    def _decrypt_date(self, encrypted_date: str) -> str:
        if not encrypted_date or '-' not in encrypted_date:
            return encrypted_date
        
        try:
            parts = encrypted_date.split('-')
            if len(parts) != 3:
                return encrypted_date
            
            year, month, day = parts
        
            decrypted_year = year[::-1]

            month_int = int(month)
            decrypted_month_int = ((month_int - 1 - 4) % 12) + 1
            decrypted_month = f"{decrypted_month_int:02d}"

            day_int = int(day)
            decrypted_day_int = ((day_int - 1 - 7) % 28) + 1
            decrypted_day = f"{decrypted_day_int:02d}"
            
            return f"{decrypted_year}-{decrypted_month}-{decrypted_day}"
        except:
            return encrypted_date

    def encrypt(self, plaintext: str) -> str:
        """
        1. Apply caesar cipher (shift 47)
        2. Swap character positions
        """
        if not plaintext:
            return ""
        
        result = self._caesar_encrypt(plaintext)
        result = self._swap_positions(result)
        
        return result
    
    def decrypt(self, ciphertext: str) -> str:
        """
        1. Reverse character position swapping
        2. Reverse caesar cipher
        """
        if not ciphertext:
            return ""

        result = self._swap_positions(ciphertext)
        result = self._caesar_decrypt(result)
        
        return result

    def encrypt_date(self, date_str: str) -> str:
        """
        Special encryption untuk date fields
        """
        if not date_str:
            return ""
        return self._encrypt_date(date_str)
    
    def decrypt_date(self, encrypted_date: str) -> str:
        """
        Special decryption untuk date fields
        """
        if not encrypted_date:
            return ""
        return self._decrypt_date(encrypted_date)

_encryption_instance = None

def get_encryption_instance() -> Encryption:
    global _encryption_instance
    if _encryption_instance is None:
        _encryption_instance = Encryption()
    return _encryption_instance

def encrypt(data: str) -> str:
    if not data:
        return ""
    return get_encryption_instance().encrypt(data)

def decrypt(encrypted_data: str) -> str:
    if not encrypted_data:
        return ""
    return get_encryption_instance().decrypt(encrypted_data)

def encrypt_date(date_str: str) -> str:
    if not date_str:
        return ""
    return get_encryption_instance().encrypt_date(date_str)

def decrypt_date(encrypted_date: str) -> str:
    if not encrypted_date:
        return ""
    return get_encryption_instance().decrypt_date(encrypted_date)