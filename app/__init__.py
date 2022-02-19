from flask import Flask


def create_app():
    app = Flask(__name__)
    # Avoid imports on `import app`
    from app.server.server_configurator import ServerConfigurator
    ServerConfigurator.configure(app)
    return app
