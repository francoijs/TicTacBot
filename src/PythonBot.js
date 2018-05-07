/*
 * Copyright 2018 The boardgame.io Authors
 *
 * Use of this source code is governed by a MIT-style
 * license that can be found in the LICENSE file or at
 * https://opensource.org/licenses/MIT.
 */

const ChildProcess = require('./ChildProcess.js').ChildProcess;
const Client = require('boardgame.io/react').Client;


export class PythonBot {
	constructor({
		game,
		server,
		playerID
	}) {
		// python subprocess
		this.py = new ChildProcess({
			args: ['python', 'src/tictacbot.py'],
			callback: this._childData.bind(this)
		});
		
		// MP client
		const BotClient = Client({
			game: game,
			multiplayer: { server: server },
//			enhancer: applyMiddleware(logger)
		});
		this.playerID = playerID;
		this.client = new BotClient({
			playerID: this.playerID,
			gameID: "default"
		}).client;
		
		// subscribe to Redux events
		this.client.multiplayerClient.store.subscribe(
			this._gameEvent.bind(this)
		);
		this.client.multiplayerClient.connect();
	}

	_gameEvent() {
		try {
			let state = this.client.getState();
			if (state.ctx.currentPlayer !== this.playerID)
				return
			console.log('G:', state.G);
			// send state to python subprocess
			this.py.write(JSON.stringify(state.G)+'\r\n');
		}
		catch(e) {
			console.log('exception:', e);
		}
	}

	_childData(str) {
		try {
			// handle action received from python subprocess
			var cell = parseInt(str.trim());
			let state = this.client.getState();
			let that = this
			// wait 1s before playing
			new Promise(resolve => setTimeout(resolve, 1000)).then(function() {
				that.client.moves['clickCell'](cell);
				/* FIXME: for some reason, event 'endTurn' is not always properly handled
				*/
				that.client.events['endTurn']();
			});
		}
		catch(e) {
			console.log('exception:', e);
		}
	}
};
