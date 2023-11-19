import csv
from typing import List

from table_handler.TableHandlerInterface import TableHandlerInterface

class TableHandlerUpdate(TableHandlerInterface):
    def __init__(self, cmd_list: List[str]):
        self.__update_columns=cmd_list[5]
        self.__update_values=cmd_list[6]

        super().__init__(cmd_list)
    
    def _execute(self) -> None:
        with open(self._abs_table_path, "r", newline="") as file:
            csv_reader=csv.DictReader(file)
            headers=csv_reader.fieldnames

            final_condition=None
            save_registers=[]

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

                column_value_update_dict={}

                if final_condition==True:
                    for i in range(0, len(self.__update_columns)):
                        column=self.__update_columns[i]
                        value=self.__update_values[i]

                        column_value_update_dict[column]=value
                    
                    save_registers.append(column_value_update_dict)
                
                else:
                    save_registers.append(register)
                    
                final_condition=None
            
        with open(self._abs_table_path, "w") as file:
            csv_writer=csv.DictWriter(file, fieldnames=headers)
            csv_writer.writeheader()
            csv_writer.writerows(save_registers)
