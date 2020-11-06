import socket
import sys
from gamestate import GameState

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 5000)
print('Conectando ao servidor {} na porta {}'.format(server_address[0], server_address[1]))
sock.connect(server_address)
print("Você é o X")

# Cria um tabuleiro de jogo vazio
game = GameState()

try:

    while True:
        if game.hasWinner():
                sock.close()

        # Recebe a jogada do servidor
        data = sock.recv(1024)
        game.restore(data.decode('utf-8'))

        print('O servidor jogou:')
        game.print()

        print('Faça a sua jogada:')
        print('------------------')

        nok = True
        while nok:
            row = int(input('Digite a linha:'))
            col = int(input('Digite a coluna:'))

            nok = False
            try:
                game.move(row, col, 'x')
            except:
                nok = True
                print('Linha ou coluna inválida. Tente novamente.')

        # Envia o tabuleiro para o servidor
        sock.sendall(game.save().encode('utf-8'))

        if game.hasWinner():
            sock.close()

finally:
    print('Encerrando o cliente')
    sock.close()