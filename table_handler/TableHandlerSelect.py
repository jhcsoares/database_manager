import os
import csv

from table_handler.TableHandlerInterface import TableHandlerInterface

from typing import List

class TableHandlerSelect(TableHandlerInterface):
    def __init__(self, cmd_list: List[str]) -> None:
        self.__abs_table2_path=None
        self.__fields=cmd_list[5]
        self.__using_key=cmd_list[6]
        self.__order_by_columns=cmd_list[7]

        super().__init__(cmd_list)

    def _tables_exist(self) -> bool:
        if self._tables[1] is None:
            table_path=os.path.join("../database_manager/data/tables", self._tables[0].lower()+".csv")
            absolute_path1=os.path.abspath(table_path)
            self._abs_table_path=absolute_path1

            return os.path.isfile(absolute_path1)

        else:
            table_path=os.path.join("../database_manager/data/tables", self._tables[0].lower()+".csv")
            absolute_path1=os.path.abspath(table_path)
            self._abs_table_path=absolute_path1

            table_path=os.path.join("../database_manager/data/tables", self._tables[1].lower()+".csv")
            absolute_path2=os.path.abspath(table_path)
            self.__abs_table2_path=absolute_path2
            return os.path.isfile(absolute_path1) and os.path.isfile(absolute_path2)
        
    def __fields_exist(self) -> bool:
        if self._tables[1] is None:
            return self.__select_registers_fields_exist()
        
        else:
            return self.__inner_join_fields_exist()
    
    def __select_registers_fields_exist(self) -> bool:
        if self.__fields[0]=="*":
            return True
        
        with open(self._abs_table_path, "r", newline="") as file:
            csv_reader=csv.reader(file)
            file_headers=next(csv_reader, None)
            
            for i in range(0, len(file_headers)):
                file_headers[i]=file_headers[i].upper()

            for field in self.__fields:
                if field not in file_headers:
                    return False
                
            return True
    
    def __inner_join_fields_exist(self) -> bool:
        with open(self._abs_table_path, "r", newline="") as file:
            csv_reader=csv.reader(file)
            file_headers1=next(csv_reader, None)
            
            for i in range(0, len(file_headers1)):
                file_headers1[i]=file_headers1[i].upper()

        with open(self.__abs_table2_path, "r", newline="") as file:
            csv_reader=csv.reader(file)
            file_headers2=next(csv_reader, None)
            
            for i in range(0, len(file_headers2)):
                file_headers2[i]=file_headers2[i].upper()
        
        file_headers=file_headers1+file_headers2

        for field in self.__fields:
            if field not in file_headers:
                return False
            
        return True
        
    def _validate(self) -> None:
        if not self._tables_exist() and self._tables[1] is None:
            raise Exception(f"Tabela {self._tables[0]} não existente!")
        
        elif not self._tables_exist() and self._tables[1] is not None:
            raise Exception(f"Tabela {self._tables[0]} ou {self._tables[1]} não existente!")
        
        if not self.__fields_exist():
            raise Exception("Campos incorretos!")

    def _execute(self) -> None:
        if self._tables[1] is None:
            self.__select_registers()
        
        else:
            self.__inner_join()

    def __select_registers(self):
        with open(self._abs_table_path, "r", newline="") as file:
            csv_reader=csv.DictReader(file)
            
            final_condition=True
            registers=[]

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
                    if self.__fields[0]=="*":
                        registers.append(register)
                    
                    else:
                        column_value_dict={}
                        for field in self.__fields:
                            column_value_dict[field]=register[field]
                        registers.append(column_value_dict)

                final_condition=True
        print(registers)
                    
    def __inner_join(self):
        pass
