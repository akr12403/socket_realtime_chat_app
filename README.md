# socket_realtime_chat_app

Realtime Chat Application was developed through the practice of TCP Socket Programming. By employing an echo client-server architecture, Realtime Chat Application sures low-latency in message delivery and compatibility in using the application. Below is the documentation of Realtime Chat Application:


Key Variables of Server Side Chat Application
- host_ip: Variable that defines the IP address to be passed in
- port_addr: Variable that defines the port number to be passed in
- total_listeners: Variable that defines the total listeners on the network
- server: Variable that defines a server socket object
- active_clients: Variable that is a list of currently connected users

Functionality/Approach: I will be explaining the purpose of each method, and in the following section, I will show the execution of the code. I have defined five global variables above with their purposes being stated

Method 1 - def listen_for_messages(client, username): This method listens for incoming messages from a client and must inform everyone that a new message has been sent every time a user sent a message. The message is received and appended to a final message that consists of the client username along with the message content (with a special character ‘~’ that will eventually be used to identify the username and message content when the client receives the message back in client receive_message. The final message is passed into send_message_to_all() which will be broadcasted to all connected clients and sent back to the client (receiving function in client)

Code description:
def listen_for_messages(client, username): #listen for upcoming messages from a client
    while True: #server must inform everyone that a new message has been sent everytime a user sent a message
        message = client.recv(2048).decode('utf-8')
        if message != '': #message is appended to a final message with username seperated by ~ (identifying username and content in client receive_message)
            final_msg = username + '~' + message
            send_messages_to_all(final_msg) #final message is passed into send_messages_to_all which sends the message back to client (receiving function in client)
        else:
            print(f"Client {username} has sent an empty message")

Method 2 - def send_message_to_client(client, message): This method sends an encoded message back to the client taking in the client and the message to be sent as parameters. The message, originally in readable string format, is encoded in bytes and sent to the client (who has a receiving function).
	
Code description:
def send_message_to_client(client, message): #send message to a single client
    	client.sendall(message.encode())

Method 3 - def send_messages_to_all(message): This method serves to broadcast all the messages to currently connected clients. Therefore, any new message that is sent using this function will essentially be broadcasted to all clients connected. It loops through each tuple in the active_client list (explained more in detail in client_handler). For every tuple in the list containing tuple (every user in active_client), we will implement send_message_to_client() and pass in a client along with the message. Essentially “user” is a tuple that stores (username, client) (this part is explained more in detail in client_handler), and by accessing user[1] we can access the client.


Code description:
def send_messages_to_all(message): #specific user has sent specific message is broadcasted to all connected clients
#function sends any new message to all clients currently connected to server
    for user in active_clients: #iterating through every user in active_client
        send_message_to_client(user[1], message) #client list is storing tuple (username, client)
        #for every tuple in client list, we send_message_to_client and pass in user[1] = client

Method 4 - def client_handler(client): This method functionality deals with clients. It listens for messages that the client would send to the server, which will contain the username. Client connect_to_server() is behind this, which will be discussed in the client section. The username is received by the server, which is decoded into a readable string format, and while this username exists and is not empty, we can update our list of tracking current clients by appending client and username as tuple attributes to active_clients. The server also deals with clients by providing the prompt message of the server welcoming the client into the chat application (this message of welcoming the client is the parameter passed into send_messages_to_all() which is broadcasted to all currently connected clients. Not to mention, I implemented a thread to concurrently run listen_for_messages (which will continue to keep listening for messages sent from the client side.


Code Description:
def client_handler(client): # Function to handle client
    while True: #listen for message that the client will send which will contain the username and get username
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

def main(): This is the main method, the executable.


Code description:
def main(): #main/executable
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
