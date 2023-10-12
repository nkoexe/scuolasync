import sys
from io import StringIO


class RedirectedStdout:
    def __init__(self):
        self._stdout = None
        self._stderr = None
        self._string_io = None

    def __enter__(self):
        self._string_io = StringIO()
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        sys.stdout = self._string_io
        sys.stderr = self._string_io
        return self

    def __exit__(self, type, value, traceback):
        sys.stdout = self._stdout
        sys.stderr = self._stderr

    def __str__(self):
        return self._string_io.getvalue()
