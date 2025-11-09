import random
import string


class TestDataGenerator:
<<<<<<< HEAD
    @staticmethod
    def generate_post_code():
        """Генерация 10-значного почтового кода"""
        return ''.join([str(random.randint(0, 9)) for _ in range(10)])

    @staticmethod
    def generate_first_name_from_post_code(post_code):
        """
        Генерация имени на основе почтового кода
        Логика: разбиваем на двузначные числа, преобразуем в буквы (0-25 = a-z)
        Если число > 25, берем остаток от деления на 26
        """
        if len(post_code) != 10:
            raise ValueError("Post Code должен содержать 10 цифр")

        # Разбиваем на 5 двузначных чисел
        numbers = [int(post_code[i:i + 2]) for i in range(0, 10, 2)]

        # Преобразуем числа в буквы
        name_parts = []
        for num in numbers:
            # Берем остаток от деления на 26 для чисел > 25
            letter_index = num % 26
            letter = string.ascii_lowercase[letter_index]
            name_parts.append(letter)

        return ''.join(name_parts)

    @staticmethod
    def generate_last_name():
        """Генерация случайной фамилии"""
        syllables = ['son', 'man', 'wood', 'field', 'stone', 'brook', 'hill', 'ford']
        prefixes = ['Smith', 'John', 'Will', 'Brown', 'Green', 'White', 'Black', 'Taylor']
        return random.choice(prefixes) + random.choice(syllables)

    @staticmethod
    def find_closest_to_average_name(names):
        """
        Находит имя с длиной, наиболее близкой к средней длине всех имен
        """
        if not names:
            return None

        # Вычисляем длины имен
        name_lengths = [len(name) for name in names]

        # Вычисляем среднюю длину
        average_length = sum(name_lengths) / len(name_lengths)

        # Находим имя с длиной, наиболее близкой к средней
        closest_name = min(names, key=lambda name: abs(len(name) - average_length))

        return closest_name
=======
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
        """Находит имя с длиной, наиболее близкой к средней, исключая короткие имена"""
        if not names:
            return None

        lengths = [len(name) for name in names]
        average_length = sum(lengths) / len(lengths)

        # Фильтруем слишком короткие имена (меньше 4 символов)
        filtered_names = [name for name in names if len(name) >= 4]

        if not filtered_names:
            filtered_names = names

        # Находим 3 самых близких к среднему
        closest_names = sorted(filtered_names, key=lambda name: abs(len(name) - average_length))[:3]

        # Выбираем случайного из ближайших
        return random.choice(closest_names)

    @staticmethod
    def find_random_customer(names):
        """Выбирает случайного клиента для удаления"""
        if not names:
            return None
        return random.choice(names)
>>>>>>> develop
