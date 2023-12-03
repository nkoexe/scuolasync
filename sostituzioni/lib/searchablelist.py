from beartype._decor.decormain import beartype
from beartype.typing import List, Tuple, Any


class SearchableList(List):
    """
    Essenzialmente semplicemente una lista, con funzionalità aggiunte di ricerca per id
    """

    @beartype
    def __init__(self, key_name: str | Tuple = 'id', values: list | None = None):
        super(SearchableList, self).__init__()

        self.key = key_name
        if values is not None:
            self.extend(values)

    def get(self, id, key: str | Tuple | None = None, default: Any = None):
        if key is None:
            key = self.key

        res = []

        if isinstance(key, str):
            for element in self:
                if isinstance(element, dict):
                    if element[key] == id:
                        res.append(element)
                elif isinstance(element, object):
                    if getattr(element, key) == id:
                        res.append(element)
                else:
                    raise TypeError(f'SearchableList.get: non è possibile ricercare elementi di tipo {type(element)}')

        elif isinstance(key, Tuple):
            for element in self:
                if isinstance(element, dict):
                    if all(element[k] == v for k, v in zip(key, id)):
                        res.append(element)
                elif isinstance(element, object):
                    if all(getattr(element, k) == v for k, v in zip(key, id)):
                        res.append(element)
                else:
                    raise TypeError(f'SearchableList.get: non è possibile ricercare elementi di tipo {type(element)}')

        if len(res) == 1:
            return res[0]
        elif len(res) > 1:
            return res

        return default

    def keys(self):
        id_list = []
        for element in self:
            id_list.append(getattr(element, self.key))

        return id_list


class Test:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return f'{self.a} {self.b}'


if __name__ == '__main__':
    a = SearchableList(key_name='a', values=[Test('ciao', 'buon'), Test('hello', 'good')])
    print(a.get('ciao'))
    print(a.get(('ciao', 'a'), ('a', 'b')))
