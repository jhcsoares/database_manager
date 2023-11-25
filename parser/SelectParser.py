from abc import ABC, abstractmethod
from typing import List

class SelectParser(ABC):
    def __init__(self, cmd_list: str) -> None:
        self._cmd_list=cmd_list

    def _execute(self) -> List:
        self._parser()

        tables=self._get_tables()
        columns=self._get_columns()
        values=self._get_values()
        math_operators=self._get_math_operators()
        logical_operators=self._get_logical_operators()
        fields=self.__get_fields()
        using_key=self.__get_using_key()
        order_by_columns=self.__get_order_by_columns()
        
        return [tables, columns, values, math_operators, logical_operators, fields, using_key, order_by_columns]
    
    def _parser(self) -> None:
        if len(self._cmd_list)<4:
            raise Exception("Comando de selecionar incorreto! (Poucas palavras no comando)")
        
        if not "de" in self._cmd_list:
            raise Exception("Comando de selecionar incorreto! (Faltando palavra-chave 'de')")
        
        if ("junte" in self._cmd_list and not "com" in self._cmd_list) or ("com" in self._cmd_list and not "junte" in self._cmd_list):
            raise Exception("Comando de selecionar incorreto! (Palavra-chave 'junte com' incorreta)")
        
    def _get_tables(self) -> List[str]:
        table1_index=self._cmd_list.index("de")+1
        table1=self._cmd_list[table1_index]

        if "com" in self._cmd_list:
            table2_index=self._cmd_list.index("com")+1
            table2=self._cmd_list[table2_index]
        else:
            table2=None

        return [table1, table2]
    
    def _get_columns(self) -> List[str]:
        if "onde" in self._cmd_list:
            columns=[]        

            start_value=self._cmd_list.index("onde")+1

            for column_index in range(start_value, len(self._cmd_list), 4):
                column=self._cmd_list[column_index]

                if column!="por":
                    columns.append(column)
            
            return columns

        else:
            return []

    def _get_values(self) -> List[str]:
        if "onde" in self._cmd_list:
            values=[]        

            start_value=self._cmd_list.index("onde")+3

            stop=False

            for value_index in range(start_value, len(self._cmd_list), 4):
                if not stop:
                    if ("ordene" in self._cmd_list) and (self._cmd_list[value_index+1]=="ordene"):                
                        value=self._cmd_list[value_index]
                        values.append(value)
                        stop=True
                    
                    else:
                        value=self._cmd_list[value_index]
                        values.append(value)

            return values

        else:
            return []

    def _get_math_operators(self) -> List[str]:
        if "onde" in self._cmd_list:
            math_operators=[]        

            start_math_operator=self._cmd_list.index("onde")+2

            stop=False

            for math_operator_index in range(start_math_operator, len(self._cmd_list), 4):
                if not stop:
                    if ("ordene" in self._cmd_list) and (self._cmd_list[math_operator_index+2]=="ordene"):                
                        math_operator=self._cmd_list[math_operator_index]
                        math_operators.append(math_operator)
                        stop=True
                    
                    else:
                        math_operator=self._cmd_list[math_operator_index]
                        math_operators.append(math_operator)

            return math_operators

        else:
            return []

    def _get_logical_operators(self) -> List[str]:
        if "onde" in self._cmd_list:
            logical_operators=[]        

            start_logical_operator=self._cmd_list.index("onde")+4

            if (start_logical_operator<len(self._cmd_list)) and (self._cmd_list[start_logical_operator]!="ordene"):

                stop=False

                for logical_operator_index in range(start_logical_operator, len(self._cmd_list), 4):
                    if not stop:
                        if ("ordene" in self._cmd_list) and (self._cmd_list[logical_operator_index+4]=="ordene"):                
                            logical_operator=self._cmd_list[logical_operator_index]
                            logical_operators.append(logical_operator)
                            stop=True
                        
                        else:
                            logical_operator=self._cmd_list[logical_operator_index]
                            logical_operators.append(logical_operator)
            
                return logical_operators

            else:
                return []

        else:
            return []

    def __get_fields(self):
        fields=[]
        field_index=1

        stop=False

        while not stop:
            field=self._cmd_list[field_index]

            if "," in field:
                fields.append(field[0:len(field)-1])
            else:
                fields.append(field)

            field_index+=1

            if self._cmd_list[field_index]=="de":
                stop=True

        return fields
    
    def __get_using_key(self) -> str:
        if "junte" in self._cmd_list:
            if "usando" in self._cmd_list:
                key_index=self._cmd_list.index("usando")+1

                return [self._cmd_list[key_index]]
            
            else:
                key1_index=self._cmd_list.index("sob")+1
                key2_index=self._cmd_list.index("sob")+3
                return [self._cmd_list[key1_index], self._cmd_list[key2_index]]

        return None
    
    def __get_order_by_columns(self) -> List[str]:
        if "ordene" in self._cmd_list:
            order_by_columns=[]

            start_index=self._cmd_list.index("por")+1

            for index in range(start_index, len(self._cmd_list)):
                column=self._cmd_list[index]

                if "," in column:
                    order_by_columns.append(column[0:len(column)-1])
                else:
                    order_by_columns.append(column)
            
            return order_by_columns
        
        return []
    