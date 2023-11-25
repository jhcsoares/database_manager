from abc import ABC, abstractmethod
from typing import List

class DBHandlerInterface(ABC):
    def __init__(self, cmd_list: List[str]) -> None:
        self._connection=None
        self._table=None
        self._data_base=None

        if not self._connection:
            self._db_setup={
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": cmd_list[1]
            }

        self._validate()
    
    @abstractmethod
    def _validate(self) -> None:
        pass

    @abstractmethod
    def _execute(self, cmd_list: List[str]) -> None:
        pass
