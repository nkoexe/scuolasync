"""
database controller
"""

import sqlite3

from sostituzioni.control.configurazione import configurazione


class Database:
    def __init__(self):
        con = sqlite3.connect("test.db")

    def crea_database(self):
        pass

    class ElementoDatabase():
        def __init__(self):
            super().__init__()

        def modifica(self):
            pass

        def salva(self):
            pass

    class ElementoConStorico(ElementoDatabase):
        def __init__(self):
            self._cancellato = False

            self.elimina = self.cancella = self.__del__

        def __del__(self, mantieni_in_storico: bool = True):
            self._cancellato = True

        @property
        def cancellato(self):
            return self._cancellato


database = Database()
