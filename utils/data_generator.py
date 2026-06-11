import datetime
import random
import string
from faker import Faker

faker = Faker()


class DataGenerator:

    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"kek{random_string}@gmail.com"


    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"


    @staticmethod
    def generate_random_password():
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        # Гарантируем наличие хотя бы одной буквы и одной цифры
        letters = random.choice(string.ascii_letters)  # Одна буква
        digits = random.choice(string.digits)  # Одна цифра

        # Дополняем пароль случайными символами из допустимого набора
        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)  # Остальная длина пароля
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        # Перемешиваем пароль для рандомизации
        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    """
    Добавим метод в DataGenerator который сразу делает рандомные данные
    которые можно сразу передать в метод создания юзера через БД
    """

    @staticmethod
    def generate_user_data() -> dict:
        """Генерирует данные для тестового пользователя"""
        from uuid import uuid4

        return {
            'id': f'{uuid4()}',  # генерируем UUID как строку
            'email': DataGenerator.generate_random_email(),
            'full_name': DataGenerator.generate_random_name(),
            'password': DataGenerator.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }

    @staticmethod
    def generate_movie_data() -> dict:
        return {
            'id': faker.random_int(min=1, max=555),
            'name': f'About {faker.first_name()} {faker.last_name()}',
            'price': faker.random_int(min=100, max=1000),
            'description': f'Absolute cinema about {faker.date()} years and {faker.last_name()}',
            'image_url': "https://example.com/image.png",
            'location': faker.random_element(['SPB', 'MSK']),
            'published': True,
            'rating': faker.random_int(min=1, max=10),
            'genre_id': 1,
            'created_at': datetime.datetime.now()
        }

    @staticmethod
    def generate_random_int(max_value: int) -> int:
        return faker.random_int(min=1, max=max_value)