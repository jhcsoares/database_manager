from typing import List
from parser.ParserInterface import ParserInterface

class InsertParser(ParserInterface):
    def __init__(self, cmd_list: str) -> None:
        super().__init__(cmd_list)

    def _parser(self) -> None:
        if len(self._cmd_list)<5:
            raise Exception("Comando de inserir incorreto! (Poucas palavras no comando)")
       
        if self._cmd_list[1]!="EM":
            raise Exception("Comando de inserir incorreto! (Palavra-chave 'EM' incorreta)")
        
        if "VALORES" not in self._cmd_list:
            raise Exception("Comando de inserir incorreto! (Faltando palavra-chave 'VALORES')")

        column_index=3
        value_index=len(self._cmd_list)-1

        stop=False
        
        while not stop:
            if self._cmd_list[column_index]=="VALORES" or self._cmd_list[value_index]=="VALORES":
                stop=True

            if not stop:
                column_index+=1
                value_index-=1

        if column_index!=value_index or column_index==3 or value_index==len(self._cmd_list)-1:
            raise Exception("Comando de inserir incorreto! (Relação coluna-valor está incorreta)")

    def _get_tables(self) -> List[str]:
        return [self._cmd_list[2]]

    def _get_columns(self) -> List[str]:
        columns=[]        
        columns_index=3

        while self._cmd_list[columns_index]!="VALORES":
            column=self._cmd_list[columns_index]

            if not column.startswith("("):
                columns.append(column[0:len(column)-1])
            
            else:
                columns.append(column[1:len(column)-1])
            
            columns_index+=1
        
        return columns
    
    def _get_values(self) -> List[str]:
        values=[]        
        values_index=self._cmd_list.index("VALORES")+1

        for i in range(values_index, len(self._cmd_list)):
            value=self._cmd_list[i]

            if not value.startswith("("):
                values.append(value[0:len(value)-1])
            
            else:
                values.append(value[1:len(value)-1])
            
            values_index+=1
        
        return values
    
    def _get_math_operators(self) -> List[str]:
        return []
    
    def _get_logical_operators(self) -> List[str]:
        return []