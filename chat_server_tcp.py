import socket
import sys
import thread

def clientThread(conn):

    #conn.send("Connecting to the server... \n")

    data = conn.recv(1024)
    dataParseCommand = data.split('>')
    command = dataParseCommand[0]
    print('Received <' + command +'> command...\n')

    if(command == 'register'):
        print('Register procedure started...\n')
        reply = loginUser(dataParseCommand[1])
        conn.sendall(reply)
    if(command == 'quit'):
        print('Quit procedure started...\n')
        reply = removeUser(dataParseCommand[1].split('|')[0])
        conn.sendall(reply)
    if(command == 'getUser'):
        reply = getExistingUser(dataParseCommand[1].split('|')[0])
        conn.sendall(reply)
    if(command == 'userList'):
        reply = userList()
        conn.sendall(reply)
    conn.close()

def loginUser(data):
    dataParseName = data.split('|')
    username = dataParseName[0]
    dataParseAddress = dataParseName[1].split(':')
    userIpAddr = dataParseAddress[0]
    userPort = dataParseAddress[1]
    if not (checkExistingUserName(username)):
        addNewUser(username, userIpAddr, userPort)
        print (' -- User successfully registered --\n'
           ' -- Username: ' + username + ' --\n'
           ' -- Ip Address: ' + userIpAddr + ' --\n'
           ' -- Ip Port: ' + userPort + ' --\n')
        return username + ', you correctly joined our chat!\n'
    else:
        return 'ERROR | User <' + username + '> already exists, please choose a different nickname'

def addNewUser(name, address, port):
    activeUsers[name] = [address, port]
    print ('User registered, updating dictionary...', activeUsers)

def getExistingUser(name):
    if(checkExistingUserName(name)):
        print ('Retrieving user <' + name + '>...')
        address = activeUsers.get(name)[0]
        port = activeUsers.get(name)[1]
        return name + ' | ' + address + ' | ' + port
    else:
        return ('User <' + name + '> does not exist...')

def checkExistingUserName(name):
    print ('Checking if user <' + name + '> is already registered...')
    return activeUsers.get(name) is not None and len(activeUsers.get(name)) > 0

def userList():
    print ('Retrieving registered users...')
    userList = activeUsers.keys()
    userListFlat = ''
    for user in userList:
        userListFlat += user + ' - '
    return userListFlat

def removeUser(name):
    print ('Removing user <' + name +'>...')
    if activeUsers.get(name):
        activeUsers.pop(name)
    print ('User removed, updating dictionary...', activeUsers)
    return ('See you soon, ' + name + '...')


HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

activeUsers = dict([('DummyUser', ['0.0.0.0', '8080'])])
print ('Init dictionary : ', activeUsers)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

s.listen(100)
print 'Socket now listening'

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    print 'Waiting for users to open a connection...\n'
     #wait to accept a connection - blocking call
    conn, addr = s.accept()
    try:
        thread.start_new_thread(clientThread, (conn,))
        print ('Receiving registration from: ' + addr[0] + ':' + str(addr[1])+'\n')
    except thread.error, msg:
        print 'Connection failed. Error Code : '  + str(msg[0]) + ' Message ' + msg[1]

s.close()
