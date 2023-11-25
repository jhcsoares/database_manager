from typing import List
from parser.ParserInterface import ParserInterface

class UpdateParser(ParserInterface):
    def __init__(self, cmd_list: str):
        super().__init__(cmd_list)

    def _execute(self):
        self._parser()

        tables=self._get_tables()
        columns=self._get_columns()
        values=self._get_values()
        math_operators=self._get_math_operators()
        logical_operators=self._get_logical_operators()
        update_columns=self.__get_update_columns()
        update_values=self.__get_update_values()

        return [tables, columns, values, math_operators, logical_operators, update_columns, update_values]

    def _parser(self) -> None:
        if len(self._cmd_list)<5:
            raise Exception("Comando de atualizar incorreto! (Poucas palavras no comando)")
       
        if self._cmd_list[2]!="configure":
            raise Exception("Comando de atualizar incorreto! (Palavra-chave 'configure' incorreta)")
        
        if "onde" not in self._cmd_list:
            raise Exception("Comando de atualizar incorreto! (Faltando palavra-chave 'onde')")

    def _get_tables(self) -> List[str]:
        return [self._cmd_list[1]]

    def _get_columns(self) -> List[str]:
        columns=[]        

        start_value=self._cmd_list.index("onde")+1

        for column_index in range(start_value, len(self._cmd_list), 4):
            column=self._cmd_list[column_index]

            columns.append(column)
        
        return columns

    def _get_values(self) -> List[str]:
        values=[]        

        start_value=self._cmd_list.index("onde")+3

        for value_index in range(start_value, len(self._cmd_list), 4):
            value=self._cmd_list[value_index]

            if value.endswith(","):
                values.append(value[0:len(value)-1])

            else:
                values.append(value)
        
        return values
    
    def _get_math_operators(self) -> List[str]:
        math_operators=[]        

        start_math_operator=self._cmd_list.index("onde")+2

        for math_operator_index in range(start_math_operator, len(self._cmd_list), 4):
            math_operator=self._cmd_list[math_operator_index]

            math_operators.append(math_operator)
        
        return math_operators

    def _get_logical_operators(self) -> List[str]:
        logical_operators=[]        

        start_logical_operator=self._cmd_list.index("onde")+4

        for logical_operators_index in range(start_logical_operator, len(self._cmd_list), 4):
            logical_operator=self._cmd_list[logical_operators_index]

            logical_operators.append(logical_operator)
        
        return logical_operators
    
    def __get_update_columns(self) -> List[str]:
        update_columns=[]

        update_column_index=self._cmd_list.index("configure")+1

        stop=False

        while not stop:
            update_column=self._cmd_list[update_column_index]

            update_columns.append(update_column)

            update_column_index+=3

            if self._cmd_list[update_column_index]=="onde":
                stop=True

        return update_columns
    
    def __get_update_values(self) -> List[str]:
        update_values=[]

        update_value_index=self._cmd_list.index("configure")+3

        stop=False

        while not stop:
            update_value=self._cmd_list[update_value_index]

            if "," in update_value:
                update_values.append(update_value[0:len(update_value)-1])
                update_value_index+=3

            else:
                update_values.append(update_value)
                stop=True

        return update_values
    