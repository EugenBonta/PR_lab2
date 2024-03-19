import sys
import threading
import socket

host = ('192.168.43.120')
port = 8500
user_addresses = {}


def hello_world(name):
    server.sendto(f'new:u:{name}'.encode(), ('<broadcast>', port))


def receive_messages():
    while True:
        try:
            data, address = server.recvfrom(1024)
            message = data.decode()
            state = message.split(':')[0]
            b_or_u = message.split(':')[1]
            name = message.split(':')[2]
            if address[0] == host:
                continue
            if state == 'new':
                add_new_user(name, address)
                continue

            if state == 'exit':
                exit_user(name)
                continue

            print(message)
        except:
            pass


def add_new_user(name, address):
    if user_addresses.get(name):
        return
    user_addresses[name] = address
    server.sendto(f'new:u:{username}'.encode(), address)
    print(f'New user {name}')


def exit_user(name):
    user_addresses.pop(name)
    print(f"User {name} has left")
    sys.exit(0)


def send_message():
    while True:
        message = input("")

        if message.startswith('b:'):
            server.sendto(f'From broadcast:b:{username}:{message.split(":")[1]}'.encode(), ('<broadcast>', port))
        elif message.startswith('u:'):
            parts = message.split(':', 3)
            target_username, message_content = parts[1], parts[2]
            if target_username in user_addresses:
                target_address = user_addresses[target_username]
                server.sendto(f"From user:u:{username}:{message_content}".encode(), target_address)
            else:
                print(f"Utilizatorul '{target_username}' nu exista sau nu este conectat.")
        elif message.startswith('exit'):
            server.sendto(f'exit:b:{username}'.encode(), ('<broadcast>', port))
        else:
            print(
                "Invalid command. Please start your message with 'b:' for broadcast or 'u:' for user-specific message.")


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

username = input("Introduceți numele dvs.: ")
print(f"Bun venit, {username}! Pentru a trimite un mesaj de broadcast, scrieți 'b:mesaj'.")
print(f"Pentru a trimite un mesaj unui utilizator specific, scrieti 'u:utilizator:mesaj'.")

hello_world(username)

send_thread = threading.Thread(target=send_message)
send_thread.daemon = True
send_thread.start()

receive_messages()
