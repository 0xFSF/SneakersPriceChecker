import datetime
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def captcha():
    print("{}: Solve captcha".format(datetime.datetime.now()))
    time.sleep(5)


class Stockx:

    def __init__(self, driver, size, sku, email, password):
        self.driver = driver
        self.size = size
        self.sku = sku
        self.email = email
        self.password = password

    def region(self):
        # Chooses country
        self.driver.get("https://stockx.com/")
        self.driver.refresh()

        while True:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@role="dialog"]/footer/button')))
                time.sleep(0.5)
                self.driver.find_element_by_xpath('//*[@role="dialog"]/footer/button').click()
                break
            except Exception:
                captcha()
        time.sleep(4)

    def logging_in(self):
        # Logs

        while True:
            try:
                self.driver.find_element_by_xpath('//*[@id="nav-login"]').click()
                break
            except Exception:
                captcha()

        self.driver.refresh()

        while True:
            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="email-login"]')
                                                                                    ))
                self.driver.find_element_by_xpath('//*[@id="email-login"]').send_keys(self.email)
                time.sleep(0.5)
                self.driver.find_element_by_xpath('//*[@id="password-login"]').send_keys(self.password)
                time.sleep(1)
                break
            except Exception:
                captcha()

    def product_link(self):
        # Finds product link
        self.driver.get("https://stockx.com/search/sneakers?s={}".format(self.sku))

        while True:
            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((
                    By.XPATH, '//*[@data-testid="product-tile"]')))
                href = self.driver.find_element_by_xpath('//*[@data-testid="product-tile"]')
                return href.find_element_by_css_selector('a').get_attribute('href')
            except Exception:
                captcha()

    def item_info(self):
        # Gets product name, sku and price

        self.driver.get(self.product_link())

        while True:
            try:
                WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@class="product'
                                                                                              '-header-wrapper '
                                                                                              'css-j7qwjs"]/div['
                                                                                              '1]/h1')))
                break
            except Exception:
                try:
                    WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="product'
                                                                                                  '-header"]/div['
                                                                                                  '1]/div/h1')))
                    break
                except Exception:
                    print('{}:Nothing for sale'.format(datetime.datetime.now()))

        while True:
            try:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView();", self.driver.find_element_by_xpath("//a[text()='Home']"))
                try:
                    self.driver.find_element_by_xpath('//button[@id="menu-button-pdp-size-selector"]').click()
                except Exception:
                    self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/main/div/section[1]/div[3]/div['
                                                      '2]/div[1]/div[1]/div/button').click()
                break
            except Exception:
                self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/main/div/section[1]/div[4]/div[2]/div['
                                                  '1]/div[1]/div/button').click()

        # Scraps price
        for s in range(1, 27):
            try:
                # Chooses appropriate size
                try:
                    sizes1 = self.driver.find_element_by_xpath(
                        '/html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[1]/div[1]/div[1]/div[2]/div['
                        '1]/div/div/div/div/div/div[2]/ul/li[{}]'.format(s))
                    if sizes1.find_element_by_class_name('title').text == "US {}".format(self.size) \
                            or sizes1.find_element_by_class_name('title').text == "US M {}".format(self.size):
                        if '€' in sizes1.find_element_by_class_name('subtitle').text \
                                or '$' in sizes1.find_element_by_class_name('subtitle').text:
                            self.logging_in()
                            return self.item_info()
                        price = float(sizes1.find_element_by_class_name('subtitle').text.replace('£', ''))
                        item_name = self.driver.find_element_by_xpath(
                            '//*[@id="product-header"]/div[1]/div/h1').get_attribute("innerText")
                        return [item_name, price]
                except Exception:
                    try:
                        sizes2 = self.driver.find_element_by_xpath('//div[@class="css-1o6kz7w"]/button[{}]/span['
                                                                   '2]/div/dl'.format(s))
                        if sizes2.find_element_by_xpath('dt[@class="chakra-stat__label css-nszg6y"]').text == "US M {}"\
                                .format(self.size) \
                                or sizes2.find_element_by_xpath('dt[@class="chakra-stat__label css-nszg6y"]').text == \
                                "US {}".format(self.size):
                            if '€' in sizes2.find_element_by_xpath('//div[@class="css-1o6kz7w"]/button[{}]/span['
                                                                   '2]/div/dl/dd[@class="chakra-stat__number '
                                                                   'css-1pulpde"]'.format(s)).text or '$' in \
                                    sizes2.find_element_by_xpath('//div[@class="css-1o6kz7w"]/button[{}]/span['
                                                                 '2]/div/dl/dd[@class="chakra-stat__number '
                                                                 'css-1pulpde"]'.format(s)).text:
                                self.logging_in()
                                return self.item_info()
                            price = float(sizes2.find_element_by_xpath('dd[@class="chakra-stat__number '
                                                                       'css-1pulpde"]').text.replace('£', ''))
                            item_name1 = self.driver.find_element_by_xpath('//*[@class="chakra-heading '
                                                                           'primary-product-title '
                                                                           'css-1gbu8yz"]').get_attribute("innerText")
                            item_name2 = self.driver.find_element_by_xpath('//*[@class="chakra-heading '
                                                                           'secondary-product-title '
                                                                           'css-10v5fk5"]').get_attribute("innerText")
                            return [item_name1 + " " + item_name2, price]
                    except Exception as e:
                        print(e)
                        continue
            except Exception:
                print('{}:Nothing for sale'.format(datetime.datetime.now()))
