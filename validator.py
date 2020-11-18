from abc import ABCMeta, abstractmethod
import datetime
import time
import string

class Validator(metaclass=ABCMeta):
    types = {}

    def __init__(self):
        self._next = None

    @abstractmethod
    def validate(self, *args, **kwargs):
        pass


    @classmethod
    def get_isinstance(cls, name):
        klass = cls.types.get(name)
        if klass is None:
            raise ValidatorExceptions(f'Validator with name {name} not found')
        return klass(*args, **kwargs)


    @classmethod
    def add_type(cls, name, klass):
        if not name:
            raise ValidatorExceptions('Validator must have a name')
        if not issubclass(klass, Validator):
            raise ValidatorExceptions(f'Class "{klass}" is not Validator!')
        Validator.types[name] = klass

    def set_next(self, next):
        self._next = next

class ValidatorExceptions(Exception):
    pass

class EMailValidator(Validator):
    valid_range = string.ascii_letters + string.digits + '/\()"\':,.;<>~!@#$%^&*|+=[]{}`?-…'

    def get_valid_range(self):
        return self.valid_range

    def validate(self, value):
        if '@' not in value:
            return False
        user_host = value.strip().split('@')
        # print(user_host)
        if len(user_host) != 2:
            return False
        if len(user_host[0]) <=2 and len(user_host[1])<=2:
            return False
        for char in user_host[0]:
            if char not in self.get_valid_range():
                return False
        return True


class DateTimeValidator(Validator):
    def validate(self, value):
        date = value.replace('/', '-').replace('.', '-').replace('  ', ' ').strip()
        if len(date) <= 10:
            date += ' 00:00:00'
        elif 14 <= len(date) <= 16:
            date += ':00'

        try:
            if date.index('-') != 4:
                valid_date = time.strptime(date, '%d-%m-%Y %H:%M:%S')
            else:
                valid_date = time.strptime(date, '%Y-%m-%d %H:%M:%S')
            return True
        except ValueError:
            return False



class ChainValidator(Validator):
    def __init__(self, validators):
        self.validators = validators

    def validate(self, value):
        for i in self.validators:
            if not i.validate(value):
                return False
        return True


Validator.add_type('email', EMailValidator)
Validator.add_type('date', DateTimeValidator)
Validator.add_type('chain', ChainValidator)
