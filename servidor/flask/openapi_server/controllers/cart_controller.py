import connexion
import six

from openapi_server.models.cart_status import CartStatus  # noqa: E501
from openapi_server.models.item_data import ItemData  # noqa: E501
from openapi_server import util

import openapi_server.dbmodels as dbm
from openapi_server.database import db_session as db


def cart_alter_item(rfid_code, purchase_id, body):  # noqa: E501
    """alter amount of item in purchase

     # noqa: E501

    :param rfid_code: Item rfid_code
    :type rfid_code: int
    :param purchase_id: 
    :type purchase_id: int
    :param body: 
    :type body: int

    :rtype: None
    """
    purchase = dbm.Purchase.query.filter(dbm.Purchase.id == purchase_id).one_or_none()
    if not purchase:
        return "purchase not found", 404
    itempurchase = dbm.Purchase.query.join(dbm.ItemPurchase).filter(dbm.Purchase.id == purchase_id).filter(dbm.ItemPurchase.item_rfid_code == rfid_code).first()
    if not itempurchase:
        itempurchase = dbm.ItemPurchase(item_rfid_code=rfid_code, purchase_id=purchase_id, amount=body)
        db.add(itempurchase)
    else:
        itempurchase.amount = body
    print(itempurchase)
    db.commit()
    return 'ok'


def cart_check_on_purchase(qr_code):  # noqa: E501
    """maybe get current purchase data for a cart

     # noqa: E501

    :param qr_code: Cart qr_code
    :type qr_code: str

    :rtype: CartStatus
    """
    purchase = dbm.Purchase.query.filter(dbm.Purchase.cart == qr_code).one_or_none()
    if not purchase:
        return "not in purchase", 404
    return CartStatus(purchase=purchase.id, vest_type=purchase.vest_type)


def cart_end_purchase(qr_code):  # noqa: E501
    """Ending purchase

     # noqa: E501

    :param qr_code: Cart qr_code
    :type qr_code: str

    :rtype: None
    """
    purchase = dbm.Purchase.query.filter(dbm.Purchase.cart == qr_code).one_or_none()
    if not purchase:
        return "not in purchase", 404
    purchase.cart = None
    db.commit()
    return "ok"


def get_item_data(rfid_code):  # noqa: E501
    """get item data

     # noqa: E501

    :param rfid_code: Item rfid_code
    :type rfid_code: int

    :rtype: ItemData
    """
    item = dbm.Item.query.filter(dbm.Item.rfid_code == rfid_code).one_or_none()
    if not item:
        return "Item not found", 404
    return ItemData(name=item.name, price=item.price, weight=item.weight)
