from db_handler.DBHandlerInterface import DBHandlerInterface
from typing import List

import mysql.connector
import csv
import os

class DBHandler(DBHandlerInterface):
    def __init__(self, cmd_list: List[str]) -> None:
        super().__init__(cmd_list)

    def _validate(self) -> None:
        if not self._connection:
            try:
                self._connection=mysql.connector.connect(**self._db_setup)
            except:
                raise Exception(f"Banco de dados não existente!")

    def _execute(self, cmd_list: List[str]) -> None:
        self._table=cmd_list[0]
        self._data_base=cmd_list[1]

        if self._table:
            self._table=cmd_list[0]

            cursor=self._connection.cursor()
            query=f"select * from {self._table}"
            cursor.execute(query)
            result=cursor.fetchall()

            columns = []
            for column_name in cursor.description:
                columns.append(column_name[0])
            
            current_file_path=os.path.abspath(__file__)
            table_path=os.path.abspath(os.path.join(current_file_path, "../../data/tables/"+self._table+".csv"))
            
            with open(table_path, "w") as file:
                writer=csv.writer(file)

                writer.writerow(columns)
                writer.writerows(result)
                    
        if self._data_base:
            self._data_base=cmd_list[1]
