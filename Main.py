from typing import List

from parser.DeleteParser import DeleteParser
from parser.InsertParser import InsertParser
from parser.UpdateParser import UpdateParser

from table_handler.TableHandlerInsert import TableHandlerInsert
from table_handler.TableHandlerUpdate import TableHandlerUpdate
from table_handler.TableHandlerDelete import TableHandlerDelete

class Main:
    def __init__(self, command: str) -> None:
        self.__command=command.upper()
        self.__cmd_list=self.__parse()
        self.__execute()
    
    def __execute(self) -> None:
        if self.__cmd_list[0]=="INSIRA":
            insert_parser=InsertParser(self.__cmd_list)
            parsed_cmd_list=insert_parser._execute()

            TableHandlerInsert(parsed_cmd_list)
        
        elif self.__cmd_list[0]=="ATUALIZE":
            update_parser=UpdateParser(self.__cmd_list)
            parsed_cmd_list=update_parser._execute()

            TableHandlerUpdate(parsed_cmd_list)
        
        elif self.__cmd_list[0]=="APAGUE":
            delete_parser=DeleteParser(self.__cmd_list)
            parsed_cmd_list=delete_parser._execute()

            TableHandlerDelete(parsed_cmd_list)

        else:
            raise Exception("Comando principal não encontrado!")
    
    def __parse(self) -> List[str]:
        return self.__command.split(" ") 
