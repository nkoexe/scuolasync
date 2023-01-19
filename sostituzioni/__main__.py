#!/usr/bin/env python

"""
descr
"""

import logging
from sostituzioni.view import main


logging.basicConfig(level=logging.DEBUG)
logging.getLogger('geventwebsocket.handler').setLevel(logging.ERROR)
logging.getLogger('werkzeug').setLevel(logging.ERROR)


if __name__ == '__main__':
    main()
