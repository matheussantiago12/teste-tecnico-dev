import sys
import json
import os.path

def read_json():
    with open("config.json") as file:
        try:
            data = json.load(file)

            if (data == {}):
                print("O arquivo não contém informações.")
                sys.exit(0)
            
            return data
        except json.JSONDecodeError:
            print("Erro ao ler arquivo.")
    
def write_json(data: dict):
    with open("config.json", "w") as outfile:
        json.dump(data, outfile)

def main():
    if (not os.path.isfile("./config.json")):
        write_json({}) # Cria arquivo caso não exista
    
    print("1 - Read configuration")
    print("2 - Write configuration")
    option = int(input())

    if (option != 1 and option != 2):
        print("Opção inválida!")
        sys.exit(0)

    if (option == 1):
        data = read_json()
        print(data)
    else:
        server_name = input("1 - Informe o nome do servidor: ")
        server_ip = input("2 - Informe o IP do servidor: ")
        server_password = input("3 - Informe a senha do servidor: ")

        data = {
            "server_name": server_name,
            "server_ip": server_ip,
            "server_password": server_password
        }

        write_json(data)
        result = read_json()
        print(result)

main()