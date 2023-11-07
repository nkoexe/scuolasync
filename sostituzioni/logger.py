import logging

logger = logging
logger.basicConfig(level=logging.WARNING)

logging.getLogger('geventwebsocket.handler').setLevel(logging.ERROR)
logging.getLogger('werkzeug').setLevel(logging.ERROR)
