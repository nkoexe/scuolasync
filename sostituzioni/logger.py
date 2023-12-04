import logging

logger = logging
logger.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logging.getLogger('geventwebsocket.handler').setLevel(logging.ERROR)
logging.getLogger('werkzeug').setLevel(logging.ERROR)
