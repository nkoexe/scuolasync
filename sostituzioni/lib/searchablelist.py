from beartype._decor.decormain import beartype
from beartype.typing import List


class SearchableList(List):
    """
    Essenzialmente semplicemente una lista, con funzionalità aggiunte di ricerca per id
    """

    @beartype
    def __init__(self, key_name: str = 'id', values: list | None = None):
        super(SearchableList, self).__init__()

        self.key = key_name
        if values is not None:
            self.extend(values)

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
