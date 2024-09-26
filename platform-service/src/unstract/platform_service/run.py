import logging
from logging.config import dictConfig
from typing import Any

from dotenv import load_dotenv
from flask import Flask
from unstract.platform_service.constants import LogLevel
from unstract.platform_service.controller import api
from unstract.platform_service.controller.platform import be_db
from unstract.platform_service.env import Env

load_dotenv()

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": (
                    "[%(asctime)s] %(levelname)s in"
                    " %(name)s (%(module)s): %(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S %z",
            },
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            },
        },
        "loggers": {
            "werkzeug": {
                "level": Env.LOG_LEVEL,
                "handlers": ["wsgi"],
                "propagate": False,
            },
            "gunicorn.access": {
                "level": Env.LOG_LEVEL,
                "handlers": ["wsgi"],
                "propagate": False,
            },
            "gunicorn.error": {
                "level": Env.LOG_LEVEL,
                "handlers": ["wsgi"],
                "propagate": False,
            },
        },
        "root": {
            "level": Env.LOG_LEVEL,
            "handlers": ["wsgi"],
        },
    }
)

LOGGING_LEVELS = {
    LogLevel.DEBUG: logging.DEBUG,
    LogLevel.INFO: logging.INFO,
    LogLevel.WARNING: logging.WARNING,
    LogLevel.ERROR: logging.ERROR,
    LogLevel.CRITICAL: logging.CRITICAL,
}


def create_app() -> Flask:
    app = Flask("platform-service")

    # Set logging level
    logging_level = LOGGING_LEVELS.get(Env.LOG_LEVEL, logging.INFO)
    app.logger.setLevel(logging_level)
    app.register_blueprint(api)

    return app


app = create_app()


@app.before_request
def before_request() -> None:
    if be_db.is_closed():
        be_db.connect(reuse_if_open=True)


@app.teardown_request
def after_request(exception: Any) -> None:
    # Close the connection after each request
    if not be_db.is_closed():
        be_db.close()


if __name__ == "__main__":
    # Start the server
    app.run(host="0.0.0.0", port=3001, load_dotenv=True)
