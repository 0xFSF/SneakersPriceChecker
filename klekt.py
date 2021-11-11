import datetime
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Klekt:

    def __init__(self, driver, size, sku):
        self.driver = driver
        self.size = size
        self.sku = sku
        self.t = -1

    # def region(self):
    #     # Chooses eu region
    #     self.driver.get("https://www.klekt.com")
    #     time.sleep(1.5)
    #     self.driver.find_element_by_xpath('/html/body/div[8]/div/div/div/div/div/div/button').click()
    #     self.driver.find_element_by_xpath('//*[@aria-label="open menu"]').click()
    #     time.sleep(1.5)
    #     self.driver.find_element_by_id('flag1-item-1').click()

    def product_link(self):
        # Gets product link
        self.t += 1
        self.driver.get("https://www.klekt.com/category/all#search={}".format(self.sku))
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'pod-link')))
        self.driver.find_elements_by_class_name('pod-link')
        return self.driver.find_elements_by_class_name('pod-link')[self.t].get_attribute('href')

    def item_info(self):
        # Gets item price
        link = self.product_link()
        self.driver.get(link)
        time.sleep(3)
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, '//button[@gtm="gtm"]/div')))

        try:
            while self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[1]/div[3]/p[1]/span[2]')\
                    .text != self.sku:
                link = self.product_link()
                self.driver.get(link)
                time.sleep(3)
                WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, '//button['
                                                                                               '@gtm="gtm"]/div')))
        except Exception:
            try:
                while self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[1]/div[2]/p['
                                                        '1]/span[2]').text != self.sku:
                    link = self.product_link()
                    self.driver.get(link)
                    time.sleep(3)
                    WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, '//button['
                                                                                                   '@gtm="gtm"]/div')))
            except Exception:
                while self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[1]/div[1]/p['
                                                        '1]/span[2]').text != self.sku:
                    link = self.product_link()
                    self.driver.get(link)
                    time.sleep(3)
                    WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, '//button['
                                                                                                   '@gtm="gtm"]/div')))

        for s in range(1, 25):
            try:
                # Chooses appropriate size
                sizes = self.driver.find_element_by_xpath('//*[@class="u-grid undefined"]/div[{}]'.format(s))
                if sizes.find_element_by_xpath('//*[@class="u-grid undefined"]/div[{}]/span[1]/span'.format(s))\
                        .get_attribute("innerText") == self.size:
                    if '$' in sizes.find_element_by_xpath('//*[@class="u-grid undefined"]/div[{}]/span[2]/'
                                                          'span[1]'.format(s)).text:
                        return self.item_info()
                    price = float(sizes.find_element_by_xpath('//*[@class="u-grid undefined"]/div[{}]/span[2]/span[2]'
                                                              .format(s)).get_attribute("innerText"))
                    return price
            except Exception:
                print('{}:Nothing for sale'.format(datetime.datetime.now()))
