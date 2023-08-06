from aernetworking import * # this will import everything we need from AerNetworking with just one line.

def handler(connection, address): # this function will be run on the new connection
    print("New Connection.")

    message = "Welcome to my server!" 

    server.send(connection = connection, data = message) # this will send message to connection

server = Server()

server.ip = server.get_local_ip()
server.port = 5656

server.listen(function = handler)