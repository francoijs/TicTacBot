/*
 * Copyright 2018 The boardgame.io Authors
 *
 * Use of this source code is governed by a MIT-style
 * license that can be found in the LICENSE file or at
 * https://opensource.org/licenses/MIT.
 */

const spawn = require('child_process').spawn;


export class ChildProcess {
	constructor({
		args,
		callback
	}) {
		var child = spawn(args[0], args.slice(1));
		child.stderr.on('data', function(data) {
			let str = data.toString().trim();
			console.log(args[0]+'['+child.pid+']:', str);
		});
		child.stdout.on('data', function(data) {
			let str = data.toString().trim();
			callback(str);
		});
		child.stdout.on('end', function() {
			console.log('Subprocess '+args[0]+' ended.');
		});
		child.on('error', (err) => {
			console.log('Failed to start subprocess.');
		});
		this.process = child;
	}

	write(str) {
		this.process.stdin.write(str);
	}
};
