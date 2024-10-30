from utils.auth import AuthService

class UserService:
    def __init__(self):
        self.auth_service = AuthService()

    def register_user(self, username, password, role):
        return self.auth_service.register_user(username, password, role)

    def login_user(self, username, password):
        return self.auth_service.login_user(username, password)

    def close_connection(self):
        self.auth_service.disconnect()
