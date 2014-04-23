#!/usr/bin/env python

#=====================================#
#              WEB LIFE               #
#=====================================#
#                 by:                 #
#             Tylar Murray            #
#                                     #
#=====================================#
__author__ = '7yl4r'

#=====================================#
#         std lib imports             #
#=====================================#
import os
import sys
from time import time

#=====================================#
#         included lib imports        #
#=====================================#
from py.lib.bottle import route, template, run, static_file, Bottle, request, abort
import gevent
from geventwebsocket import WebSocketServer, WebSocketApplication, Resource

#=====================================#
#            package imports          #
#=====================================#
from py.GameManager import GameManager

#=====================================#
#            globals                  #
#=====================================# 
app = Bottle()
DOMAIN = 'localhost' # domain name

game_manager = GameManager()

# temporary hacks:             
UPDATE_COUNTDOWN = 5    # seconds until update is called
CLIENT_ID = 0



#=====================================#
#           Splash Page               #
#=====================================#
@app.route("/")
def makeSplash():
    return template('tpl/pages/splash')

#=====================================#
#             main page               #
#=====================================#
@app.route("/live")
def makeLife():
    return template('tpl/pages/basic',
        cellList=game_manager.universe.cell_list, 
        timeLeft=int(game_manager.universe.sched_update-time()), 
        DOMAIN=DOMAIN, 
        client_id=0)
    
#=====================================#
#            Static Routing           #
#=====================================#
@app.route('/css/<filename:path>')
def css_static(filename):
    return static_file(filename, root='./css/')

@app.route('/js/<filename:path>')
def js_static(filename):
    return static_file(filename, root='./js/')
    
#=====================================#
#           websockets                #
#=====================================#
# class EchoApplication(WebSocketApplication):
    # def on_open(self):
        # print "Connection opened"

    # def on_message(self, message):
        # self.ws.send(message)

    # def on_close(self, reason):
        # print reason

        
@app.route('/websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    while True:
        try:
            message = wsock.receive()
            print "received : "+str(message)
            game_manager.parseMessage(message,wsock)
            
        except WebSocketError:
            break
            
        
#=====================================#
#          WEB SERVER START           #
#=====================================#

if __name__ == "__main__":

    from gevent.pywsgi import WSGIServer
    from geventwebsocket.handler import WebSocketHandler
    from geventwebsocket import WebSocketError
    
    port = int(os.environ.get("PORT", 80))
    server = WSGIServer(("0.0.0.0", port), app,
                        handler_class=WebSocketHandler)
    print 'starting server on '+str(port)
    server.serve_forever()
    # ^that^ == app.run(host='0.0.0.0', port=port)
    