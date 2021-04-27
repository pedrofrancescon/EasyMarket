# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.cart_status import CartStatus  # noqa: E501
from openapi_server.test import BaseTestCase


class TestCartController(BaseTestCase):
    """CartController integration test stubs"""

    def test_cart_alter_item(self):
        """Test case for cart_alter_item

        alter amount of item in purchase
        """
        headers = { 
        }
        response = self.client.open(
            '/purchase/{purchase_id}/{rfid_code}'.format(rfid_code=315748, purchase_id=56),
            method='PUT',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cart_check_on_purchase(self):
        """Test case for cart_check_on_purchase

        maybe get current purchase data for a cart
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/cart/{qr_code}'.format(qr_code='qr_code_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cart_end_purchase(self):
        """Test case for cart_end_purchase

        Ending purchase
        """
        headers = { 
        }
        response = self.client.open(
            '/cart/{qr_code}'.format(qr_code='qr_code_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
