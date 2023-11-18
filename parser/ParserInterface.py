from abc import ABC, abstractmethod
from typing import List

class ParserInterface(ABC):
    def __init__(self, cmd_list: str) -> None:
        self._cmd_list=cmd_list

    def _execute(self) -> List:
        self._parser()

        tables=self._get_tables()
        columns=self._get_columns()
        values=self._get_values()
        math_operators=self._get_math_operators()
        logical_operators=self._get_logical_operators()

        return [tables, columns, values, math_operators, logical_operators]
    
    @abstractmethod
    def _parser(self) -> None:
        pass
    
    @abstractmethod
    def _get_tables(self) -> List[str]:
        pass

    @abstractmethod
    def _get_columns(self) -> List[str]:
        pass

    @abstractmethod
    def _get_values(self) -> List[str]:
        pass

    @abstractmethod
    def _get_math_operators(self) -> List[str]:
        pass

    @abstractmethod
    def _get_logical_operators(self) -> List[str]:
        pass
