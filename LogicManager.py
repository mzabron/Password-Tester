import itertools
import string
import time


class LogicManager:
    def __init__(self, has_numbers, has_uppercase, has_lowercase, has_special_chars, hash_password, hash_method, attack_method, target_password, update_ui):
        self.has_numbers = has_numbers
        self.has_uppercase = has_uppercase
        self.has_lowercase = has_lowercase
        self.has_special_chars = has_special_chars
        self.hash_password = hash_password
        self.hash_method = hash_method
        self.attack_method = attack_method
        self.target_password = target_password
        self.update_ui = update_ui

    def run_test(self):
        print(f"Criteria: Numbers: {self.has_numbers}, Uppercase: {self.has_uppercase}, Lowercase: {self.has_lowercase}, Special: {self.has_special_chars}")
        print(f"Hashing: {self.hash_password}, Hash Method: {self.hash_method}, Attack Method: {self.attack_method}")
        print(f"Password: {self.target_password}")

        if self.attack_method == "Brute Force":
            self.brute_force(self.target_password)
        elif self.attack_method == "Dictionary":
            self.dictionary_attack(self.target_password)

    def brute_force(self, target_password):
        charset = ""
        if self.has_numbers:
            charset += string.digits
        if self.has_uppercase:
            charset += string.ascii_uppercase
        if self.has_lowercase:
            charset += string.ascii_lowercase
        if self.has_special_chars:
            charset += string.punctuation

        print(f"Zastosowany charset: {charset}")

        def password_generator():
            length = 1
            start_time = time.time()
            tested_count = 0
            while True:
                for attempt in itertools.product(charset, repeat=length):
                    tested_count += 1
                    elapsed_time = time.time() - start_time
                    self.update_ui(tested_count, elapsed_time, ''.join(attempt))
                    yield ''.join(attempt)
                length += 1

        for attempt in password_generator():
            print(f"Próba: {attempt}")

            if attempt == target_password:
                print(f"Znaleziono hasło: {attempt}")
                return attempt

        return None

    def dictionary_attack(self, target_password):
        start_time = time.time()
        tested_count = 0

        with open("psswd1M.txt", "r", encoding="utf-8") as file:
            for line in file:
                attempt = line.strip()
                tested_count += 1
                elapsed_time = time.time() - start_time
                self.update_ui(tested_count, elapsed_time, ''.join(attempt))

                print(f"Próba: {attempt}")
                if attempt == target_password:
                    print(f"Znaleziono hasło: {attempt}")
                    return attempt

        print("Hasła nie znaleziono.")
        self.update_ui(tested_count, elapsed_time,'Password Not Found')
        return None
