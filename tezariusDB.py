import base64

import requests
from requests import JSONDecodeError

import config
from datetime import datetime
import datetime as dt
import pytz

format_str = '%Y.%m.%d'
day = dt.timedelta(days=1)
timezone = pytz.timezone('Europe/Moscow')


class Sales:
    def __init__(self, d1=(datetime.now(timezone) - day).strftime(format_str),
                 d2=datetime.now(timezone).strftime(format_str)):
        self.orders = 'Error'
        self.d1 = d1
        self.d2 = d2
        self.headers = {'Authorization': 'Basic ' + base64.b64encode(
            (config.tz_login + ':' + config.tz_password).encode()).decode()}
        self.host = config.tz_host
        self.sess = requests.session()
        self.sess.headers = self.headers
        self.prods = []

    def get_order(self, order_id):
        method = '/method/orders/GetOrderListDetails'
        data = {
            "db": config.tz_db,
            "params":
                [
                    {
                        "YourReferenceOperationID": 1,
                        "jparams":
                            {
                                "GroupByDocNumber": 0,
                                "ByOrderNumber": order_id,
                                "ShowArh": "1",
                                "MyOnly": "0"
                            }
                    }
                ]
        }
        try:
            return self.sess.post(self.host + method, json=data).json()[0]['result']
        except JSONDecodeError:
            return None

    def get_client(self, client_id):
        method = '/method/any/SearchCounterparts'
        data = {
            'db': config.tz_db,
            'params': [{
                "YourReferenceOperationID": 1,
                'jparams': {
                    'CurrID': 0,
                    'SearchFilter': 'ById',
                    'SearchValue': str(client_id),
                    'FirmID': config.firmid
                }
            }]
        }
        try:
            return self.sess.post(self.host + method, json=data).json()[0]['result'][0]
        except JSONDecodeError as e:
            return None

    def get_product(self, sku):
        method = '/method/referencebook/rbGoods/get'
        data = {
            'db': config.tz_db,
            'params': [{
                "YourReferenceOperationID": 1,
                'jparams': {
                    "RemaindersByStockID": 2,
                    "isRemainsOnly": 0,
                    "filter": "GoodsMultiSearch",
                    "multivalue": sku,
                    "limit": 100,
                    "limitPos": 1
                }
            }]
        }
        try:
            result = self.sess.post(self.host + method, json=data).json()[0]['result']
            for prod in result:
                if str(prod['code']) == str(sku):
                    return prod
        except JSONDecodeError:
            return None

    def get_client_by_phone(self, phone):
        method = '/method/any/SearchCounterparts'
        data = {
            'db': config.tz_db,
            'params': [{
                "YourReferenceOperationID": 1,
                'jparams': {
                    'CurrID': 0,
                    'SearchFilter': 'MultiSearch',
                    'SearchValue': phone,
                    'FirmID': config.firmid
                }
            }]
        }
        try:
            return self.sess.post(self.host + method, json=data).json()[0]['result'][0]
        except JSONDecodeError as e:
            return None
        except Exception:
            return None

    def get_orders(self):
        method = '/method/orders/GetOrderListDetails'
        data = {
            "db": "TZRS_2071_84593",
            "params":
                [
                    {
                        "YourReferenceOperationID": 1,
                        "jparams":
                            {
                                "GroupByDocNumber": 0,
                                "ByDate": 1,
                                "HideIssued": 0,
                                "date1": self.d1,
                                "date2": self.d2,
                                "ShowArh": 1,
                                "MyOnly": 0,
                                "TZ": 0,
                                "ShowSales": 1
                            }
                    }
                ]
        }
        try:
            self.orders = self.sess.post(self.host + method, json=data).json()[0]['result']
        except JSONDecodeError:
            self.orders = 'Error'

    def get_location_id(self, name):
        method = '/method/referencebook/rbStockStoragePlace/get'
        data = {
            'db': config.tz_db,
            'params': [
                {
                    'YourReferenceOperationID': 1,
                    'jparams': {
                        'filter': 'rbStock',
                        'id_rbStock': 2
                    }
                }
            ]
        }

        try:
            res = self.sess.post(self.host + method, json=data).json()[0]['result']
            for i in res:
                if i['name'] == name:
                    return i['id']
        except JSONDecodeError:
            return None

    def add_cart(self, counterpart_id, product_id, qty, loc_name):
        method = '/method/cart/add'
        data = {
            'db': config.tz_db,
            'params': [
                {
                    'YourReferenceOperationID': 1,
                    'jparams': {
                        "isWebCart": 0,
                        "ShopID": 2,
                        "tabID": 1,
                        "CounterPartsID": counterpart_id,
                        "id_rbGoods": product_id,
                        "GoodsTempID": 0,
                        "qty": qty,
                        "FirmID": 2,
                        "StockID": 2,
                        "PlaceID": self.get_location_id(loc_name) if self.get_location_id(loc_name) else 0,
                        "note": '',
                        "isHideArticleCode": 0,
                        "LanguageCode": 'ru'
                    }
                }
            ]
        }

        try:
            self.sess.post(self.host + method, json=data).json()[0]['result']
        except JSONDecodeError:
            return None

    def create_order(self, order_id, date, customer_name, customer_phone, customer_email, customer_source, note,
                     positions):
        method = '/method/cart/OrderFastAny'
        positions_tz = []
        for pos in positions:
            positions_tz.append({'isInnerGoods': 1, 'name': pos['name'], 'code': int(pos['code']),
                                 'brand': pos['brand'],
                                 'cost': pos['cost'], 'cost_in': pos['cost'],
                                 'qty': pos['qty'], 'note': pos['note'], 'warehouse': 'Автозапчасти Гидрач',
                                 'dlvrMin': pos['date'], 'dlvrMax': pos['date']})
        data = {
            'db': config.tz_db,
            'params': [
                {
                    'YourReferenceOperationID': 1,
                    'jparams': {
                        'FirmID': 2,
                        'ShopID': 2,
                        'isWebCard': 1,
                        'OrderID': order_id,
                        'OrderDataSet': date,
                        'CounterPartsID': self.get_client_by_phone(customer_phone)['id'] if self.get_client_by_phone(
                            customer_phone) else 0,
                        'CustomerName': customer_name,
                        'CustomerPhone': customer_phone,
                        'CustomerEmail': customer_email,
                        'CustomerSource': customer_source,
                        'note': note,
                        'isToWork': 0,
                        'isDelivery': 0,
                        'address_delivery': '',
                        'isDeliveryPartly': 0,
                        'LanguageCode': 'ru',
                        'positions': positions_tz
                    }
                }
            ]
        }

        try:
            return self.sess.post(self.host + method, json=data).json()[0]['result']
        except JSONDecodeError:
            print('error')
            return 'Error'

    def get_sales(self):
        method = '/method/reports/ReportSales'
        data = {
            'db': config.tz_db,
            'params': [{
                "YourReferenceOperationID": 1,
                'jparams': {
                    'GroupByDocNumber': 0,
                    'byDocID': 0,
                    'd1': self.d1,
                    'd2': self.d2,
                    'isByOnStock': 1,
                    'isByOrder': 1,
                    'isCarServiceOrder': 1,
                    'IsServiceGoods': 0,
                    'isReturnShow': 1,
                    'isCarServiceOrderClosed': 0
                }
            }]
        }
        try:
            self.prods = self.sess.post(self.host + method, json=data).json()[0]['result']
        except JSONDecodeError as e:
            self.prods = 'Error'


class Products:
    def __init__(self, start=1, limit=10000):
        self.page = start
        self.headers = {'Authorization': 'Basic ' + base64.b64encode(
            (config.tz_login + ':' + config.tz_password).encode()).decode()}
        self.host = config.tz_host
        self.sess = requests.session()
        self.sess.headers = self.headers
        self.limit = limit

    def __iter__(self):
        return self

    def __next__(self):
        method = '/method/referencebook/rbGoods/get'
        data = {
            'db': config.tz_db,
            'params': [{
                'YourReferenceOperationID': 1,
                'jparams': {
                    'isRemainsOnly': 0,
                    'limit': self.limit,
                    'RemaindersByStockId': 2,
                    'limitPos': self.page
                }
            }]
        }
        try:
            self.result = self.sess.post(self.host + method, json=data).json()
        except JSONDecodeError as e:
            self.result = 'Error'
        if self.result == 'Error' or not self.result[0]['result']:
            raise StopIteration
        else:
            self.page += 1
            return self.result[0]['result']
