#!/usr/bin/python

import sys, argparse, copy, signal, json, random


running = True

def eprint(str):
    print >> sys.stderr, str

def main(argv=sys.argv):

    eprint('starting python bot...')
    
    while running:
        try:
            line = sys.stdin.readline()
            eprint('received '+line)
            jst = json.loads(line)
            
            # read state and choose an action
            cells = jst['cells']
            idx = -1
            while True:
                idx = random.randint(0, len(cells)-1)
                if not cells[idx]:
                    break
            eprint('cell chosen: '+str(idx))
            
            # send action through stdout
            print str(idx)
            sys.stdout.flush()
            
        except Exception as e:
            eprint(str(e))
    
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
