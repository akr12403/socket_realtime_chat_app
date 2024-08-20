import socket
import threading

host_ip = '127.0.0.1'
port_addr = 9999 # You can use any port between 0 to 65535
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating a server socket object, AF_INET for ipv4 addresses, SOCK_STREAM for tcp based socket communication
total_listeners = 5
active_clients = [] #list of currently connected users

def listen_for_messages(client, username): #listen for upcoming messages from a client
    while True: #server must inform everyone that a new message has been sent everytime a user sent a message
        message = client.recv(2048).decode('utf-8')
        if message != '': #message is appended to a final message with username seperated by ~ (identifying username and content in client receive_message)
            final_msg = username + '~' + message
            send_messages_to_all(final_msg) #final message is passed into send_messages_to_all which sends the message back to client (receiving function in client)
        else:
            print(f"Client {username} has sent an empty message")

def send_message_to_client(client, message): #send message to a single client
    client.sendall(message.encode())

def send_messages_to_all(message): #specific user has sent specific message is broadcasted to all connected clients
#function sends any new message to all clients currently connected to server
    for user in active_clients: #iterating through every user in active_client
        send_message_to_client(user[1], message) #client list is storing tuple (username, client)
        #for every tuple in clientlist, we send_message_to_client and pass in user[1] = client

def client_handler(client): # Function to handle client
    while True: #listen for message that the client will send which will contain the usernam and get username
        username = client.recv(2048).decode('utf-8') #client connect_to_server() sends the username after executing the client join
        if username != '': #appends the tuple containing the username along with the client socket to a list tracking currently connected users
            active_clients.append((username, client))
            prompt_message = "SERVER~" + "Welcoming " f"{username} to the chat!" 
            send_messages_to_all(prompt_message) #string message welcoming client is eventually encoded to bytes and is broadcasted to all connected clients
            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username, )).start() #concurrently runs listen_for_messages as a executable thread
    #continues to keep listening for messages that are sent from the client to server and sends broadcasted messages back to all clients

def main(): #main
    try: #creating a try catch block, provide the server with an address in the form of host IP and port
        server.bind((host_ip, port_addr)) #Socket is a server socket, will accept connections
        print(f"Server runs on {host_ip} {port_addr}")
    except:
        print(f"Cannot bind host {host_ip} and port {port_addr}")

    server.listen(total_listeners)  # Set server limit

    while True:  # This while loop will keep listening to client connections
        client, addr = server.accept()
        print(f"Client Connection Success: {addr[0]} {addr[1]} ")

        threading.Thread(target=client_handler, args=(client, )).start() 
        #concurrently runs client_handler that will continue to let the server deal with concurrent client connections

if __name__ == '__main__':
    main()