#!/usr/bin/env python

"""
descr
"""

import logging

from view import create_app, socketio


logging.basicConfig(level=logging.DEBUG)

app = create_app()


def main():
    socketio.run(app, '0.0.0.0', debug=True)


if __name__ == '__main__':
    main()
