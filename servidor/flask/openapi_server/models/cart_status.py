# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.vesttype import Vesttype
from openapi_server import util

from openapi_server.models.vesttype import Vesttype  # noqa: E501

class CartStatus(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, purchase=None, vest_type=None):  # noqa: E501
        """CartStatus - a model defined in OpenAPI

        :param purchase: The purchase of this CartStatus.  # noqa: E501
        :type purchase: int
        :param vest_type: The vest_type of this CartStatus.  # noqa: E501
        :type vest_type: Vesttype
        """
        self.openapi_types = {
            'purchase': int,
            'vest_type': Vesttype
        }

        self.attribute_map = {
            'purchase': 'purchase',
            'vest_type': 'VestType'
        }

        self._purchase = purchase
        self._vest_type = vest_type

    @classmethod
    def from_dict(cls, dikt) -> 'CartStatus':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The CartStatus of this CartStatus.  # noqa: E501
        :rtype: CartStatus
        """
        return util.deserialize_model(dikt, cls)

    @property
    def purchase(self):
        """Gets the purchase of this CartStatus.


        :return: The purchase of this CartStatus.
        :rtype: int
        """
        return self._purchase

    @purchase.setter
    def purchase(self, purchase):
        """Sets the purchase of this CartStatus.


        :param purchase: The purchase of this CartStatus.
        :type purchase: int
        """
        if purchase is None:
            raise ValueError("Invalid value for `purchase`, must not be `None`")  # noqa: E501

        self._purchase = purchase

    @property
    def vest_type(self):
        """Gets the vest_type of this CartStatus.


        :return: The vest_type of this CartStatus.
        :rtype: Vesttype
        """
        return self._vest_type

    @vest_type.setter
    def vest_type(self, vest_type):
        """Sets the vest_type of this CartStatus.


        :param vest_type: The vest_type of this CartStatus.
        :type vest_type: Vesttype
        """
        if vest_type is None:
            raise ValueError("Invalid value for `vest_type`, must not be `None`")  # noqa: E501

        self._vest_type = vest_type
