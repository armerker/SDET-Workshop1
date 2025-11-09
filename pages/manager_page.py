from selenium.webdriver.common.by import By
from .base_page import BasePage


class ManagerPage(BasePage):
    # Locators
    ADD_CUSTOMER_BTN = (By.XPATH, "//button[contains(text(),'Add Customer')]")
    OPEN_ACCOUNT_BTN = (By.XPATH, "//button[contains(text(),'Open Account')]")
    CUSTOMERS_BTN = (By.XPATH, "//button[contains(text(),'Customers')]")

    # Add Customer form
    FIRST_NAME_INPUT = (By.XPATH, "//input[@placeholder='First Name']")
    LAST_NAME_INPUT = (By.XPATH, "//input[@placeholder='Last Name']")
    POST_CODE_INPUT = (By.XPATH, "//input[@placeholder='Post Code']")
    ADD_CUSTOMER_SUBMIT_BTN = (By.XPATH, "//button[@type='submit']")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def click_add_customer(self):
        self.click(self.ADD_CUSTOMER_BTN)

    def click_customers(self):
        self.click(self.CUSTOMERS_BTN)

    def add_customer(self, first_name, last_name, post_code):

        self.click_add_customer()

        # Ждем появления формы
        self.find_element(self.FIRST_NAME_INPUT)

        self.send_keys(self.FIRST_NAME_INPUT, first_name)
        self.send_keys(self.LAST_NAME_INPUT, last_name)
        self.send_keys(self.POST_CODE_INPUT, post_code)
        self.click(self.ADD_CUSTOMER_SUBMIT_BTN)


        return self.get_alert_text()