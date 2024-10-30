from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from database.db_mysql import MySQLDatabase

class AuthService:
    def __init__(self):
        self.db = MySQLDatabase()
        self.db.connect()  # Conéctate a la base de datos al inicializar el servicio

    def register_user(self, username, password, role):
        if not username or not password or not role:
            return {"message": "Username, password, and role are required"}, 400

        hashed_password = generate_password_hash(password)
        query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
        affected_rows = self.db.execute_update(query, (username, hashed_password, role))

        if affected_rows == 0:
            return {"message": "Username already taken"}, 400

        return {"message": "User registered successfully"}, 201

    def login_user(self, username, password):
        if not username or not password:
            return {"message": "Username and password are required"}, 400

        query = "SELECT * FROM users WHERE username = %s"
        users = self.db.execute_query(query, (username,))
        
        if not users:
            return {"message": "Invalid credentials"}, 401
        
        user = users[0]
        
        if check_password_hash(user['password'], password):
            access_token = create_access_token(identity={"username": username, "role": user['role']})
            return {"access_token": access_token}, 200
        
        return {"message": "Invalid credentials"}, 401

    def disconnect(self):
        self.db.disconnect()  # Cierra la conexión cuando ya no sea necesaria
