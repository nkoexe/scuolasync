import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(levelname)s - %(asctime)s - %(name)s - %(message)s"
)


# logging.getLogger('geventwebsocket.handler').setLevel(logging.ERROR)
# logging.getLogger('werkzeug').setLevel(logging.ERROR)
# logging.getLogger('socketio').setLevel(logging.ERROR)
# logging.getLogger('engineio').setLevel(logging.ERROR)
# logging.getLogger('urllib3').setLevel(logging.ERROR)
