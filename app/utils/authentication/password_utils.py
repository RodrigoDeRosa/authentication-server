import re


class PasswordUtils:

    PASSWORD_REQUIREMENTS_READABLE = \
        'At least 8 characters with 1 number, 1 lower case character and 1 upper case character'
    __VALID_PASSWORD_REGEX = re.compile(r'(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{8,})')

    @classmethod
    def verify_password(cls, password: str) -> bool:
        """ Validate a given password against valid password's regex. """
        return cls.__VALID_PASSWORD_REGEX.match(password) is not None
