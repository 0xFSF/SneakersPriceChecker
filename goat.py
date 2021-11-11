import datetime
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def captcha():
    print("{}: Solve captcha".format(datetime.datetime.now()))
    time.sleep(5)


class Goat:

    def __init__(self, size, sku, driver):
        self.driver = driver
        self.sku = sku
        self.size = size

    def region(self):
        # Chooses region
        self.driver.get("https://www.goat.com/search?query={}".format(self.sku))
        time.sleep(1)
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler')))
            self.driver.find_element_by_id('onetrust-accept-btn-handler').click()
            self.driver.find_element_by_xpath('//*[@data-qa="button-cancel"]').click()
        except Exception:
            try:
                self.driver.find_element_by_xpath('//*[@data-qa="button-cancel"]').click()
            except Exception:
                print('{}: Click accept'.format(datetime.datetime.now()))
                input()

        time.sleep(0.5)

    def product_link(self):
        # Gets product link
        self.driver.get("https://www.goat.com/search?query={}".format(self.sku))
        time.sleep(1)

        while True:
            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@data-qa'
                                                                                               '="search_grid_cell"]')))
                return self.driver.find_element_by_xpath('//a[@data-qa="search_grid_cell"]').get_attribute('href')
            except Exception:
                captcha()

    def item_info(self):
        # Gets item price
        product_link = self.product_link()
        self.driver.get(product_link)
        time.sleep(1)

        try:
            while self.driver.find_element_by_class_name('page-title').text:
                captcha()
                continue
        except Exception:
            pass

        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, '//button[@data-qa="btn-pdp'
                                                                                        '-buy-new"]')))
        self.driver.find_element_by_xpath('//button[@data-qa="btn-pdp-buy-new"]').click()
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, '//div[@class="swiper-wrapper"]')
                                                                            ))
        sizes = self.driver.find_element_by_xpath('//div[@class="swiper-wrapper"]')
        for s in range(1, 25):
            try:
                # Chooses appropriate size
                if sizes.find_element_by_xpath('//div[@class="swiper-wrapper"]/button[{}]/div/div[1]'.format(s))\
                        .get_attribute("innerText") == self.size:
                    price = float(sizes.find_element_by_xpath('//div[@class="swiper-wrapper"]/button[{}]/div/div[2]'
                                                              .format(s)).get_attribute("innerText").replace('$', ''))
                    return price
            except Exception:
                print('{}:Nothing for sale'.format(datetime.datetime.now()))
