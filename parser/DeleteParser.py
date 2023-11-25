from typing import List
from parser.ParserInterface import ParserInterface

class DeleteParser(ParserInterface):
    def __init__(self, cmd_list: str):
        super().__init__(cmd_list)

    def _parser(self) -> None:
        if len(self._cmd_list)<2:
            raise Exception("Comando de deletar incorreto! (Poucas palavras no comando)")
        
        if self._cmd_list[1]!="de":
            raise Exception("Comando de deletar incorreto! (Palavra-chave 'de' incorreta)")
        
        if len(self._cmd_list)>3:
            if self._cmd_list[3]!="onde":
                raise Exception("Comando de deletar incorreto! (Faltando palavra-chave 'onde')")

    def _get_tables(self) -> List[str]:
        return [self._cmd_list[2]]
    
    def _get_columns(self) -> List[str]:
        columns=[]        

        for columns_index in range(4, len(self._cmd_list), 4):
            column=self._cmd_list[columns_index]

            columns.append(column)
        
        return columns
    
    def _get_values(self) -> List[str]:
        values=[]        

        for values_index in range(6, len(self._cmd_list), 4):
            value=self._cmd_list[values_index]

            values.append(value)
        
        return values
    
    def _get_math_operators(self) -> List[str]:
        math_operators=[]        

        for math_operators_index in range(5, len(self._cmd_list), 4):
            math_operator=self._cmd_list[math_operators_index]

            math_operators.append(math_operator)
        
        return math_operators
    
    def _get_logical_operators(self) -> List[str]:
        logical_operators=[]        

        for logical_operators_index in range(7, len(self._cmd_list), 4):
            logical_operator=self._cmd_list[logical_operators_index]

            logical_operators.append(logical_operator)
        
        return logical_operators
    