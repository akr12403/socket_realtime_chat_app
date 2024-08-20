import socket
import threading
import tkinter as tk 
from tkinter import scrolledtext
from tkinter import messagebox #used for outputting/catching errors

host_ip = '127.0.0.1'
port_addr = 9999

WHITE = "white"
BLACK = "black"
FONT = ("Arial", 17)
BUTTON_FONT = ("Arial", 15)
SMALL_FONT = ("Arial", 13)

obj = tk.Tk() #the following code presents the beautification of the application, using tkinter
obj.title("Socket Programming Chat App")
obj.geometry("600x600") #create an object of tkinter and set the panel to a 600x600 frame titled "Socket Programming Message App"
obj.resizable(False, False) #so application/chat window stays in place

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating a client socket object, AF_INET for ipv4 addresses, SOCK_STREAM for tcp based socket communication

def insert(message): #state of middle frame is disabled as we do not want middle frame to be editable
    chatbox.config(state=tk.NORMAL) #temporarily returns normal state to add insert inputted message (tk.END adds message to end)
    chatbox.insert(tk.END, message + '\n')
    chatbox.config(state=tk.DISABLED) #reaches a disabled state again to not cause any interference

def receive_message(client):
    while True:
        message = client.recv(2048).decode('utf-8') #server sends message to client, who receives this
        if message != '': #if decoded received message not empty, split at symbol to define username component and actual message component
            username = message.split("~")[0]
            content = message.split('~')[1]
            #print(username)
            #print(content)
            insert(f"[{username}] {content}") #adds message to the middle frame 
        else:
            messagebox.showerror("Error", "Message recevied from client is empty")

def connect_to_server():
    try: # tries to connect client to server, server must be running first
        client.connect((host_ip, port_addr))  # Connect to the server
        print("Terminal: Connection Success") #indicates successful connection on terminal
        insert("[SERVER] Connection Successful") #insert enables message to be outputted onto the middle frame to indicate successful connection
    except:
        messagebox.showerror("Cannot connect to server", f"Unable to connect to server {host_ip} {port_addr}") #error indicate unsuccessful connection

    username = namebox.get() #gets the username to be inputted into the white textbox
    if username != '':
        client.sendall(username.encode()) #sends the username to the server or shows error
    else:
        messagebox.showerror("Empty name", "Username cannot be empty") #cannot have no username inputted

    threading.Thread(target=receive_message, args=(client, )).start() #concurrently runs receive message passing in the client, which identifies username and
    #passes it to insert to output which client said what

    namebox.config(state=tk.DISABLED) #cannot re-enter name on same instance so disabled
    join.config(state=tk.DISABLED) #cannot join again on same instance

def send_message(): #method to send actual message to server
    message = message_box.get() #white textbox receives input entry of message to be sent, and client sends byte-formatted message to server and resets textbox
    if message != '':
        client.sendall(message.encode())
        message_box.delete(0, len(message))
    else:
        messagebox.showerror("No input", "Message must contain text") #shows error that empty message cannot be sent to server

obj.grid_rowconfigure(0, weight=1) #sets/allocates the weights for username entry, conversation box, and send message box and assigns rows to specify components
obj.grid_rowconfigure(1, weight=4)
obj.grid_rowconfigure(2, weight=1)

#top = tk.Frame()
#middle = tk.Frame()
#bottom = tk.Frame()

top = tk.Frame(obj, width=600, height=100)
top.grid(row=0, sticky=tk.NSEW) #setting row equivalent to configured row, frame expands and covers all directions

middle = tk.Frame(obj, width=600, height=400)
middle.grid(row=1, sticky=tk.NSEW) #setting row equivalent to configured row, and expanded height for socket communication

bottom = tk.Frame(obj, width=600, height=100)
bottom.grid(row=2, sticky=tk.NSEW) #setting row equivalent to configured row

namebox = tk.Entry(top, font=FONT, bg=WHITE, fg=BLACK, width=32) #will use the .get() method to receive username input within the textbox
namebox.pack(side=tk.LEFT) 

join = tk.Button(top, text="Enter Username", font=BUTTON_FONT, bg=BLACK, fg=WHITE, command=connect_to_server) #username button
join.pack(side=tk.LEFT, padx=15) #upon execution right after inputting, client connects to server (by connecting host ip and port)
#sends username to server, which concurrently runs receive_message as a executing thread to output which user said what

message_box = tk.Entry(bottom, font=FONT, bg=WHITE, fg=BLACK, width=31) #will use the .get() method to receive message input within the textbox 
message_box.pack(side=tk.LEFT, padx=10)

send_message_button = tk.Button(bottom, text="Send Message", font=BUTTON_FONT, bg=BLACK, fg=WHITE, command=send_message)
send_message_button.pack(side=tk.LEFT, padx=10) #upon execution after inputting message
#client sends message to server (which will be received back) and resets textbox for further input

chatbox = scrolledtext.ScrolledText(middle, font=SMALL_FONT, bg=BLACK, fg=WHITE, width=67, height=26.5) #use ScrolledText for processional order of chat messages
chatbox.config(state=tk.DISABLED) #middle is configured so no editing can be done and can be modified to add username and content to the frame using insert
chatbox.pack(side=tk.TOP)

if __name__ == '__main__':
    obj.mainloop()