import csv
import os

from typing import List

class TableHandler:
    def __init__(self, cmd_list: List[str]):
        self.__cmd_list=cmd_list
        
        self.__table=self.__cmd_list[0][0]
        self.__columns=self.__cmd_list[1]
        self.__values=self.__cmd_list[2]

        self.__abs_table_path=None
        self.__validate_insert()

        self.__insert()

    def __validate_insert(self):
        if not self.__table_exists():
            raise Exception(f"Tabela {self.__table} não existente!")
        
        if not self.__columns_exists():
            raise Exception("Colunas incorretas!")

    def __table_exists(self) -> bool:
        table_path=os.path.join("../database_manager/data/tables", self.__table.lower()+".csv")
        absolute_path=os.path.abspath(table_path)
        self.__abs_table_path=absolute_path
        return os.path.isfile(absolute_path)
    
    def __columns_exists(self) -> bool:
        with open(self.__abs_table_path, "r", newline="") as file:
            csv_reader=csv.reader(file)
            file_headers=next(csv_reader, None)
            
            for i in range(0, len(file_headers)):
                file_headers[i]=file_headers[i].upper()

            for column in self.__columns:
                if column not in file_headers:
                    return False
                
            return True
    
    def __insert(self):
        with open(self.__abs_table_path, "r", newline="") as file:
            csv_reader=csv.reader(file)
            file_headers=next(csv_reader, None)

        column_value_dict={}

        for i in range(0, len(self.__columns)):
            column=self.__columns[i]
            value=self.__values[i]

            column_value_dict[column]=value

        with open(self.__abs_table_path, "a", newline="") as file:
            csv_writer=csv.DictWriter(file, fieldnames=file_headers)
            csv_writer.writerow(column_value_dict)

