from selenium.webdriver.support.wait import WebDriverWait

import data
import urbanroutespage
from selenium import webdriver
import time

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
        routes_page = urbanroutespage.UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        self.driver.implicitly_wait(10)
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_comfort_fee(self):
        self.test_set_route()
        routes_page = urbanroutespage.UrbanRoutesPage(self.driver)
        button_text = "Pedir un taxi"
        button = routes_page.get_element_by_text(button_text)
        assert button.text == button_text
        button.click()
        routes_page.get_comfort_button().click()

    def test_add_telephone_number(self):
        self.test_select_comfort_fee()
        routes_page = urbanroutespage.UrbanRoutesPage(self.driver)
        routes_page.set_telephone(data.phone_number)
        telephone = routes_page.get_telephone()
        assert telephone.text == data.phone_number

    def test_add_credit_card(self):
        self.test_select_comfort_fee()
        routes_page = urbanroutespage.UrbanRoutesPage(self.driver)
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
        routes_page = urbanroutespage.UrbanRoutesPage(self.driver)
        self.test_select_comfort_fee()
        routes_page.set_comment_field(data.message_for_driver)
        assert routes_page.get_comment_field().get_attribute('value') == data.message_for_driver

    def test_add_blanket_and_handkerchiefs(self):
        routes_page = urbanroutespage.UrbanRoutesPage(self.driver)
        self.test_select_comfort_fee()
        b_switch = routes_page.get_blanket_switch()
        b_switch.click()

    def test_add_icecream(self):
        routes_page = urbanroutespage.UrbanRoutesPage(self.driver)
        self.test_select_comfort_fee()
        counter = routes_page.get_icecream_counter()
        counter.click()
        counter.click()

    def test_searching_for_taxi_modal(self):
        routes_page = urbanroutespage.UrbanRoutesPage(self.driver)
        self.test_write_message()
        button = routes_page.get_taxi_button()
        button.click()

    def test_driver_information(self):
        routes_page = urbanroutespage.UrbanRoutesPage(self.driver)
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
