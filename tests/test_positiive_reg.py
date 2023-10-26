from pages.reg_mail import RegEmail
from pages.auth import *
from selenium.webdriver.common.by import By
from pages.settings import *
import time
import pytest

class TestRegistration:

    # Выносим данные в тело класса
    result_email, status_email = RegEmail().get_api_email()
    email_reg = result_email[0]

    @pytest.mark.reg
    @pytest.mark.positive
    def test_get_registration_valid(self, browser):


        # Разделяем email на имя и домен для использования в следующих запросах
        sign_at = self.email_reg.find('@')
        mail_name = self.email_reg[0:sign_at]
        mail_domain = self.email_reg[sign_at + 1:len(self.email_reg)]
        assert self.status_email == 200, 'status_email error'
        assert len(self.result_email) > 0, 'len(result_email) > 0 -> error'


        # Нажимаем на кнопку Зарегистрироваться:
        page = AuthPage(browser)
        page.enter_reg_page()
        browser.implicitly_wait(2)
        assert page.get_relative_link() == '/auth/realms/b2c/login-actions/registration'

        page = RegPage(browser)
        # Ввод имени
        page.enter_firstname(fake_firstname)
        browser.implicitly_wait(5)
        print(fake_firstname)
        # Ввод фамилии
        page.enter_lastname(fake_lastname)
        browser.implicitly_wait(5)
        print(fake_lastname)
        # Ввод адрес почты
        page.enter_email(self.email_reg)
        browser.implicitly_wait(3)

        # Ввод пароля
        page.enter_password(fake_password)
        browser.implicitly_wait(3)
        print(fake_password)
        # Ввод подтверждения пароля:
        page.enter_pass_conf(fake_password)
        browser.implicitly_wait(3)
        # Нажать кнопку 'Зарегистрироваться'
        page.btn_click()
        time.sleep(30)


        result_id, status_id = RegEmail().get_id_letter(mail_name, mail_domain)
        # Получение id письма с кодом
        id_letter = result_id[0].get('id')
        # Сверка полученных данные с ожиданиями
        assert status_id == 200, "status_id error"
        assert id_letter > 0, "id_letter > 0 error"


        result_code, status_code = RegEmail().get_reg_code(mail_name, mail_domain, str(id_letter))

        # Получаем body из текста письма
        text_body = result_code.get('body')
        # Получаем код из текста методом find
        reg_code = text_body[text_body.find('Ваш код : ') + len('Ваш код : '):
                             text_body.find('Ваш код : ') + len('Ваш код : ') + 6]
        # Сверка полученных данных с ожиданиями
        assert status_code == 200, "status_code error"
        assert reg_code != '', "reg_code != [] error"

        reg_digit = [int(char) for char in reg_code]
        browser.implicitly_wait(30)
        for i in range(0, 6):
            browser.find_elements(By.XPATH, '//input[@inputmode="numeric"]')[i].send_keys(reg_code[i])
            browser.implicitly_wait(5)
        browser.implicitly_wait(30)


        assert page.get_relative_link() == '/account_b2c/page', 'Регистрация не пройдена'
        page.driver.save_screenshot('reg_done.png')
        # Проверка о пройденной регистрации

        page.driver.save_screenshot('reg_done.png')
        # При успешной регистрации, перезаписываются данные в settings
        print(self.email_reg, fake_password)
        with open(r"../pages/settings.py", 'r', encoding='utf8') as file:
            lines = []
            print(lines)
            for line in file.readlines():
                if 'valid_email' in line:
                    lines.append(f"valid_email = '{str(self.email_reg)}'\n")
                elif 'valid_pass_reg' in line:
                    lines.append(f"valid_pass_reg = '{fake_password}'\n")
                else:
                    lines.append(line)
        with open(r"../pages/settings.py", 'w', encoding='utf8') as file:
            file.writelines(lines)
