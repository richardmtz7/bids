class User():
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
    
    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'role': self.role
        }
