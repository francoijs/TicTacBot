#!/usr/bin/python
#
# Copyright 2018 The boardgame.io Authors
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
#
 
import sys, argparse, copy, signal, json, random, time, logging, sys
import socketIO_client as io

logging.basicConfig(level=logging.DEBUG)
running = False

def eprint(str):
    print >> sys.stderr, str


class BoardGameIONamespace(io.BaseNamespace):

    def __init__(self, *args):
        io.BaseNamespace.__init__(self, *args)
        self.game_id = None
        self.previous_state_id = None

    def set_id(self, game_id, player_id):
        self.game_id = game_id
        self.player_id = player_id

    def think(self, state):
        # read state and choose an action
        G = state['G']
        cells = G['cells']
        idx = -1
        while True and None in cells:
            idx = random.randint(0, len(cells)-1)
            if not cells[idx]:
                break
        print('cell chosen: '+str(idx))
        return idx
    
    def on_connect(self):
        eprint('connected')
    def on_disconnect(self):
        eprint('disconnected')
    def on_reconnect(self):
        eprint('reconnected')
    
    def on_sync(self, *args):
        game_id = args[0]
        state = args[1]
        state_id = state['_stateID']
        player = state['ctx']['currentPlayer']
        print 'player:',str(player)
        if game_id==self.game_id:
            if not self.previous_state_id or state_id>=self.previous_state_id:
                self.previous_state_id = state_id
                if player == self.player_id:
                    action = {
                        'type': 'MAKE_MOVE',
                        'payload': {
                            'type': 'clickCell',
                            'args': self.think(state),
                            'playerID': self.player_id
                        }
                    }
                    self.action(action, state_id, game_id, self.player_id)

    def on_action(self, *args):
        game_id = args[0]
        state = args[1]
        print state        

    def action(self, action, state_id, game_id, player_id):
        self.emit('action', action, state_id, game_id, player_id)


class BoardGameIOClient(object):

    def __init__(self, server='localhost', port=8000, game='default', player_id='1'):
        self.game_id = 'default:'+game
        self.player_id = player_id
        # open websocket
        socket = io.SocketIO(server, port, wait_for_connection=False)
        socket.define(io.LoggingNamespace, '/'+game)
        self.game_namespace = socket.define(BoardGameIONamespace, '/'+game)
        self.game_namespace.set_id(self.game_id, player_id)
        self.socket = socket
        # initial sync
        self.sync(game, player_id, 2)

    def listen(self):
        self.socket.wait(seconds=1)
#        self.sync(self.game_id, self.player_id, 2)

    def sync(self, game_id, player_id, num_players):
        self.game_namespace.emit('sync', self.game_id, player_id, num_players)


def main(argv=sys.argv):
    eprint('starting python client...')
    client = BoardGameIOClient()

    global running
    running = True
    while running:
        client.listen()
        
    eprint('python bot ended.')

def stop(signum, frame):
    eprint('stopping...')
    global running
    running = False
    
# start process
if __name__ == '__main__':
    # sigterm
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    main()
