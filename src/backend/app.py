from flask import Flask
from src.backend.routes import init_routes
from src.backend.services.auth import AuthService

def create_app():
    app = Flask(__name__)

    # Initialize middleware and configurations
    app.config['SECRET_KEY'] = 'your_secret_key_here'

    # Initialize authentication service
    auth_service = AuthService()

    # Initialize routes
    init_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)