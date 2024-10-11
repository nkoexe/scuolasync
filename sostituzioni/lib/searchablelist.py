"""
    This file is part of ScuolaSync.

    Copyright (C) 2023-present Niccolò Ragazzi <hi@njco.dev>

    ScuolaSync is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with ScuolaSync.  If not, you can find a copy at
    <https://www.gnu.org/licenses/agpl-3.0.html>.
"""

from beartype import beartype
from beartype.typing import List, Tuple, Any


class SearchableList(List):
    """
    Essenzialmente semplicemente una lista, con funzionalità aggiunte di ricerca per id
    """

    @beartype
    def __init__(self, key_name: str | Tuple = "id", values: list | None = None):
        super(SearchableList, self).__init__()

        self.key = key_name
        if values is not None:
            self.extend(values)

    @beartype
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
                    raise TypeError(
                        f"SearchableList.get: non è possibile ricercare elementi di tipo {type(element)}"
                    )

        elif isinstance(key, Tuple):
            for element in self:
                if isinstance(element, dict):
                    if all(element[k] == v for k, v in zip(key, id)):
                        res.append(element)
                elif isinstance(element, object):
                    if all(getattr(element, k) == v for k, v in zip(key, id)):
                        res.append(element)
                else:
                    raise TypeError(
                        f"SearchableList.get: non è possibile ricercare elementi di tipo {type(element)}"
                    )

        if len(res) == 1:
            return res[0]
        elif len(res) > 1:
            return res

        return default

    @beartype
    def get_all(self, id, key: str | Tuple | None = None):
        if key is None:
            key = self.key

        if isinstance(key, str):
            for element in self:
                if isinstance(element, dict):
                    if element[key] == id:
                        yield element
                elif isinstance(element, object):
                    if getattr(element, key) == id:
                        yield element
                else:
                    raise TypeError(
                        f"SearchableList.get: non è possibile ricercare elementi di tipo {type(element)}"
                    )

        elif isinstance(key, Tuple):
            for element in self:
                if isinstance(element, dict):
                    if all(element[k] == v for k, v in zip(key, id)):
                        yield element
                elif isinstance(element, object):
                    if all(getattr(element, k) == v for k, v in zip(key, id)):
                        yield element
                else:
                    raise TypeError(
                        f"SearchableList.get: non è possibile ricercare elementi di tipo {type(element)}"
                    )

    def keys(self):
        return [getattr(element, self.key) for element in self]

    @beartype
    def index(self, id, key: str | Tuple | None = None):
        if key is None:
            key = self.key

        if isinstance(key, str):
            for index, element in enumerate(self):
                if isinstance(element, dict):
                    if element[key] == id:
                        return index
                elif isinstance(element, object):
                    if getattr(element, key) == id:
                        return index
                else:
                    raise TypeError(
                        f"SearchableList.get: non è possibile ricercare elementi di tipo {type(element)}"
                    )
            return -1

        elif isinstance(key, Tuple):
            for index, element in enumerate(self):
                if isinstance(element, dict):
                    if all(element[k] == v for k, v in zip(key, id)):
                        return index
                elif isinstance(element, object):
                    if all(getattr(element, k) == v for k, v in zip(key, id)):
                        return index
                else:
                    raise TypeError(
                        f"SearchableList.get: non è possibile ricercare elementi di tipo {type(element)}"
                    )
            return -1


class Test:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return f"{self.a} {self.b}"


if __name__ == "__main__":
    a = SearchableList(
        key_name="a", values=[Test("ciao", "buon"), Test("hello", "good")]
    )
    print(a.get("ciao"))
    print(a.get(("ciao", "a"), ("a", "b")))
