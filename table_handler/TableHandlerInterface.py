import os
import csv

from abc import ABC, abstractmethod

from typing import List

class TableHandlerInterface(ABC):
    def __init__(self, cmd_list: List[str]) -> None:
        self._cmd_list=cmd_list
        
        self._tables=self._cmd_list[0]
        self._columns=self._cmd_list[1]
        self._values=self._cmd_list[2]
        self._math_operators=self._cmd_list[3]
        self._logical_operators=self._cmd_list[4]

        self._abs_table_path=None
        self._validate()

        self._execute()
    
    @abstractmethod
    def _validate(self) -> None:
        pass

    def _tables_exist(self) -> bool:
        table_path=os.path.join("../database_manager/data/tables", self._tables[0].lower()+".csv")
        absolute_path=os.path.abspath(table_path)
        self._abs_table_path=absolute_path
        return os.path.isfile(absolute_path)
    
    def _validate(self) -> None:
        if not self._tables_exist():
            raise Exception(f"Tabela {self._tables[0]} não existente!")
        
        if not self._columns_exist():
            raise Exception("Colunas incorretas!")
        
    def _columns_exist(self) -> bool:
        with open(self._abs_table_path, "r", newline="") as file:
            csv_reader=csv.reader(file)
            file_headers=next(csv_reader, None)
            
            for i in range(0, len(file_headers)):
                file_headers[i]=file_headers[i].upper()

            for column in self._columns:
                if column not in file_headers:
                    return False
                
            return True
    
    @abstractmethod
    def _execute(self) -> None:
        pass

    def _get_registers(self) -> List:
        with open(self._abs_table_path, "r", newline="") as file:
            csv_reader=csv.DictReader(file)

            registers=[]

            for register in csv_reader:
                registers.append(register)
        
        return registers
