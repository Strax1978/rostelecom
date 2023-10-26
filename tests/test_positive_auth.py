import pickle
import time
import pytest
from pages.auth import *
from selenium.webdriver.common.by import By
from pages.settings import *

@pytest.mark.auth
@pytest.mark.positive
@pytest.mark.xfail
@pytest.mark.parametrize('username', [valid_phone, valid_email, valid_login, invalid_ls],
                         ids=['phone', 'email', 'login', 'ls'])
def test_active_tab(browser, username):

    page = AuthPage(browser)
    page.enter_username(username)
    page.enter_password(valid_password)
    if username == valid_phone:
        assert browser.find_element(*AuthLocators.AUTH_ACTIVE_TAB).text == 'Телефон'
    elif username == valid_email:
        assert browser.find_element(*AuthLocators.AUTH_ACTIVE_TAB).text == 'Почта'
    elif username == valid_login:
        assert browser.find_element(*AuthLocators.AUTH_ACTIVE_TAB).text == 'Логин'
    else:
        assert browser.find_element(*AuthLocators.AUTH_ACTIVE_TAB).text == 'Лицевой счет'

@pytest.mark.auth
@pytest.mark.positive
@pytest.mark.parametrize('username', [valid_phone, valid_login],
                         ids=['valid phone', 'valid login'])
def test_auth_page_phone_login_valid(browser, username):
    page = AuthPage(browser)
    page.enter_username(username)
    page.enter_password(valid_password)
    page.btn_click_enter()

    assert page.get_relative_link() == '/account_b2c/page'

@pytest.mark.auth
@pytest.mark.positive
def test_auth_page_email_valid(browser):
    page = AuthPage(browser)
    page.enter_username(valid_email)
    page.enter_password(valid_password)
    time.sleep(10)
    page.btn_click_enter()
    page.driver.save_screenshot('auth_by_email.png')

    with open('my_cookies.txt', 'wb') as cookies:
        pickle.dump(browser.get_cookies(), cookies)

    assert page.get_relative_link() == '/account_b2c/page'


