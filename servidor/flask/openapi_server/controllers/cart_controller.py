import connexion
import six

from openapi_server.models.cart_status import CartStatus  # noqa: E501
from openapi_server import util


def cart_alter_item(rfid_code, purchase_id):  # noqa: E501
    """alter amount of item in purchase

     # noqa: E501

    :param rfid_code: Item rfid_code
    :type rfid_code: int
    :param purchase_id: 
    :type purchase_id: int

    :rtype: None
    """
    return 'do some magic!'


def cart_check_on_purchase(qr_code):  # noqa: E501
    """maybe get current purchase data for a cart

     # noqa: E501

    :param qr_code: Cart qr_code
    :type qr_code: str

    :rtype: CartStatus
    """
    return 'do some magic!'


def cart_end_purchase(qr_code):  # noqa: E501
    """Ending purchase

     # noqa: E501

    :param qr_code: Cart qr_code
    :type qr_code: str

    :rtype: None
    """
    return 'do some magic!'
