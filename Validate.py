

class Validate:

    def __init__(self, data = ''):
        self.data = data

    def __lower(self):
        lower = any(c.islower() for c in self.data)
        return lower

    def __upper(self):
        upper = any(c.isupper() for c in self.data)
        return upper

    def __digit(self):
        digit = any(c.isdigit() for c in  self.data)
        return digit

    def __symbol_exclude(self):
        symbol = not any(c in ' ;,?' for c in self.data)
        return symbol

    def __symbol_include(self):
        symbol = any(c in '!@#$%^&*()' for c in self.data)
        return symbol

    def validate_password(self):
        lower = self.__lower()
        upper = self.__upper()
        digit = self.__digit()
        symbol_in = self.__symbol_include()

        length = len(self.data)

        report = lower and upper and digit and length >= 6 and symbol_in

        if report:
            # Password passes all checks
            return True

        elif not lower:
            # Password requires lowercase letter
            return False

        elif not upper:
            # Password requires uppercase letters
            return False

        elif length < 7:
            # Password must be 7 or more characters
            return False

        elif not digit:
            # Password must contain a digit
            return False

    def validate_username(self):
        symbol_ex = self.__symbol_exclude()

        report = symbol_ex

        if report:
            # Username passes all checks
            return True

        elif not symbol_ex:
            # Password contains bad symbol
            return False