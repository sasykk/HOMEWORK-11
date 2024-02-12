from collections import UserDict
from datetime import datetime, date


class Field:

    def __init__(self, value):
        if self.is_valid(value):
            self.value = value
        else:
            raise ValueError

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if self.is_valid(value):
            self.__value = value
        else:
            raise ValueError

    def __eq__(self, other):
        return self.__value == other

    def __ne__(self, other):
        return self.__value != other
    
    def is_valid(self, value):
        return True

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):

    def is_valid(self, value):
        value = str(value)
        if value.isdigit() and len(value) == 10:
            return True
        else:
            return False


class Birthday(Field):

    def is_valid(self, value):
        try:
            date(*[int(x) for x in value.split()])
            return True
        except ValueError:
            return False


class Record:

    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phones = []
        if phone:
            self.phones.append(Phone(phone))
        self.birthday = Birthday(birthday) if birthday else None

    def days_to_birthday(self):
        if self.birthday:
            bday = date(*[int(x) for x in str(self.birthday.value).split()])
            current_date = datetime.now()
            next_birthday = datetime(current_date.year, bday.month, bday.day)
            if current_date > next_birthday:
                next_birthday = datetime(current_date.year + 1, bday.month, bday.day)
            delta = next_birthday - current_date
            return delta.days
        return None

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def edit_phone(self, phone, new_phone):
        for ph in self.phones:
            if ph.value == phone:
                if ph.is_valid(new_phone):
                    ph.value = new_phone
                    break
                else:
                    raise ValueError("Invalid phone number")
        else:
            raise ValueError("Phone not found in record")
        
    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.pop(self.phones.index(phone))
        else:
            raise ValueError

    def find_phone(self, item):
        if item in self.phones:
            return Phone(item)
        else:
            return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):

    def __init__(self):
        super().__init__()

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        try:
            return self.data[name]
        except KeyError:
            return None

    def delete(self, name):
        if name in self.data.keys():
            self.data.pop(name)
        else:
            return None

    def iterator(self, n=3):
        records = list(self.data.values())
        for i in range(0, len(records), n):
            yield records[i: i+n]
