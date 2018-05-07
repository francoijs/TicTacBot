/*
  Run multiplayer server with:
  $ npx babel-node --presets zero src/Server.js
*/

const Server = require('boardgame.io/server').Server;
const TicTacToe = require('./Game.js').TicTacToe;
const PythonBot = require('./PythonBot.js').PythonBot;


const server = Server({
	games: [TicTacToe],
});

server.run(8000);

// const bot = new PythonBot({
// 	game: TicTacToe,
// 	server: 'localhost:8000',
// 	playerID: '1'
// });
