import csv
from typing import List

from table_handler.TableHandlerInterface import TableHandlerInterface

class TableHandlerUpdate(TableHandlerInterface):
    def __init__(self, cmd_list: List[str]) -> None:
        self.__update_columns=cmd_list[5]
        self.__update_values=cmd_list[6]

        super().__init__(cmd_list)
    
    def _execute(self) -> None:
        if not self._columns:
            self.__update_all_registers()
        
        else:
            self.__update_register()
    
    def __update_all_registers(self) -> None:   
        with open(self._abs_table_path, "r", newline="") as file:
            csv_reader=csv.DictReader(file)
            headers=csv_reader.fieldnames

            save_registers=[]

            for register in csv_reader:
                for index, update_column in enumerate(self.__update_columns):
                    components=[]
                    
                    if "*" in self.__update_values[index]:
                        components=self.__update_values[index].split("*")
                        
                        if components[1].isdecimal():
                            value=components[1]
                        else:
                            value=components[0]

                        register[update_column]=float(register[update_column])*float(value)
                    
                    elif "/" in self.__update_values[index]:
                        components=self.__update_values[index].split("/")
                        
                        if components[1].isdecimal():
                            value=components[1]
                            register[update_column]=float(register[update_column])/float(value)
                        else:
                            value=components[0]
                            register[update_column]=float(value)/float(register[update_column])

                    elif "+" in self.__update_values[index]:
                        components=self.__update_values[index].split("+")
                        
                        if components[1].isdecimal():
                            value=components[1]
                        else:
                            value=components[0]
                        
                        register[update_column]=float(register[update_column])+float(value)

                    elif "-" in self.__update_values[index]:
                        components=self.__update_values[index].split("-")
                        
                        if components[1].isdecimal():
                            value=components[1]
                            register[update_column]=float(register[update_column])-float(value)
                        else:
                            value=components[0]
                            register[update_column]=float(value)-float(register[update_column])
                    
                    if len(components)==0:
                        register[update_column]=self.__update_values[index]
                
                save_registers.append(register)
            
        with open(self._abs_table_path, "w") as file:
            csv_writer=csv.DictWriter(file, fieldnames=headers)
            csv_writer.writeheader()
            csv_writer.writerows(save_registers)

    def __update_register(self) -> None:
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
                        if self._logical_operators[i-1]=="ou":
                            final_condition=final_condition or condition 
                        elif self._logical_operators[i-1]=="e":
                            final_condition=final_condition and condition 
                        else:
                            raise Exception("Erro de operador lógico!")
                    else:
                        final_condition=condition

                if final_condition==True:
                    for index, update_column in enumerate(self.__update_columns):

                        components=[]
                    
                        if "*" in self.__update_values[index]:
                            components=self.__update_values[index].split("*")
                            
                            if components[1].isdecimal():
                                value=components[1]
                            else:
                                value=components[0]

                            register[update_column]=float(register[update_column])*float(value)
                        
                        elif "/" in self.__update_values[index]:
                            components=self.__update_values[index].split("/")
                            
                            if components[1].isdecimal():
                                value=components[1]
                                register[update_column]=float(register[update_column])/float(value)
                            else:
                                value=components[0]
                                register[update_column]=float(value)/float(register[update_column])

                        elif "+" in self.__update_values[index]:
                            components=self.__update_values[index].split("+")
                            
                            if components[1].isdecimal():
                                value=components[1]
                            else:
                                value=components[0]
                            
                            register[update_column]=float(register[update_column])+float(value)

                        elif "-" in self.__update_values[index]:
                            components=self.__update_values[index].split("-")
                            
                            if components[1].isdecimal():
                                value=components[1]
                                register[update_column]=float(register[update_column])-float(value)
                            else:
                                value=components[0]
                                register[update_column]=float(value)-float(register[update_column])
                        
                        if len(components)==0:
                            register[update_column]=self.__update_values[index]
                    
                    save_registers.append(register)
                
                else:
                    save_registers.append(register)
                    
                final_condition=None
            
        with open(self._abs_table_path, "w") as file:
            csv_writer=csv.DictWriter(file, fieldnames=headers)
            csv_writer.writeheader()
            csv_writer.writerows(save_registers)
