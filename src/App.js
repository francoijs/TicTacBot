/*
  Run web app server with:
  $ npm start
*/

import React from 'react';
import { Client } from 'boardgame.io/react';
import { TicTacToe } from './Game'
import { TicTacToeBoard } from './Board'


const TicTacToeClient = Client({
	game: TicTacToe,
	board: TicTacToeBoard,
	multiplayer: { server: 'localhost:8000' },
});

const App = () => (
  <div>
    <TicTacToeClient playerID="0" />
  </div>
);


export default App;
