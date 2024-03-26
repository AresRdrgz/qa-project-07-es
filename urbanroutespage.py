from selenium.webdriver.common.by import By
class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    comfort_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]')
    telephone_field = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[1]/div')
    pay_method_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[2]')
    payment_modal = (By.CLASS_NAME, 'modal')
    add_credit_card_button = (By.XPATH, "//div[contains(@class, 'pp-row') and contains(@class, 'disabled')]")
    credit_card_id_field = (By.CLASS_NAME, 'card-number-input')
    card_id_input = (By.ID, 'number')
    credit_card_code_id_field = (By.CLASS_NAME, 'card-code-input')
    card_code_input = (By.ID, 'code')
    credit_card_submit = (By.XPATH, '//div[@class="pp-buttons"]/child::*[1]')
    credit_card_close = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')
    comment_field = (By.ID, 'comment')
    blanket_and_handkerchiefs_switch = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span')
    icecream_counter = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')
    taxi_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/button')
    modal_timer = (By.XPATH, '//*[@id="root"]/div/div[5]/div[2]/div[1]/div/div[2]')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def get_element_by_text(self, text):
        xpath = f"//button[contains(text(), '{text}')]"
        return self.driver.find_element(By.XPATH, xpath)

    def get_comfort_button(self):
        return self.driver.find_element(*self.comfort_button)


    def get_telephone(self):
        return self.driver.find_element(*self.telephone_field)

    def set_telephone(self, phone_number):
        telephone = self.get_telephone()
        self.driver.execute_script(f"arguments[0].innerText='{phone_number}'", telephone)

    def get_payment_button(self):
        return self.driver.find_element(*self.pay_method_button)

    def get_modal(self):
        return self.driver.find_element(*self.payment_modal)

    def get_add_credit_card_button(self, modal):
        return modal.find_element(*self.add_credit_card_button)

    def get_credit_card_id_field(self):
        return self.driver.find_element(*self.credit_card_id_field).find_element(*self.card_id_input)

    def set_credit_card_id_field(self, credit_card_id):
        self.get_credit_card_id_field().send_keys(credit_card_id)

    def get_card_code_id_field(self):
        return self.driver.find_element(*self.credit_card_code_id_field).find_element(*self.card_code_input)

    def set_card_code_id_field(self, card_code):
        self.get_card_code_id_field().send_keys(card_code)

    def get_submit_credit_card(self):
        return self.driver.find_element(*self.credit_card_submit)

    def get_credit_card_close(self):
        return self.driver.find_element(*self.credit_card_close)

    def get_comment_field(self):
        return self.driver.find_element(*self.comment_field)

    def set_comment_field(self, comment):
        self.driver.find_element(*self.comment_field).send_keys(comment)

    def get_blanket_switch(self):
        return self.driver.find_element(*self.blanket_and_handkerchiefs_switch)

    def get_icecream_counter(self):
        return self.driver.find_element(*self.icecream_counter)

    def get_taxi_button(self):
        return self.driver.find_element(*self.taxi_button)

    def get_modal_timer(self):
        return self.driver.find_element(*self.modal_timer)
