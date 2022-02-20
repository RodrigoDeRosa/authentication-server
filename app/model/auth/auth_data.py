from dataclasses import dataclass

from werkzeug.security import generate_password_hash, check_password_hash

from app.utils.authentication.password_utils import PasswordUtils


@dataclass
class AuthData:
    username: str
    password: str

    def __post_init__(self):
        if PasswordUtils.is_plain_password(self.password):
            self.password = generate_password_hash(self.password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)
