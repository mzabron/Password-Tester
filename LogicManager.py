import itertools
import string


class LogicManager:
    def __init__(self, has_numbers, has_uppercase, has_lowercase, has_special_chars, hash_password, hash_method, attack_method, target_password):
        self.has_numbers = has_numbers
        self.has_uppercase = has_uppercase
        self.has_lowercase = has_lowercase
        self.has_special_chars = has_special_chars
        self.hash_password = hash_password
        self.hash_method = hash_method
        self.attack_method = attack_method
        self.target_password = target_password

    def run_test(self):
        print(f"Criteria: Numbers: {self.has_numbers}, Uppercase: {self.has_uppercase}, Lowercase: {self.has_lowercase}, Special: {self.has_special_chars}")
        print(f"Hashing: {self.hash_password}, Hash Method: {self.hash_method}, Attack Method: {self.attack_method}")
        print(f"Password: {self.target_password}")

