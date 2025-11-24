from flask import Blueprint

# Initialize the routes blueprint
routes_bp = Blueprint('routes', __name__)

# Import route definitions here
from . import example_routes  # Replace with actual route files as needed