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
        time.sleep(3)

        while True:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@role="dialog"]/footer/button')))
                self.driver.find_element_by_xpath('/html/body/div[5]/div[4]/div/section/footer/button').click()
                break
            except Exception as e:
                print(e)
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
        while True:
            try:
                self.driver.get("https://stockx.com/search/sneakers?s={}".format(self.sku))
                break
            except Exception:
                continue

        while True:
            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((
                    By.XPATH, '//*[@data-testid="search-confirmation"]')))
                href = self.driver.find_element_by_xpath('//*[@data-testid="product-tile"]')
                return href.find_element_by_css_selector('a').get_attribute('href')
            except Exception:
                captcha()

    def item_info(self):
        # Gets product name, sku and price

        self.driver.get(self.product_link())

        while True:
            try:
                self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/main/div/section[1]/div[3]/div['
                                                  '2]/div[1]/div[1]/div/button').click()
                break
            except Exception:
                try:
                    self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/main/div/section[1]/div['
                                                      '4]/div[2]/div[1]/div[1]/div/button').click()
                    break
                except Exception:
                    print('Something wrong')
                print('Something wrong')

        # Scraps price
        for s in range(1, 27):
            try:
                # Chooses appropriate size
                try:
                    sizes = self.driver.find_element_by_xpath('//div[@class="css-1o6kz7w"]/button[{}]/span['
                                                               '2]/div/dl'.format(s))
                    if sizes.find_element_by_xpath('dt[@class="chakra-stat__label css-nszg6y"]').text == "US M {}"\
                            .format(self.size) \
                            or sizes.find_element_by_xpath('dt[@class="chakra-stat__label css-nszg6y"]').text == \
                            "US {}".format(self.size):
                        if '€' in sizes.find_element_by_xpath('//div[@class="css-1o6kz7w"]/button[{}]/span['
                                                               '2]/div/dl/dd[@class="chakra-stat__number '
                                                               'css-1pulpde"]'.format(s)).text or '$' in \
                                sizes.find_element_by_xpath('//div[@class="css-1o6kz7w"]/button[{}]/span['
                                                             '2]/div/dl/dd[@class="chakra-stat__number '
                                                             'css-1pulpde"]'.format(s)).text:
                            self.logging_in()
                            return self.item_info()
                        lowest_price = float(sizes.find_element_by_xpath('dd[@class="chakra-stat__number css-1pulpde"]')
                                             .text.replace('£', ''))
                        lowest_price = (lowest_price / 1.05) - 1
                        item_name1 = self.driver.find_element_by_xpath('//*[@class="chakra-heading css-146c51c"]'). \
                            get_attribute("innerText")
                        item_name2 = self.driver.find_element_by_xpath('//*[@class="chakra-heading css-xgzdo7"]'). \
                            get_attribute("innerText")
                        self.driver.find_element_by_xpath('//div[@class="css-1o6kz7w"]/button[{}]'.format(s)).click()
                        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((
                            By.XPATH, '//*[@class="chakra-button__group css-1etipep"]/button[1]')))
                        self.driver.find_element_by_xpath('//*[@class="chakra-button__group css-1etipep"]/button[1]')\
                            .click()

                        staleElement = True
                        list_price = 0
                        while staleElement:
                            try:
                                list_price = float(self.driver.find_element_by_xpath('//*[@class="css-aydg0x"]/tr['
                                                                                     '1]/td[3]/p/p').get_attribute(
                                    "innerText").replace('£', ''))
                                list_price = float(self.driver.find_element_by_xpath('//*[@class="css-aydg0x"]/tr['
                                                                                     '1]/td[3]/p/p').get_attribute(
                                    "innerText").replace('£', ''))
                                staleElement = False
                            except Exception:
                                staleElement = True
                        if list_price > lowest_price:
                            price = list_price
                        else:
                            price = lowest_price

                        return [item_name1 + " " + item_name2, price]
                except Exception as e:
                    print(e)
                    continue
            except Exception:
                print('{}:Nothing for sale'.format(datetime.datetime.now()))
