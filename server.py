import threading
import socket


clientes = []
num_conect = 0

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(('localhost', 9000))
        server.listen(5)
    except:
        return print('\nServidor já está em execução!')

    while True:
        print('Aguardando conexões!')
        client, endereco = server.accept()
        print(f'Cliente connectado: {endereco}')
        global num_conect
        num_conect += 1
        clientes.append((client, num_conect))

        thread = threading.Thread(target=tratar_mensagem, args=[client])
        thread1 = threading.Thread(target=responder, args=[client])

        thread.start()
        thread1.start()


def delete_cliente(cliente):
    clientes.remove(cliente)


def tratar_mensagem(cliente):
    while True:
        try:
            mensagem = cliente.recv(2048)
            stringdata = mensagem.decode('utf-8')
            data = stringdata.split('::')

            if len(data) == 3:
                id = int(data[1])
                send_by_id(id, data[0] + ": " + data[2])
            else:
                broadcast(mensagem, cliente)
        except:
            delete_cliente(cliente)
            break


def broadcast(mensagem, cliente):
    for clientItem in clientes:
        if cliente != clientItem[0]:
            try:
                clientItem[0].send(mensagem)
            except:
                delete_cliente(clientItem)

def responder(cliente):
    m = ''
    for client in clientes:
        if client[0] != cliente:

            print(client[0].getpeername())
            y = client[0].getpeername()
            m += ' '.join(map(str,y))+"_:_" + str(client[1])+'\n'
        else:
            y = client[0].getpeername()
            m += ' '.join(map(str, y)) + "_:_" + str(client[1]) + '_MY\n'

    for clientItem in clientes:
        try:
            clientItem[0].send(m.encode('utf-8'))
        except:
            delete_cliente(clientItem)


def send_by_id(id, mensagem):
    for cliente in clientes:
        if cliente[1] == id:
            cliente[0].send(mensagem.encode('utf-8'))
            break


main()

