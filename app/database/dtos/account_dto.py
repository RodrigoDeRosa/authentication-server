from app.database.database_manager import DatabaseManager


class AccountDto(DatabaseManager.DB.Model):
    __tablename__ = 'account'

    username = DatabaseManager.DB.Column(DatabaseManager.DB.String, primary_key=True)
    first_name = DatabaseManager.DB.Column(DatabaseManager.DB.String)
    last_name = DatabaseManager.DB.Column(DatabaseManager.DB.String)

    def __init__(self, username: str, first_name: str, last_name: str) -> None:
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
