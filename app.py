from flask import Flask
from extensions import db, jwt
from routes.user_routes import user_bp
from routes.operation_routes import operation_bp
from routes.auction_routes import auction_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(operation_bp, url_prefix='/api/operations')
    app.register_blueprint(auction_bp, url_prefix='/api/auctions')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
