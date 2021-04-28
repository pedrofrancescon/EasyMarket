# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class PaymentDataReq(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, payment=None):  # noqa: E501
        """PaymentDataReq - a model defined in OpenAPI

        :param payment: The payment of this PaymentDataReq.  # noqa: E501
        :type payment: int
        """
        self.openapi_types = {
            'payment': int
        }

        self.attribute_map = {
            'payment': 'payment'
        }

        self._payment = payment

    @classmethod
    def from_dict(cls, dikt) -> 'PaymentDataReq':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PaymentDataReq of this PaymentDataReq.  # noqa: E501
        :rtype: PaymentDataReq
        """
        return util.deserialize_model(dikt, cls)

    @property
    def payment(self):
        """Gets the payment of this PaymentDataReq.

        Payment method. Optional (transaction not completed if absent)  # noqa: E501

        :return: The payment of this PaymentDataReq.
        :rtype: int
        """
        return self._payment

    @payment.setter
    def payment(self, payment):
        """Sets the payment of this PaymentDataReq.

        Payment method. Optional (transaction not completed if absent)  # noqa: E501

        :param payment: The payment of this PaymentDataReq.
        :type payment: int
        """

        self._payment = payment
