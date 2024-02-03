from datetime import datetime


class Field:
    def __init__(self, value=None):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Phone(Field):
    def __init__(self, value=None):
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not new_value or not isinstance(new_value, str) or not new_value.isdigit():
            raise ValueError("Invalid phone number")
        self._value = new_value


class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        try:
            datetime.strptime(new_value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Use year-month-day (for example: 2002-10-12)")
        self._value = new_value


class Record:
    def __init__(self, phone=None, birthday=None):
        self._phone = Phone(phone)
        self._birthday = Birthday(birthday)

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, new_value):
        self._phone.value = new_value

    @property
    def birthday(self):
        return self._birthday

    @birthday.setter
    def birthday(self, new_value):
        self._birthday.value = new_value

    def days_to_birthday(self):
        if not self.birthday.value:
            return None
        today = datetime.today()
        next_birthday = datetime(today.year, datetime.strptime(self.birthday.value, "%Y-%m-%d").month, datetime.strptime(self.birthday.value, "%Y-%m-%d").day)
        if today > next_birthday:
            next_birthday = datetime(today.year + 1, datetime.strptime(self.birthday.value, "%Y-%m-%d").month, datetime.strptime(self.birthday.value, "%Y-%m-%d").day)
        days_remaining = (next_birthday - today).days
        return days_remaining


class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def iterator(self, chunk_size=5):
        for i in range(0, len(self.records), chunk_size):
            yield self.records[i:i + chunk_size]
