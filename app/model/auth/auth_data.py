from dataclasses import dataclass

from werkzeug.security import generate_password_hash, check_password_hash


@dataclass
class AuthData:
    username: str
    password: str

    def encrypt(self):
        self.password = generate_password_hash(self.password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    @classmethod
    def compulsory_fields(cls):
        return dict(cls.__annotations__)
