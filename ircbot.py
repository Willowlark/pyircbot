"""An irc bot program. Commands will be variable and modifiable.
 
Example PRIVMSG command:
:natsuPaw_!~piro@24.115.128.97.res-cmts.sesh.ptd.net PRIVMSG #rowancsc :hello world
"""

import sys
import socket

class Message():
    hostname = ''
    def __init__(self, mess):
        data = mess.split(' ')
        self.command = data[1] #the command of the mess
        if self.command == 'PRIVMSG':
            self.type = 'msg' #for internal use
            self.target = data[2]
            self.message = mess.split(':')[2]
            self.split_msg = self.message.split(' ')
            self.nick = mess.split('!')[0][1:]
            # self.hostname = mess.split('!')[1].split(' ')[0]
        elif data[0] == "PING":
            self.type = 'PING'
            self.target = data[1][1:]
        elif data[1] == 'JOIN' and Message.hostname == '':
            self.type = 'nil'
            Message.hostname = data[0].split('@')[1]
        else:
            self.type = 'nil' #for internal use


def do_cmd(command=""):
    s.sendall("PRIVMSG #" + channel + " :\001ACTION does " + command +"\001\r\n")

def fe_cmd(command):
    pass

def processMessage(message):
    if message.type == 'msg' and message.target == nick: #Private message to the bot
        if message.split_msg[0] in commands:
            commands[message.split_msg[0]](' '.join(message.split_msg[1:]))
        elif message.split_msg[0] is 'fe':
            pass
        else:
            s.sendall('PRIVMSG ' + message.nick + ' :This is not one of my commands.\r\n')
    elif message.type == "PING":
        s.sendall('PONG ' + message.target+'\r\n')
    if message.type == 'nil': #place holder for other message type handling
        pass





#Actual program

#Get & declare vars from command line
commands = {'do':do_cmd, 'fe':fe_cmd} #dictionary of avaiable command keywords : functions.
server, nick, channel = '', '', ''

args = sys.argv[1:]
if len(args) == 3:
    server, nick, channel = args
else:
    print 'Invalid params, server nick channel'
    print args
    exit()

#make a connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, 6667))

#register with the server and join the channel
s.sendall('pass secret\r\n')
s.sendall('nick ' + nick + '\r\n')
s.sendall('user ' + nick +  ' 8  *' + ' : ' + "Paw's bot\r\n")
s.sendall('JOIN #' + channel + '\r\n')

#program loop
while 1:
    data = s.recv(1024)
    mess = Message(data)
    processMessage(mess)
    print data
