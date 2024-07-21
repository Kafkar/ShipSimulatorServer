from .start_page import register_start_routes
from .tank import register_tank_routes


def register_all_routes(app, tank_control):
    register_start_routes(app)
    register_tank_routes(app, tank_control)