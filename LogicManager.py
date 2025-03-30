import itertools
import string
import time


class LogicManager:
    def __init__(self, has_numbers, has_uppercase, has_lowercase, has_special_chars, attack_method, target_password, update_ui, update_test):
        self.has_numbers = has_numbers
        self.has_uppercase = has_uppercase
        self.has_lowercase = has_lowercase
        self.has_special_chars = has_special_chars
        self.attack_method = attack_method
        self.target_password = target_password
        self.update_ui = update_ui
        self.update_test = update_test
        self.cancel_test = False

    def run_test(self):
        print(f"Criteria: Numbers: {self.has_numbers}, Uppercase: {self.has_uppercase}, Lowercase: {self.has_lowercase}, Special: {self.has_special_chars}")
        print(f"Attack Method: {self.attack_method}")
        print(f"Password: {self.target_password}")

        if self.attack_method == "Brute Force":
            self.brute_force(self.target_password)
        elif self.attack_method == "Dictionary":
            self.dictionary_attack(self.target_password)
        elif self.attack_method == "Combined":
            self.combined_attack()


    def end_test(self):
        self.cancel_test = True
        self.update_test()

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
            while not self.cancel_test:
                for attempt in itertools.product(charset, repeat=length):
                    if self.cancel_test:
                        print("Przerwano brute force.")
                        return
                    tested_count += 1
                    elapsed_time = time.time() - start_time
                    self.update_ui(tested_count, elapsed_time, ''.join(attempt))
                    yield ''.join(attempt)
                length += 1

        for attempt in password_generator():
            print(f"Próba: {attempt}")

            if attempt == target_password:
                print(f"Znaleziono hasło: {attempt}")
                self.end_test()
                return attempt

        return None

    def dictionary_attack(self, target_password):
        start_time = time.time()
        tested_count = 0

        with open("psswd1M.txt", "r", encoding="utf-8") as file:
            for line in file:
                if self.cancel_test:
                    print("Przerwano atak słownikowy.")
                    self.end_test()
                    return
                attempt = line.strip()
                tested_count += 1   
                elapsed_time = time.time() - start_time
                self.update_ui(tested_count, elapsed_time, attempt)

                print(f"Próba: {attempt}")
                if attempt == target_password:
                    print(f"Znaleziono hasło: {attempt}")
                    self.end_test()
                    return attempt

        print("Hasła nie znaleziono.")
        self.update_ui(tested_count, elapsed_time, 'Password Not Found')
        self.end_test()
        return None

    def dictionary_generator(self):
        with open("psswd1M.txt", "r", encoding="utf-8") as file:
            for line in file:
                yield line.strip()

    def common_modifications(self, base_password):
        if self.has_numbers:
            for i in range(1, 3):
                for digits in itertools.product(string.digits, repeat=i):
                    yield base_password + ''.join(digits)

        if self.has_special_chars:
            common_symbols = ["!", "?", "@", "#", "$"]
            for sym in common_symbols:
                yield base_password + sym

        if self.has_numbers:
            leet_map = str.maketrans("aAeEiIoOsS", "4433110055")
            leet_version = base_password.translate(leet_map)
            if leet_version != base_password:
                yield leet_version

        if len(base_password) > 1:
            yield base_password + base_password[-1]

        if self.has_uppercase and self.has_lowercase and base_password[0].islower():
            yield base_password.capitalize()

    def combined_attack(self):
        start_time = time.time()
        tested_count = 0

        for word in self.dictionary_generator():
            if self.cancel_test:
                return
            tested_count += 1
            self.update_ui(tested_count, time.time() - start_time, word)
            if word == self.target_password:
                print(f"Znaleziono hasło: {word}")
                self.end_test()
                return

            for variant in self.common_modifications(word):
                if self.cancel_test:
                    return
                tested_count += 1
                self.update_ui(tested_count, time.time() - start_time, variant)
                if variant == self.target_password:
                    print(f"Znaleziono hasło: {variant}")
                    self.end_test()
                    return

        print("Hasło nie zostało znalezione.")
        self.end_test()

