from typing import List

from parser.DeleteParser import DeleteParser
from parser.InsertParser import InsertParser
from parser.UpdateParser import UpdateParser
from parser.SelectParser import SelectParser
from db_parser.DBParser import DBParser

from table_handler.TableHandlerInsert import TableHandlerInsert
from table_handler.TableHandlerUpdate import TableHandlerUpdate
from table_handler.TableHandlerDelete import TableHandlerDelete
from table_handler.TableHandlerSelect import TableHandlerSelect
from db_handler.DBHandler import DBHandler

class Main:
    def __init__(self) -> None:
        self.__command=None
        self.__cmd_list=None
        self.__db_handler=None
        self.__created_tables=[] ############
        self.__execute()
    
    def __execute(self) -> None:
        while True:
            command=str(input("Digite seu comando: "))
            self.__command=command
            self.__cmd_list=self.__parse()

            if self.__cmd_list[0]=="insira":
                insert_parser=InsertParser(self.__cmd_list)
                parsed_cmd_list=insert_parser._execute()

                TableHandlerInsert(parsed_cmd_list)
            
            elif self.__cmd_list[0]=="atualize":
                update_parser=UpdateParser(self.__cmd_list)
                parsed_cmd_list=update_parser._execute()

                TableHandlerUpdate(parsed_cmd_list)
            
            elif self.__cmd_list[0]=="apague":
                delete_parser=DeleteParser(self.__cmd_list)
                parsed_cmd_list=delete_parser._execute()

                TableHandlerDelete(parsed_cmd_list)
            
            elif self.__cmd_list[0]=="selecione":
                select_parser=SelectParser(self.__cmd_list)
                parsed_cmd_list=select_parser._execute()

                TableHandlerSelect(parsed_cmd_list)

            elif self.__cmd_list[0]=="importe":
                import_parser=DBParser(self.__cmd_list)
                parsed_cmd_list=import_parser.execute()

                if (not self.__db_handler) or (self.__db_handler._data_base!=parsed_cmd_list[1] and parsed_cmd_list[1]):
                    self.__db_handler=DBHandler(parsed_cmd_list)
                    self.__db_handler._execute(parsed_cmd_list)
                else:
                    self.__db_handler._execute(parsed_cmd_list)

            else:
                raise Exception("Comando principal não encontrado!")
    
    def __parse(self) -> List[str]:
        return self.__command.split(" ") 
    
if __name__=="__main__":
    main=Main()
