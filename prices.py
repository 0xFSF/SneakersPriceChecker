from goat import Goat
from klekt import Klekt
from restocks import Restocks
from stockx import Stockx
# Gets prices from each site


class Prices:

    def __init__(self, driver, sizes_list, sku, email, password, t, rate_gbp, rate_eur, rate_usd):
        self.driver = driver
        self.sizes_list = sizes_list
        self.sku = sku
        self.email = email
        self.password = password
        self.t = t
        self.rate_gbp = rate_gbp
        self.rate_eur = rate_eur
        self.rate_usd = rate_usd

    def stockx(self):
        st = Stockx(self.driver, self.sizes_list[0], self.sku, self.email, self.password)
        if self.t == 0:
            st.region()
            st.logging_in()
        try:
            list_stockx = st.item_info()
            price_stockx = (list_stockx[1] - (list_stockx[1] * 0.03) - (list_stockx[1] * 0.065)) * self.rate_gbp
            return [list_stockx[0], list_stockx[1], price_stockx]
        except Exception:
            return ['None', 0, 0]

    def klekt(self):
        kl = Klekt(self.driver, self.sizes_list[1], self.sku)
        # if self.t == 0:
            # kl.region()
        try:
            price = kl.item_info()
            price_klekt = (price - (price * 0.15)) * self.rate_eur
            return [price, price_klekt]
        except Exception:
            return [0, 0]

    def restocks(self):
        rest = Restocks(self.driver, self.sizes_list[2], self.sku)
        if self.t == 0:
            rest.region()
        try:
            price = rest.item_info()
            price_restocks = (price * 0.9 - 10) * self.rate_eur
            return [price, price_restocks]
        except Exception:
            return [0, 0]

    def goat(self):
        gt = Goat(self.sizes_list[3], self.sku, self.driver)
        if self.t == 0:
            gt.region()
        try:
            price = gt.item_info()
            price_goat = ((price - (price * 0.095) - 12) * 0.971 * self.rate_usd) * 0.97
            return [price, price_goat]
        except Exception:
            return [0, 0]
