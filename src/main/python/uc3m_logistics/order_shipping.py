"""Contains the class OrderShipping"""
from datetime import datetime
import hashlib
from .attributes.attribute_product_id import ProductId
from .attributes.attribute_order_id import OrderID
from .attributes.attribute_contact_email import ContactEmail
from .order_request import OrderRequest
from .send_input_file import SendInput


#pylint: disable=too-many-instance-attributes
class OrderShipping():
    """Class representing the shipping of an order"""

    def __init__(self, product_id, order_id, delivery_email, order_type):
        self.__alg = "SHA-256"
        self.__type = "DS"
        self.__product_id = ProductId(product_id).value
        self.__order_id = OrderID(order_id).value
        self.__delivery_email = ContactEmail(delivery_email).value
        justnow = datetime.utcnow()
        self.__issued_at = datetime.timestamp(justnow)
        if order_type == "Regular":
            delivery_days = 7
        else:
            delivery_days = 1
        #timestamp is represneted in seconds.microseconds
        #__delivery_day must be expressed in senconds to be added to the timestap
        self.__delivery_day = self.__issued_at + (delivery_days * 24 * 60 * 60)
        self.__tracking_code = hashlib.sha256(self.__signature_string().encode()).hexdigest()

    def __signature_string( self ):
        """Composes the string to be used for generating the tracking_code"""
        return "{alg:" + self.__alg + ",typ:" + self.__type + ",order_id:" + \
               self.__order_id + ",issuedate:" + str(self.__issued_at) + \
               ",deliveryday:" + str(self.__delivery_day) + "}"

    @property
    def product_id( self ):
        """Property that represents the product_id of the order"""
        return self.__product_id

    @product_id.setter
    def product_id( self, value ):
        self.__product_id = value

    @property
    def order_id( self ):
        """Property that represents the order_id"""
        return self.__order_id

    @order_id.setter
    def order_id( self, value ):
        self.__order_id = value

    @property
    def email( self ):
        """Property that represents the email of the client"""
        return self.__delivery_email

    @email.setter
    def email( self, value ):
        self.__delivery_email = value

    @property
    def tracking_code( self ):
        """returns the tracking code"""
        return self.__tracking_code

    @property
    def issued_at( self ):
        """Returns the issued at value"""
        return self.__issued_at

    @issued_at.setter
    def issued_at( self, value ):
        self.__issued_at = value

    @property
    def delivery_day( self ):
        """Returns the delivery day for the order"""
        return self.__delivery_day

    @classmethod
    def get_order_shipping(cls,input_file):
        """Method that returns object OrderShipping"""
        send_input_file = SendInput(input_file)
        order = OrderRequest.get_order_by_order_id(send_input_file.order_id)
        my_order_shipping = OrderShipping(product_id=order.product_id,
                                    order_id=order.order_id,
                                    order_type=order.order_type,
                                    delivery_email=send_input_file.contact_email)
        return my_order_shipping
