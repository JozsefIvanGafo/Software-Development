"""MODULE: order_request. Contains the order request class"""
import hashlib
import json
from datetime import datetime
from .order_management_exception import OrderManagementException
import re
from .attributes.attribute_phone_number import PhoneNumber
from .attributes.attribute_product_id import PoductId
class OrderRequest:
    """Class representing the register of the order in the system"""
    #pylint: disable=too-many-arguments
    def __init__( self, product_id, order_type,
                  delivery_address, phone_number, zip_code ):
        self.__product_id = ProductID()
        self.__delivery_address = self.validate_address(delivery_address)
        self.__order_type = self.validate_order_type(order_type)
        self.__phone_number = PhoneNumber(phone_number).value
        self.__zip_code = self.validate_zip_code(zip_code)
        justnow = datetime.utcnow()
        self.__time_stamp = datetime.timestamp(justnow)
        self.__order_id =  hashlib.md5(self.__str__().encode()).hexdigest()

    def __str__(self):
        return "OrderRequest:" + json.dumps(self.__dict__)

    @property
    def delivery_address( self ):
        """Property representing the address where the product
        must be delivered"""
        return self.__delivery_address

    @delivery_address.setter
    def delivery_address( self, value ):
        self.__delivery_address = value

    @property
    def order_type( self ):
        """Property representing the type of order: REGULAR or PREMIUM"""
        return self.__order_type
    @order_type.setter
    def order_type( self, value ):
        self.__order_type = value

    @property
    def phone_number( self ):
        """Property representing the clients's phone number"""
        return self.__phone_number
    @phone_number.setter
    def phone_number( self, value ):
        self.__phone_number = PhoneNumber(value).value

    @property
    def product_id( self ):
        """Property representing the products  EAN13 code"""
        return self.__product_id
    @product_id.setter
    def product_id( self, value ):
        self.__product_id = value

    @property
    def time_stamp(self):
        """Read-only property that returns the timestamp of the request"""
        return self.__time_stamp

    @property
    def order_id( self ):
        """Returns the md5 signature"""
        return self.__order_id

    @property
    def zip_code( self ):
        """Returns the order's zip_code"""
        return self.__zip_code

    def validate_zip_code(self, zip_code):
        if zip_code.isnumeric() and len(zip_code) == 5:
            if (int(zip_code) > 52999 or int(zip_code) < 1000):
                raise OrderManagementException("zip_code is not valid")
        else:
            raise OrderManagementException("zip_code format is not valid")
        return zip_code

    def validate_order_type(self, order_type):
        myregex = re.compile(r"(Regular|Premium)")
        res = myregex.fullmatch(order_type)
        if not res:
            raise OrderManagementException("order_type is not valid")
        return order_type

    def validate_address(self, address):
        myregex = re.compile(r"^(?=^.{20,100}$)(([a-zA-Z0-9]+\s)+[a-zA-Z0-9]+)$")
        res = myregex.fullmatch(address)
        if not res:
            raise OrderManagementException("address is not valid")
        return address