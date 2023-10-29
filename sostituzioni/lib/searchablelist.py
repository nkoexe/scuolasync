from beartype._decor.decormain import beartype
from beartype.typing import List


class SearchableList(List):
    """
    Essenzialmente semplicemente una lista, con funzionalità aggiunte di ricerca per id
    """

    @beartype
    def __init__(self, key_name: str = 'id'):
        super().__init__(self)
        self.key = key_name

    def __getitem__(self, id):
        for element in self:
            if getattr(element, self.key) == id:
                return element

        return None

    def get(self, id, key_name):
        # todo complete, get ma con una key personalizzata
        for element in self:
            if getattr(element, self.key) == id:
                return element

        return None

    def keys(self):
        id_list = []
        for element in self:
            id_list.append(getattr(element, self.key))

        return id_list


class Test:
    def __init__(self) -> None:
        self.aa = 'pasta'


lista = SearchableList('aa')

tes = Test()
lista.append(tes)
print(lista['pasta'])
