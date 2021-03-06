
from py.Universe import Universe
from threading import Timer

DELTA_T = 0.1 # seconds between updates

class GameManager(object):
    def __init__(self):
        self.sockets = list() # list of all websocket connections open 
        self.universe = Universe()
        self.update_handle = Timer(DELTA_T, self.__update)
        self.update_handle.start()
        self.pauseTime = 0 # amount of time to stay paused

        
    def __update(self):
        # updates the universe
        self.universe._Universe__update(self)
        self.update_handle = Timer(DELTA_T+self.pauseTime, self.__update)
        self.pauseTime = 0
        self.update_handle.start()


    def sendAll(self, m, originator=None, supress=False):
        # sends message to all open websocket connections except for the originator websocket
        for sock in self.sockets:
            if sock != originator:
                sock.send(m)
        if supress == False:
            print 'broadcast message: ',m,' from ...' #TODO: get originator client ID
        
    def parseMessage(self, m, webSock):
        # takes action according to the following message structure:
        # AAA BBB CCC DDD
        # where:
        #   AAA = alphanumeric chars specifying the action to take
        #   BBB = numeric chars specifying the row of the cell 
        #   CCC = numeric chars specifying the column of the cell
        #   DDD = alphanumeric chars containing additional data
        act, row, col, dat = m.split(" ")
        if act == 'set':
            self.universe.cell_list[int(row)][int(col)] = int(dat)
            self.sendAll(m,originator=webSock)
        elif act == 'Hello':
            self.sockets.append(webSock)   # TODO: sockets should be a dict referenced by id # in dat???
            webSock.send('confirm None None Hello');
        elif act == 'goodbye':
            pass # TODO: remove socket from list
        elif act == 'pause':
            self.pauseTime += int(dat)
            self.sendAll('pause None None '+str(self.pauseTime))
        else:
            webSock.send('ERR: bad message: %r ' % m)