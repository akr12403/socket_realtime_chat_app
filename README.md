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

Method 2 - def send_message_to_client(client, message): This method sends an encoded message back to the client taking in the client and the message to be sent as parameters. The message, originally in readable string format, is encoded in bytes and sent to the client (who has a receiving function).

Method 3 - def send_messages_to_all(message): This method serves to broadcast all the messages to currently connected clients. Therefore, any new message that is sent using this function will essentially be broadcasted to all clients connected. It loops through each tuple in the active_client list (explained more in detail in client_handler). For every tuple in the list containing tuple (every user in active_client), we will implement send_message_to_client() and pass in a client along with the message. Essentially “user” is a tuple that stores (username, client) (this part is explained more in detail in client_handler), and by accessing user[1] we can access the client.

Method 4 - def client_handler(client): This method functionality deals with clients. It listens for messages that the client would send to the server, which will contain the username. Client connect_to_server() is behind this, which will be discussed in the client section. The username is received by the server, which is decoded into a readable string format, and while this username exists and is not empty, we can update our list of tracking current clients by appending client and username as tuple attributes to active_clients. The server also deals with clients by providing the prompt message of the server welcoming the client into the chat application (this message of welcoming the client is the parameter passed into send_messages_to_all() which is broadcasted to all currently connected clients. Not to mention, I implemented a thread to concurrently run listen_for_messages (which will continue to keep listening for messages sent from the client side.

main():

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Key Variables of Client Side Chat Application
- host_ip: Variable that defines the IP address to be passed in
- port_addr: Variable that defines the port number to be passed in
- client: Variable that defines a client socket object
- obj: Tkinter variable that beautifies the application

Functionality/Approach: I will be explaining the purpose of each method.

Method 1 - def connect_to_server(): This method effectively connects the client to the server. The client attempts to connect to the server by client.connect() which takes in the host_ip and port address to connect to the server. IF success, I added a test conditional to the print “Connection Success” in the terminal and also passed the same string to output onto the chat application by using insert() (which will be discussed). Connect_to_server relies on a button trigger functionality, which also attains to get the username of the client as the user clicks the “join” button after inputting their name into a textbox (namebox var). This attained username during connect_to_server() is sent to the server through client.sendall() (which is received by client_handler who appends the client to a list of currently active connections and broadcasts this to all currently connected clients, and continues the process.

We concurrently run receive_message (to be discussed) which passes in the client, which will eventually be used to determine the username and actual content of the message, which will then be passed to insert() (who adds the output to the chat application interface)

Method 2 - def receive_message(client): This method takes in a client as a parameter. While the client continues to receive messages back from the server, it decodes the received messages into a readable string format. Provided that the message is not empty, we can split the string message into two separate components. I earlier discussed that by using a special character ‘~’, I was able to split the message into a username component and message component when the client receives the message back in client receive_message. The message and username variables are local variables in the function, which will be passed together as a string to insert(), which inserts who the client is and the message sent on the chat application interface.

Method 3 - def insert(message):  Chatbox is a variable that uses the scrolledtext functionality in the middle frame (Row 1). Scrolledtext will allow us to have a processional order of the messages conversed between the connected clients, however, this is configured and set to a disabled state as we do not want the middle frame to be editable by the client (insert() function will directly output the message).

By default, chatbox is configured to a disabled state and this must be changed in order to directly output “message” that is inputted in insert(message). To do this, we can change the state of the chatbox by configuring it to be normal or “editable”. Then, using chatbox.insert() we will be able to insert messages directly into the middle frame or in other words, the chat application interface. After inputting this, we can set the configuration of chatbox to disabled to ensure nothing else is edited.

Method 4 - def send_message(): This method functionality will send the message to the server. This is the method that sends the message from the client to the server (receiving side is server (listen_for_messages).

mainloop():



	
	




