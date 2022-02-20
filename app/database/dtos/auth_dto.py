from app.database.database_manager import DatabaseManager


class AuthDto(DatabaseManager.DB.Model):
    __tablename__ = 'auth'

    username = DatabaseManager.DB.Column(DatabaseManager.DB.String, primary_key=True)
    password = DatabaseManager.DB.Column(DatabaseManager.DB.String)

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
