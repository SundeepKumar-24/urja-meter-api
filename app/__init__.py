
import os
from flask import Flask
from dotenv import load_dotenv
from .routes import api


def create_app(overrides=None):
    # Load environment variables from the project-root .env file.
    load_dotenv()

    app = Flask(__name__)

    app.config.update({
        "PORTAL_BASE_URL": os.getenv("PORTAL_BASE_URL", ""),
        "PORTAL_METERS_URL": os.getenv("PORTAL_METERS_URL", ""),
        "PORTAL_TRANSFORMERS_URL": os.getenv(
            "PORTAL_TRANSFORMERS_URL", ""
        ),
        "PORTAL_ENERGY_URL": os.getenv("PORTAL_ENERGY_URL", ""),
        "PORTAL_GEO_URL": os.getenv("PORTAL_GEO_URL", ""),
        "PORTAL_COOKIE": os.getenv("PORTAL_COOKIE", ""),
        "PORTAL_BEARER_TOKEN": os.getenv("PORTAL_BEARER_TOKEN", ""),
        "REQUEST_TIMEOUT_SECONDS": int(
            os.getenv("REQUEST_TIMEOUT_SECONDS", "15")
        ),
    })

    # Allow tests to override configuration.
    if overrides:
        app.config.update(overrides)

    app.register_blueprint(api)

    return app
