import pytest
from pages.auth import *
from pages.settings import *


@pytest.mark.auth
@pytest.mark.negative
@pytest.mark.parametrize('username', [fake_phone, fake_login, invalid_ls],
                         ids=['fake phone', 'fake login', 'fake service account'])
def test_auth_page_fake_phone_login_serv_account(browser, username):
    page = AuthPage(browser)
    page.enter_username(username)
    page.enter_password(valid_password)
    page.btn_click_enter()
    browser.implicitly_wait(10)

    error_mess = browser.find_element(*AuthLocators.AUTH_FORM_ERROR)
    forgot_pass = browser.find_element(*AuthLocators.AUTH_FORGOT_PASSWORD)

    assert error_mess.text == 'Неверный логин или пароль' and \
           page.check_color(forgot_pass) == '#ff4f12'


@pytest.mark.auth
@pytest.mark.negative
def test_auth_page_fake_email(browser):
    #Авторизация  по не валидной почте
    page = AuthPage(browser)
    page.enter_username(fake_email)
    page.enter_password(valid_pass_reg)
    time.sleep(20)
    page.btn_click_enter()
    browser.implicitly_wait(10)

    error_mess = browser.find_element(*AuthLocators.AUTH_FORM_ERROR)
    forgot_pass = browser.find_element(*AuthLocators.AUTH_FORGOT_PASSWORD)

    assert error_mess.text == 'Неверный логин или пароль' and \
           page.check_color(forgot_pass) == '#ff4f12'


@pytest.mark.auth
@pytest.mark.negative
@pytest.mark.parametrize('username', [valid_phone, valid_email, valid_login],
                         ids=['valid phone', 'valid login', 'valid email'])
def test_auth_page_fake_password(browser, username):
    page = AuthPage(browser)
    page.enter_username(username)
    page.enter_password(fake_password)
    page.btn_click_enter()
    browser.implicitly_wait(10)

    error_mess = browser.find_element(*AuthLocators.AUTH_FORM_ERROR)
    forgot_pass = browser.find_element(*AuthLocators.AUTH_FORGOT_PASSWORD)

    assert error_mess.text == 'Неверный логин или пароль' and \
           page.check_color(forgot_pass) == '#ff4f12'


@pytest.mark.auth
@pytest.mark.negative
def test_auth_page_phone_empty_username(browser):
    page = AuthPage(browser)
    page.enter_username('')
    page.enter_password(valid_password)
    page.btn_click_enter()
    browser.implicitly_wait(10)

    error_mess = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_mess.text == 'Введите номер телефона' or \
           error_mess.text == 'Введите адрес, указанный при регистрации' or \
           error_mess.text == 'Введите логин, указанный при регистрации' or \
           error_mess.text == 'Введите номер вашего лицевого счета'


@pytest.mark.auth
@pytest.mark.negative
@pytest.mark.parametrize('username', [1, 111111111],
                         ids=['one digit', '9 digits'])
def test_auth_page_invalid_username(browser, username):
    """Проверка авторизации по номеру телефона и паролю, неверный формат телефона"""
    page = AuthPage(browser)
    page.enter_username(username)
    page.enter_password(valid_password)
    page.btn_click_enter()
    browser.implicitly_wait(10)

    error_mess = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_mess.text == 'Неверный формат телефона'
