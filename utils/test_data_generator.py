import random
import string


class TestDataGenerator:
    """Генератор тестовых данных для автотестов"""

    @staticmethod
    def generate_post_code():
        """Генерирует СЛУЧАЙНЫЙ 10-значный Post Code"""
        return ''.join(random.choices(string.digits, k=10))

    @staticmethod
    def generate_first_name_from_post_code(post_code):
        """Генерирует First Name на основе Post Code"""
        name_chars = []
        for i in range(0, min(10, len(post_code)), 2):
            digit_pair = post_code[i:i + 2]
            if digit_pair.isdigit():
                char_code = int(digit_pair) % 26
                name_chars.append(chr(ord('a') + char_code))
        return ''.join(name_chars) if name_chars else "User"

    @staticmethod
    def generate_last_name():
        """Генерирует случайную фамилию"""
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones",
                      "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
        return random.choice(last_names)

    @staticmethod
    def find_closest_to_average_name(names):
        """Находит имя с длиной, наиболее близкой к средней"""
        if not names:
            return None

        lengths = [len(name) for name in names]
        average_length = sum(lengths) / len(lengths)

        closest_name = min(names, key=lambda name: abs(len(name) - average_length))
        return closest_name