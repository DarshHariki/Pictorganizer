import time
import threading
from getch import getch

def doing_things():
    #print 'Just livin my life, doing execution things.'
    #time.sleep(3)
    pass

def waiting_for_buttons():
    stop = False
    n = 0
    while not stop:
        k = getch()
        t_start = time.time()
        t = time.time()-t_start
        kn = 0
        while t < 0.25 and kn < 3:
            k += getch()
            kn += 1
            print 'Got a '+repr(k), kn
            t = time.time()-t_start
            
        print
        print repr(k), '#'+str(n)
        print
        n += 1
        if k == '\x1b[C':
            print 'NEXT'
        elif k == '\x1b[D':
            print 'PREV'
        elif k == 'q':
            stop = True

if __name__ == '__main__':
    thread1 = threading.Thread(target=waiting_for_buttons)
    thread1.start()
    while True:
        k = raw_input('Wat u want?')
        if k == 'k':
            thread1._stop_event.set()
            print 'Killed thread?'

