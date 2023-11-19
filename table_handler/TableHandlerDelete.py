import csv
import os

from typing import List

from table_handler.TableHandlerInterface import TableHandlerInterface

class TableHandlerDelete(TableHandlerInterface):
    def __init__(self, cmd_list: List[str]):
        super().__init__(cmd_list)
    
    def _execute(self) -> None:
        if not self._columns:
            self.__delete_all_registers()

        else:
            self.__delete_register()

    def __delete_all_registers(self) -> None:
        with open(self._abs_table_path, "r", newline="") as file:
            csv_reader=csv.reader(file)
            file_headers=next(csv_reader, None)

        os.remove(self._abs_table_path)

        with open(self._abs_table_path, "w") as file:
            csv_writer=csv.DictWriter(file, fieldnames=file_headers)
            csv_writer.writeheader()

    def __delete_register(self) -> None:
        with open(self._abs_table_path, "r", newline="") as file:
            csv_reader=csv.DictReader(file)
            headers=csv_reader.fieldnames

            final_condition=None
            save_registers=self._get_registers()

            for register in csv_reader:
                for i in range(0, len(self._columns)):
                    column=self._columns[i]
                    value=self._values[i]
                    math_operator=self._math_operators[i]
                
                    if math_operator=="=":
                        condition=register[column]==value
                    elif math_operator==">":
                        condition=register[column]>value
                    elif math_operator==">=":
                        condition=register[column]>=value
                    elif math_operator=="<":
                        condition=register[column]<value
                    elif math_operator=="<=":
                        condition=register[column]<=value
                    elif math_operator=="!=":
                        condition=register[column]!=value
                    else:
                        raise Exception("Erro de operador aritmético!")

                    if i!=0 and len(self._logical_operators)>0:
                        if self._logical_operators[i-1]=="OU":
                            final_condition=final_condition or condition 
                        elif self._logical_operators[i-1]=="E":
                            final_condition=final_condition and condition 
                        else:
                            raise Exception("Erro de operador lógico!")
                    else:
                        final_condition=condition
                
                if final_condition==True:
                    save_registers.remove(register)
                
                final_condition=None

        with open(self._abs_table_path, "w") as file:
            csv_writer=csv.DictWriter(file, fieldnames=headers)
            csv_writer.writeheader()
            csv_writer.writerows(save_registers)

