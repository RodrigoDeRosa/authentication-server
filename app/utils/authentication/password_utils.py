import re


class PasswordUtils:

    PASSWORD_REQUIREMENTS_READABLE = \
        'Between 8 and 20 characters with 1 number, 1 lower case character and 1 upper case character'
    __VALID_PASSWORD_REGEX = re.compile(r'(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{8,20})')

    @classmethod
    def verify_password(cls, password: str) -> bool:
        return cls.__VALID_PASSWORD_REGEX.match(password) is not None

    @classmethod
    def is_plain_password(cls, password: str) -> bool:
        # There's a hard limit on 20 characters for user passwords and hashes
        # are always (way) longer than that. This is sort of a hack but seems
        # like one of the better options
        return len(password) <= 20
