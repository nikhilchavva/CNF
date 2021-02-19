import socket                    
import os
import subprocess
import base64
import csv
from _thread import *
import threading
"""
*Creating and implementing basic http requests to handle different types of files and by multithreading improved the performance using python language and mime-types for handling file types.

*Created a server using python socket programming and was able to create a connection between server and client and was able to get response from server.

*Created basic HTTP requests like GET and HEAD. We will be sending the requests from the web browser and receive the response from the server. Using postman app to check GET and HEAD 

*Displaying the files in the directory and if we access any files we can see the files in the directory

*Using multithreading to achieve concurrency.

"""

# @author: Nikhi Chavva

#reference from https://www.codementor.io/@joaojonesventura/building-a-basic-http-server-from-scratch-in-python-1cedkg0842
#reference from https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET
#reference from https://www.codecademy.com/articles/http-requests
#reference from https://reqbin.com/Article/HttpHead
#reference from https://www.postman.com/downloads/ (postman to check get and head request)
#reference from https://docs.python.org/3/library/os.html
#reference from https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types



def threaded(client_connection):
    request = client_connection.recv(1024).decode()
    if request:
        request_method = request.splitlines()[0].rstrip('\r\n')
        request_method = request_method.split()
        if request_method[0] == 'GET':                      #requesting get method
            print(request)
            if request_method[1] == '//':
                response = 'HTTP/1.0 404 NOT FOUND\r\n Request not found. Try again.'     #http response
                client_connection.sendall(response.encode())
            else:
                 file_p=os.path.abspath(".")
                 handle_request(request, file_p)
        elif request_method[0]=="HEAD":
            response = 'HTTP/1.0 200 OK\r\nlook for another request'
            client_connection.sendall(response.encode())
        else:
            response = 'HTTP/1.0 404 NOT FOUND\r\n Request not found. Try again.'
            client_connection.sendall(response.encode())
        # Close connection
        client_connection.close()

def handle_request(request, file_p):                #handlerequest
    headers= request.split('/n')

    filename=headers[0].split()[1]
    file_p += filename
    if (file_p.endswith("favicon.ico")):
        response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'
        client_connection.send(response.encode())
    else:
        file_p=os.path.abspath(".")
        file_p += filename
        print(filename)
        print("there")
        print(file_p)
        if(os.path.isfile(file_p)):
            extension=file_p.split('.')[-1]
            print(extension)
            extension = extension.lower()
            if extension == 'png':
                response = 'HTTP/1.0 200 OK\r\n'
                mime_type = 'Content-Type:image/png\r\n\r\n'           #using mime type for filetype
                print("__________________________________")
                print(file_p)
                x=open(file_p,'rb').read()
                client_connection.send((response+mime_type).encode()+x)
            elif extension == 'jpeg':
                response = 'HTTP/1.0 200 OK\r\n'
                mime_type = 'Content-Type:image/jpeg\r\n\r\n'         #using mime type for filetype
                print("__________________________________")
                print(file_p)
                x=open(file_p,'rb').read()
                client_connection.send((response+mime_type).encode()+x)
            elif extension== 'pdf':
                response = 'HTTP/1.0 200 OK\r\n'
                mime_type = 'Content-Type:Application/pdf\r\n\r\n'        #using mime type for filetype
                print("__________________________________")
                print(file_p)
                x=open(file_p,'rb').read()
                client_connection.send((response+mime_type).encode()+x)
            elif extension== 'mp4':
                response = 'HTTP/1.0 200 OK\r\n'
                mime_type = 'Content-Type:video/mp4\r\n\r\n'               #using mime type for filetype
                print("__________________________________")
                print(file_p)
                x=open(file_p,'rb').read()
                client_connection.send((response+mime_type).encode()+x)
            elif extension== 'mpeg':
                response = 'HTTP/1.0 200 OK\r\n'
                mime_type = 'Content-Type:audio/mpeg\r\n\r\n'            #using mime type for filetype
                print("__________________________________")
                print(file_p)
                x=open(file_p,'rb').read()
                client_connection.send((response+mime_type).encode()+x)
            elif extension== 'py':
                response = 'HTTP/1.0 200 OK\r\n'
                mime_type = 'Content-Type:text/html\r\n\r\n'                   #using mime type for filetype
                print("__________________________________")
                print(file_p)
                x=open(file_p,'rb').read()
                client_connection.send((response+mime_type).encode()+x)
        elif(os.path.isdir(file_p)):
            lists_avail=os.listdir(file_p)
            print("Twice")
            msg = 'HTTP/1.0 200 OK\r\n'
            msg +='Content-Type:text/html\r\n\r\n'
            for i in lists_avail:
                j=os.path.abspath(i)
                msg += "<a href="+i+">"+i+"</a> <br>"
            client_connection.sendall(msg.encode())
        else:
            response = 'HTTP/1.0 404 NOT FOUND\r\nFile Not Found'
            client_connection.send(response.encode())

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT) 

while True:
    # Wait for client connections
    client_connection, client_address = server_socket.accept()
    start_new_thread(threaded, (client_connection,)) 

server_socket.close()