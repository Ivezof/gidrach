import base64

import requests
from requests import JSONDecodeError

import config


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
