#Данные для авторизации
import os
from dotenv import load_dotenv
from faker import Faker
import string
load_dotenv()

# Основной URL тестируемого сайта
MAIN_URL = 'https://b2c.passport.rt.ru'

fake_ru = Faker('ru_RU')
fake_firstname = fake_ru.first_name()
fake_lastname = fake_ru.last_name()
fake_phone = fake_ru.phone_number()
fake = Faker()
fake_password = fake.password()
fake_login = fake.user_name()
fake_email = fake.email()


valid_phone = os.getenv('phone')
valid_login = os.getenv('login')
valid_password = os.getenv('password')
invalid_ls = '1234567890'

valid_email = "xxx123@mail.ru"
valid_pass_reg = 'Qwerty'


def generate_string_rus(n):
    return 'б' * n


def generate_string_en(n):
    return 'x' * n


def english_chars():
    return 'qwertyuiop'


def russian_chars():
    return 'абвгдеёжз'


def chinese_chars():
    return '不了人大来以个中上们'


def special_chars():
    return f'{string.punctuation}'
