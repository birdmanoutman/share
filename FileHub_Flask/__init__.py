from flask import Flask


def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config['ROOT'] = 'C:\Users\dell\Desktop\share'  # Set your upload directory path here

    with app.app_context():
        from . import routes
        routes.setup_routes(app)

    return app
