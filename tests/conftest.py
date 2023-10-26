import pytest
from selenium import webdriver

@pytest.fixture(autouse=True)
def browser():
    driver = webdriver.Firefox()

    yield driver
    driver.quit()
