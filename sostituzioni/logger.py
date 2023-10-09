import logging

logger = logging
logger.basicConfig(level=logging.DEBUG)

logging.getLogger('geventwebsocket.handler').setLevel(logging.ERROR)
logging.getLogger('werkzeug').setLevel(logging.ERROR)
