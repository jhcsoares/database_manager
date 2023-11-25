from typing import List

class DBParser:
    def __init__(self, cmd_list: str) -> None:
        self.__cmd_list=cmd_list

    def execute(self) -> List:
        self.__parser()

        table=self.__get_table()
        data_base=self.__get_data_base()

        return [table, data_base]
    
    def __parser(self) -> None:
        if self.__cmd_list[1]=="banco":
            if self.__cmd_list[2]!="DE":
                raise Exception("Erro no comando de importar! (Palavra-chave 'DE' incorreta)")
            if self.__cmd_list[3]!="dados":   
                raise Exception("Erro no comando de importar! (Palavra-chave 'dados' incorreta)")

        elif len(self.__cmd_list)>3:
            raise Exception("Erro no comando de importar! (Muitas palavras-chave na importação de tabela)")   
        
    def __get_table(self):
        if self.__cmd_list[1]!="banco":
            return self.__cmd_list[1]

        return []


    def __get_data_base(self):
        if self.__cmd_list[1]=="banco":
            return self.__cmd_list[4]
        
        return []
