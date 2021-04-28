import connexion
import six

from openapi_server.models.login_req import LoginReq  # noqa: E501
from openapi_server.models.new_login_req import NewLoginReq  # noqa: E501
from openapi_server.models.payment_data_req import PaymentDataReq  # noqa: E501
from openapi_server.models.purchase_item import PurchaseItem  # noqa: E501
from openapi_server.models.purchase_start_req import PurchaseStartReq  # noqa: E501
from openapi_server import util

import openapi_server.dbmodels as dbm
from openapi_server.database import db_session as db

def auth(req):
    login = req.login
    client = dbm.Client.query.filter(dbm.Client.email == login.email).first()
    if login.password == client.password:
        return client
    return None


def app_end_purchase(payment_data_req=None):  # noqa: E501
    """End a purchase by the client

    Tries to end a purchase by either cancelling the purchase (does not include payment) or completing it(includes payment) # noqa: E501

    :param payment_data_req: 
    :type payment_data_req: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        payment_data_req = PaymentDataReq.from_dict(connexion.request.get_json())  # noqa: E501
    client = auth(payment_data_req)
    if not client:
        return "login failure", 403
    purchase = dbm.Purchase.query.filter(dbm.Purchase.client == client).one_or_none()
    if not purchase:
        return "no purchase", 404
    print("pay: " + str(payment_data_req.payment))
    db.delete(purchase)
    db.commit()
    return 'ok'


def get_current_purchase(login_req=None):  # noqa: E501
    """Get current purchase items

     # noqa: E501

    :param login_req: 
    :type login_req: dict | bytes

    :rtype: List[PurchaseItem]
    """
    if connexion.request.is_json:
        login_req = LoginReq.from_dict(connexion.request.get_json())  # noqa: E501
    client = auth(login_req)
    if not client:
        return "login failure", 403
    purchase = dbm.Purchase.query.filter(dbm.Purchase.client == client).one_or_none()
    if not purchase:
        return "no purchase", 404
    purchase_items = dbm.PurchaseItem.query.filter(dbm.PurchaseItem.purchase_id == purchase.id).join(dbm.Item).all()
    print(purchase_items)
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
    login = new_login_req.login
    client = dbm.Client(name=new_login_req.name, email=login.email, password=login.password)
    db.add(client)
    db.commit()
    return 'ok'


def start_purchase(purchase_start_req=None):  # noqa: E501
    """Start a purchase

     # noqa: E501

    :param purchase_start_req: 
    :type purchase_start_req: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        purchase_start_req = PurchaseStartReq.from_dict(connexion.request.get_json())  # noqa: E501
    client = auth(purchase_start_req)
    if not client:
        return "login failure", 403
    purchase = dbm.Purchase(client=client, cart=purchase_start_req.qr_code, vest_type=purchase_start_req.vest_type)
    db.add(purchase)
    db.commit()
    return 'ok'
