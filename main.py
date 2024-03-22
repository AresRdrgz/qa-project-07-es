import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import time

# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


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

class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()  # desired_capabilities=capabilities)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        self.driver.implicitly_wait(10)
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_comfort_fee(self):
        self.test_set_route()
        routes_page = UrbanRoutesPage(self.driver)
        button_text = "Pedir un taxi"
        button = routes_page.get_element_by_text(button_text)
        assert button.text == button_text
        button.click()
        routes_page.get_comfort_button().click()

    def test_add_telephone_number(self):
        self.test_select_comfort_fee()
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_telephone(data.phone_number)
        telephone = routes_page.get_telephone()
        assert telephone.text == data.phone_number

    def test_add_credit_card(self):
        self.test_select_comfort_fee()
        routes_page = UrbanRoutesPage(self.driver)
        modal = routes_page.get_modal()
        payment_button = routes_page.get_payment_button()
        payment_button.click()
        add_card_button = routes_page.get_add_credit_card_button(modal)
        add_card_button.click()
        routes_page.set_credit_card_id_field(data.card_number)
        assert routes_page.get_credit_card_id_field().get_attribute('value') == data.card_number
        routes_page.set_card_code_id_field(data.card_code)
        assert routes_page.get_card_code_id_field().get_attribute('value') == data.card_code
        routes_page.get_credit_card_id_field().click()
        routes_page.get_submit_credit_card().click()
        routes_page.get_credit_card_close().click()

    def test_write_message(self):
        routes_page = UrbanRoutesPage(self.driver)
        self.test_select_comfort_fee()
        routes_page.set_comment_field(data.message_for_driver)
        assert routes_page.get_comment_field().get_attribute('value') == data.message_for_driver

    def test_add_blanket_and_handkerchiefs(self):
        routes_page = UrbanRoutesPage(self.driver)
        self.test_select_comfort_fee()
        b_switch = routes_page.get_blanket_switch()
        b_switch.click()

    def test_add_icecream(self):
        routes_page = UrbanRoutesPage(self.driver)
        self.test_select_comfort_fee()
        counter = routes_page.get_icecream_counter()
        counter.click()
        counter.click()

    def test_searching_for_taxi_modal(self):
        routes_page = UrbanRoutesPage(self.driver)
        self.test_write_message()
        button = routes_page.get_taxi_button()
        button.click()

    def test_driver_information(self):
        routes_page = UrbanRoutesPage(self.driver)
        self.test_searching_for_taxi_modal()
        time.sleep(0.1)
        timer = routes_page.get_modal_timer().text
        minutes, seconds = map(float, timer.split(':'))
        total_time = minutes * 60 + seconds + .25
        assert total_time >= 0
        time.sleep(total_time)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()


if __name__ == '__main__':
    test = TestUrbanRoutes()
    test.setup_class()
    ##test.test_set_route()
    ##test.test_select_comfort_fee()
    ##test.test_add_telephone_number()
    ##test.test_add_credit_card()
    ##test.test_write_message()
    ##test.test_blanket_and_handkerchiefs()
    ##test.test_icecream()
    ##test.test_searching_for_taxi_modal()
    ##test.test_driver_information()
