# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.item_data import ItemData  # noqa: E501
from openapi_server.models.login_req import LoginReq  # noqa: E501
from openapi_server.models.new_login_req import NewLoginReq  # noqa: E501
from openapi_server.models.payment_data_req import PaymentDataReq  # noqa: E501
from openapi_server.models.purchase_item import PurchaseItem  # noqa: E501
from openapi_server.models.purchase_start_req import PurchaseStartReq  # noqa: E501
from openapi_server.test import BaseTestCase


class TestAppController(BaseTestCase):
    """AppController integration test stubs"""

    def test_app_end_purchase(self):
        """Test case for app_end_purchase

        End a purchase by the client
        """
        payment_data_req = {
  "payment" : 4748967312,
  "login" : {
    "password" : "senha",
    "email" : "josesilva@gmail.com"
  }
}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/purchase',
            method='DELETE',
            headers=headers,
            data=json.dumps(payment_data_req),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_current_purchase(self):
        """Test case for get_current_purchase

        Get current purchase items
        """
        login_req = {
  "login" : {
    "password" : "senha",
    "email" : "josesilva@gmail.com"
  }
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/purchase',
            method='GET',
            headers=headers,
            data=json.dumps(login_req),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_item_data(self):
        """Test case for get_item_data

        get item data
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/item/{rfid_code}'.format(rfid_code=315748),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_new_client(self):
        """Test case for new_client

        Add a client
        """
        new_login_req = {
  "name" : "Jose da Silva",
  "login" : {
    "password" : "senha",
    "email" : "josesilva@gmail.com"
  }
}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/client',
            method='POST',
            headers=headers,
            data=json.dumps(new_login_req),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_start_purchase(self):
        """Test case for start_purchase

        Start a purchase
        """
        purchase_start_req = {
  "VestType" : "blue",
  "qr_code" : "5477",
  "login" : {
    "password" : "senha",
    "email" : "josesilva@gmail.com"
  }
}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/purchase',
            method='POST',
            headers=headers,
            data=json.dumps(purchase_start_req),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
