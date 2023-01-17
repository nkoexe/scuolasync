#!/usr/bin/env python

"""
descr
"""

import logging

logging.basicConfig(level=logging.DEBUG)

from sostituzioni.view import create_app, socketio
# from sostituzioni.control.configurazione import configurazione


app = create_app()


def main():
    socketio.run(app, '0.0.0.0', debug=True)


if __name__ == '__main__':
    main()
