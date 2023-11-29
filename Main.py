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
        self.__execute()
    
    def __execute(self) -> None:
        while True:
            try:
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

                elif self.__cmd_list[0]=="sair":
                    break

                else:
                    raise Exception("Comando principal não encontrado!")
            
            except Exception as error:
                print(error.args[0])
    
    def __parse(self) -> List[str]:
        command_list=self.__command.split(" ") 
        
        if "insira" in command_list:
            index=command_list.index("valores")+1
            
            values=[]
            pick_last_value=False
            for i in range(index, len(command_list)):
                if not "," in command_list[i]:
                    if pick_last_value:
                        append_value=command_list[i-1]+" "+command_list[i]
                        values.append(append_value)
                    elif not ")" in command_list[i]:
                        pick_last_value=True
                    else:
                        values.append(command_list[i])
                elif pick_last_value:
                    append_value=command_list[i-1]+" "+command_list[i]
                    values.append(append_value)
                    pick_last_value=False
                else:
                    values.append(command_list[i])
                    pick_last_value=False
            
            index=command_list.index("valores")
            command_list=command_list[0:index+1]+values
            return command_list

        elif "atualize" in command_list:

            index=command_list.index("configure")+3
            
            stop=False

            while not stop:
                if index+1<len(command_list):
                    if command_list[index+1]!="onde":
                        if "," not in command_list[index]:
                            value=command_list[index]+" "+command_list[index+1]
                            command_list[index]=value
                            del command_list[index+1]
                        index+=3

                        if index>=len(command_list) or command_list.index("onde")<index:
                            stop=True   

            if "onde" in command_list:
                index=command_list.index("onde")+3
                
                stop=False

                while not stop:
                    if index+1<len(command_list):
                        if command_list[index+1]!="e" and command_list[index+1]!="ou":
                            value=command_list[index]+" "+command_list[index+1]
                            command_list[index]=value
                            del command_list[index+1]
                               
                    index+=4
                    if index>=len(command_list):
                        stop=True 

            return command_list
        
        elif "apague" in command_list:   
            if "onde" in command_list:
                index=command_list.index("onde")+3
                
                stop=False

                while not stop:
                    if index+1<len(command_list):
                        if command_list[index+1]!="e" and command_list[index+1]!="ou":
                            value=command_list[index]+" "+command_list[index+1]
                            command_list[index]=value
                            del command_list[index+1]
                               
                    index+=4
                    if index>=len(command_list):
                        stop=True 

            return command_list
        
        elif "selecione" in command_list:   
            if "onde" in command_list:
                index=command_list.index("onde")+3
                
                stop=False

                while not stop:
                    if index+1<len(command_list):
                        if command_list[index+1]!="e" and command_list[index+1]!="ou":
                            value=command_list[index]+" "+command_list[index+1]
                            command_list[index]=value
                            del command_list[index+1]
                               
                    index+=4
                    if index>=len(command_list):
                        stop=True 
                    
                    if "ordene" in command_list:
                        if index>=command_list.index("ordene"):
                            stop=True 

            return command_list
        
        return command_list

if __name__=="__main__":
    main=Main()
    