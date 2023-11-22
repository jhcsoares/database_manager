import csv
from typing import List

from table_handler.TableHandlerInterface import TableHandlerInterface

class TableHandlerInsert(TableHandlerInterface):
    def __init__(self, cmd_list: List[str]) -> None:
        super().__init__(cmd_list)
    
    def _execute(self) -> None:
        with open(self._abs_table_path, "r", newline="") as file:
            csv_reader=csv.reader(file)
            file_headers=next(csv_reader, None)

        column_value_dict={}

        for i in range(0, len(self._columns)):
            column=self._columns[i]
            value=self._values[i]

            column_value_dict[column]=value

        with open(self._abs_table_path, "a", newline="") as file:
            csv_writer=csv.DictWriter(file, fieldnames=file_headers)
            csv_writer.writerow(column_value_dict)
