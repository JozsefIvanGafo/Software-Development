from ..order_management_exception import OrderManagementException
import re
class Attribute():
    def __init__(self):
        self.attr_value = ""
        self._error_message = ""
        self._validation_pattern = r""

    def _validate(self,value):
        myregex = re.compile(self._validation_pattern)
        res = myregex.fullmatch(value)
        if not res:
            raise OrderManagementException(self._error_message)
        return value

    @property
    def value(self):
        return self._attr_value
    @value.setter
    def value(self,value):
        self._attr_value = self._validate(value)

    def __str__(self):
        return self.__attr_value