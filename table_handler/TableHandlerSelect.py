import os
import csv
from prettytable import PrettyTable 

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
            current_file_path=os.path.abspath(__file__)
            table_path=os.path.abspath(os.path.join(current_file_path, "../../data/tables/"+self._tables[0]+".csv"))
            self._abs_table_path=table_path

            return os.path.isfile(table_path)

        else:
            current_file_path=os.path.abspath(__file__)
            table_path=os.path.abspath(os.path.join(current_file_path, "../../data/tables/"+self._tables[0]+".csv"))
            self._abs_table_path=table_path

            current_file_path=os.path.abspath(__file__)
            table_path=os.path.abspath(os.path.join(current_file_path, "../../data/tables/"+self._tables[1]+".csv"))
            self.__abs_table2_path=table_path
            
            return os.path.isfile(self._abs_table_path) and os.path.isfile(self.__abs_table2_path)
        
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
                file_headers[i]=file_headers[i]

            for field in self.__fields:
                if field not in file_headers:
                    return False
                
            return True
    
    def __inner_join_fields_exist(self) -> bool:
        if self.__fields[0]=="*":
            return True
        
        with open(self._abs_table_path, "r", newline="") as file:
            csv_reader=csv.reader(file)
            file_headers1=next(csv_reader, None)
            
            for i in range(0, len(file_headers1)):
                file_headers1[i]=file_headers1[i]

        with open(self.__abs_table2_path, "r", newline="") as file:
            csv_reader=csv.reader(file)
            file_headers2=next(csv_reader, None)
            
            for i in range(0, len(file_headers2)):
                file_headers2[i]=file_headers2[i]
        
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
            registers=self.__select_registers()
        else:
            registers=self.__inner_join()

        if self.__order_by_columns is None:
            self.__print_table(registers)
        else:
            registers=self.__sort(registers)
            self.__print_table(registers)

    def __select_registers(self) -> List:
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
                        if self._logical_operators[i-1]=="ou":
                            final_condition=final_condition or condition 
                        elif self._logical_operators[i-1]=="e":
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

        return registers
                    
    def __inner_join(self) -> List:
        with open(self._abs_table_path, "r", newline="") as file:
            csv_reader1=csv.DictReader(file)
            file_headers1=csv_reader1.fieldnames

            registers1=[]

            for register in csv_reader1:
                registers1.append(register)

        with open(self.__abs_table2_path, "r", newline="") as file:
            csv_reader2=csv.DictReader(file)
            file_headers2=csv_reader2.fieldnames

            registers2=[]

            for register in csv_reader2:
                registers2.append(register)

        for using_key in self.__using_key:
            if (using_key not in file_headers1) and (using_key not in file_headers2):
                raise Exception(f"Comando de selecionar incorreto! (Chave de comparação {using_key} não existente)")
        
        if len(self.__using_key)==1:
            using_key1=self.__using_key[0]
            using_key2=self.__using_key[0]
        else:
            if self.__using_key[0] in file_headers1:
                using_key1=self.__using_key[0]
                using_key2=self.__using_key[1]
            else:
                using_key1=self.__using_key[1]
                using_key2=self.__using_key[0]

        final_registers_aux=[]

        for register1 in registers1:
            for register2 in registers2:
                column_value_dict={}

                if register1[using_key1]==register2[using_key2]:
                    column_value_dict=register1

                    for key in register2:
                        if key not in self.__using_key:
                            column_value_dict[key]=register2[key]

                    final_registers_aux.append(column_value_dict)
                
                final_registers=[]

                if self.__fields[0]=="*":
                    final_registers=final_registers_aux
                else:
                    for index, register in enumerate(final_registers_aux):
                        column_value_dict={}
                        
                        for key in self.__fields:
                            column_value_dict[key]=final_registers_aux[index][key]
                        
                        final_registers.append(column_value_dict)
        
        final_condition=True
        registers=[]

        for register in final_registers:
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
                    if self._logical_operators[i-1]=="ou":
                        final_condition=final_condition or condition 
                    elif self._logical_operators[i-1]=="e":
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
        
        return registers

    def __sort(self, registers_list: List) -> List:
        sorted_registers_list=sorted(registers_list, key=lambda x: tuple(x[key] for key in self.__order_by_columns))
        return sorted_registers_list
    
    def __print_table(self, data: List):
        table=PrettyTable()

        table.field_names=list(data[0].keys())

        for row in data:
            table.add_row(list(row.values()))

        print(table)
