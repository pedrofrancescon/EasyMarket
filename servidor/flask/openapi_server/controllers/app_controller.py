import connexion
import six

from openapi_server.models.item_data import ItemData  # noqa: E501
from openapi_server.models.login_req import LoginReq  # noqa: E501
from openapi_server.models.new_login_req import NewLoginReq  # noqa: E501
from openapi_server.models.payment_data_req import PaymentDataReq  # noqa: E501
from openapi_server.models.purchase_item import PurchaseItem  # noqa: E501
from openapi_server.models.purchase_start_req import PurchaseStartReq  # noqa: E501
from openapi_server import util


def app_end_purchase(payment_data_req=None):  # noqa: E501
    """End a purchase by the client

    Tries to end a purchase by either cancelling the purchase (does not include payment) or completing it(includes payment) # noqa: E501

    :param payment_data_req: 
    :type payment_data_req: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payment_data_req = PaymentDataReq.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_current_purchase(login_req=None):  # noqa: E501
    """Get current purchase items

     # noqa: E501

    :param login_req: 
    :type login_req: dict | bytes

    :rtype: List[PurchaseItem]
    """
    if connexion.request.is_json:
        login_req = LoginReq.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_item_data(rfid_code):  # noqa: E501
    """get item data

     # noqa: E501

    :param rfid_code: Item rfid_code
    :type rfid_code: int

    :rtype: ItemData
    """
    return 'do some magic!'


def new_client(new_login_req=None):  # noqa: E501
    """Add a client

     # noqa: E501

    :param new_login_req: 
    :type new_login_req: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        new_login_req = NewLoginReq.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def start_purchase(purchase_start_req=None):  # noqa: E501
    """Start a purchase

     # noqa: E501

    :param purchase_start_req: 
    :type purchase_start_req: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        purchase_start_req = PurchaseStartReq.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
