import connexion
import six

from openapi_server.models.new_login_req import NewLoginReq  # noqa: E501
from openapi_server.models.payment_data_req import PaymentDataReq  # noqa: E501
from openapi_server.models.purchase_item import PurchaseItem  # noqa: E501
from openapi_server.models.purchase_start_req import PurchaseStartReq  # noqa: E501
from openapi_server import util

import openapi_server.dbmodels as dbm
from openapi_server.database import db_session as db

def app_end_purchase(user, payment_data_req=None):  # noqa: E501
    """End a purchase by the client

    Tries to end a purchase by either cancelling the purchase (does not include payment) or completing it(includes payment) # noqa: E501

    :param payment_data_req: 
    :type payment_data_req: dict | bytes

    :rtype: int
    """
    if connexion.request.is_json:
        payment_data_req = PaymentDataReq.from_dict(connexion.request.get_json())  # noqa: E501
    purchase = dbm.Purchase.query.filter(dbm.Purchase.client == user).one_or_none()
    if not purchase:
        return "no purchase", 404
    print("pay: " + str(payment_data_req.payment))
    if payment_data_req.payment:
      purchase_items = dbm.ItemPurchase.query.join(dbm.Item).filter(dbm.ItemPurchase.purchase_id == purchase.id).filter(dbm.ItemPurchase.item_rfid_code == dbm.Item.rfid_code).all()
      total = sum([pi.item.price * pi.amount for pi in purchase_items])
      db.delete(purchase)
      db.commit()
      return total, 200
    else:
      db.delete(purchase)
      db.commit()
      return 'purchase aborted', 204


def get_current_purchase(user):  # noqa: E501
    """Get current purchase items

     # noqa: E501


    :rtype: List[PurchaseItem]
    """
    if connexion.request.is_json:
        login_req = LoginReq.from_dict(connexion.request.get_json())  # noqa: E501
    purchase = dbm.Purchase.query.filter(dbm.Purchase.client == user).one_or_none()
    if not purchase:
        return "no purchase", 404
    purchase_items = dbm.ItemPurchase.query.join(dbm.Item).filter(dbm.ItemPurchase.purchase_id == purchase.id).filter(dbm.ItemPurchase.item_rfid_code == dbm.Item.rfid_code).all()
    print(purchase_items)
    print(list(purchase_items))
    return [PurchaseItem(name=pi.item.name, price=pi.item.price, amount=pi.amount) for pi in purchase_items]


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


def start_purchase(user, purchase_start_req=None):  # noqa: E501
    """Start a purchase

     # noqa: E501

    :param purchase_start_req: 
    :type purchase_start_req: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        purchase_start_req = PurchaseStartReq.from_dict(connexion.request.get_json())  # noqa: E501
    purchase = dbm.Purchase(client=user, cart=purchase_start_req.qr_code, vest_type=purchase_start_req.vest_type)
    db.add(purchase)
    db.commit()
    return 'ok'
