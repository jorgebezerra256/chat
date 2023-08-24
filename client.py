import threading
import socket


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('localhost', 9000))
    except:
        return print('\nErro ao conectar!')

    print("\nConnectado")
    username = input('\nUsuário: ')

    thread1 = threading.Thread(target=receber_mensagem, args=[client])
    thread2 = threading.Thread(target=enviar_mensagem, args=(client, username))

    thread1.start()
    thread2.start()


def receber_mensagem(client):
    while True:
        try:
            mensagem = client.recv(2048).decode('utf-8')
            print(mensagem+'\n')
        except:
            print('\nPerca de conexão!')
            print('ENTER para continuar!')
            client.close()
            break


def enviar_mensagem(client, username):
    while True:
        try:
            mensagem = input('\n')
            dados = f'{username}:: {mensagem}'.encode('utf-8')
            client.send(dados)
        except:
            return


main()

