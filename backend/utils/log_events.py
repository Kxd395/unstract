import logging
import os
import threading
import time
from typing import Any

import redis
import socketio
from django.conf import settings
from django.core.wsgi import WSGIHandler
from django.dispatch import Signal

# Define a signal
log_received = Signal()
logger = logging.getLogger(__name__)

sio = socketio.Server(
    # Allowed values: {threading, eventlet, gevent, gevent_uwsgi}
    async_mode="threading",
    cors_allowed_origins=settings.CORS_ALLOWED_ORIGINS,
    logger=False,
    engineio_logger=False,
    always_connect=True,
)
redis_conn = redis.Redis(
    host=settings.REDIS_HOST,
    port=int(settings.REDIS_PORT),
    username=settings.REDIS_USER,
    password=settings.REDIS_PASSWORD,
)


@sio.event
def connect(sid: str, environ: Any, auth: Any) -> None:
    # TODO Authenticate websocket connections
    logger.info(f"[{os.getpid()}] Client with SID:{sid} connected")


@sio.event
def disconnect(sid: str) -> None:
    logger.info(f"[{os.getpid()}] Client with SID:{sid} disconnected")


def _store_execution_log(data: bytes) -> None:
    """Store execution log in database
    Args:
        data (bytes): Execution log data in bytes format
    """
    try:
        log_received.send_robust(sender=None, data=data)
    except Exception as e:
        logger.error(f"Error storing execution log: {e}")


def _emit_websocket_event(channel: str, data: bytes) -> None:
    """Emit websocket event
    Args:
        channel (str): WebSocket channel
        data (bytes): Execution log data in bytes format
    """
    payload = {"data": data}
    try:
        logger.debug(f"[{os.getpid()}] Push websocket event: {channel}, {payload}")
        sio.emit(channel, payload)
    except Exception as e:
        logger.error(f"Error emitting WebSocket event: {e}")


def _handle_pubsub_messages(message: dict[str, Any]) -> None:
    """Handle pubsub messages
    Args:
        message (dict[str, Any]): Pub sub message
    """
    channel = message.get("channel")
    data = message.get("data")

    if not channel or not data:
        logger.warning(f"Invalid message received: {message}")
        return

    try:
        channel_str = channel.decode("utf-8")
    except UnicodeDecodeError as e:
        logger.error(f"Error decoding channel: {e}")
        return

    _store_execution_log(data)
    _emit_websocket_event(channel_str, data)


def _pubsub_listen_forever() -> None:
    global shutdown

    try:
        pubsub = redis_conn.pubsub(ignore_subscribe_messages=True)
        pubsub.psubscribe("logs:*")

        logger.info(f"[{os.getpid()}] Listening for pub sub messages...")
        while True:
            message = pubsub.get_message()

            if message:
                logger.debug(f"[{os.getpid()}] Pub sub message received: {message}")
                if message["type"] == "pmessage":
                    _handle_pubsub_messages(message)

            # TODO Add graceful shutdown

            time.sleep(0.01)
    except Exception as e:
        logger.error(f"[{os.getpid()}] Failed to do pubsub: {e}")


def start_server(django_app: WSGIHandler, namespace: str) -> WSGIHandler:
    django_app = socketio.WSGIApp(sio, django_app, socketio_path=namespace)

    pubsub_listener = threading.Thread(target=_pubsub_listen_forever, daemon=True)
    pubsub_listener.start()

    return django_app
