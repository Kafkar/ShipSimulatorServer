from flask import render_template

def register_start_routes(app):
    @app.route('/')
    def start_page():
        return render_template('start.html')