# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.login import Login
from openapi_server import util

from openapi_server.models.login import Login  # noqa: E501

class NewLoginReq(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, login=None, name=None):  # noqa: E501
        """NewLoginReq - a model defined in OpenAPI

        :param login: The login of this NewLoginReq.  # noqa: E501
        :type login: Login
        :param name: The name of this NewLoginReq.  # noqa: E501
        :type name: str
        """
        self.openapi_types = {
            'login': Login,
            'name': str
        }

        self.attribute_map = {
            'login': 'login',
            'name': 'name'
        }

        self._login = login
        self._name = name

    @classmethod
    def from_dict(cls, dikt) -> 'NewLoginReq':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The NewLoginReq of this NewLoginReq.  # noqa: E501
        :rtype: NewLoginReq
        """
        return util.deserialize_model(dikt, cls)

    @property
    def login(self):
        """Gets the login of this NewLoginReq.


        :return: The login of this NewLoginReq.
        :rtype: Login
        """
        return self._login

    @login.setter
    def login(self, login):
        """Sets the login of this NewLoginReq.


        :param login: The login of this NewLoginReq.
        :type login: Login
        """
        if login is None:
            raise ValueError("Invalid value for `login`, must not be `None`")  # noqa: E501

        self._login = login

    @property
    def name(self):
        """Gets the name of this NewLoginReq.


        :return: The name of this NewLoginReq.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this NewLoginReq.


        :param name: The name of this NewLoginReq.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501
        if name is not None and len(name) > 100:
            raise ValueError("Invalid value for `name`, length must be less than or equal to `100`")  # noqa: E501

        self._name = name
