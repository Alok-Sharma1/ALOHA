from glob import glob
from numpy import random
from time import sleep, time
import threading
import sys
from queue import Queue

Tfr = float(input("Please enter Tfr(seconds)\nEnter 0 for default 10 miliseconds: "))
if Tfr == 0.0:
    Tfr = 0.01

duration = int(input("Please enter duration of simulation(seconds): "))

transmissions = 0
failedFrames = 0
channelBusy = False
lock = threading.Lock()

q = Queue()
semaphore = threading.Semaphore(11)

def runALOHAnode():
    global Tfr
    global transmissions
    global failedFrames
    global channelBusy
    global lock
    global q

    while True:
        waitTime = random.exponential(0.5,None)
        ]
        sleep(waitTime)

        #Start transmiting
        transmissions += 1

        #If channel is busy(lock is locked!).
        if lock.locked():
            #Collision happens but still transmiting the frame
            failedFrames += 1
            #Put data in queue to tell other sending nodes that this is a collision and their transmitted frame is failed
            q.put(1)
            #Sleeping for Tfr seconds means that node is transmitting and it takes Tfr seconds.
            sleep(Tfr)

        #If channel is not occupied(lock is unlocked).
        else:
            lock.acquire()
            collision = False
            channelBusy = True
            startTime = time()
            seconds = Tfr
            #Sleeping for Tfr seconds means that node is transmitting and it takes Tfr seconds.
            while True:
                currentTime = time()
                elapsedTime = currentTime - startTime

                if q.empty():
                    pass
                #q being not empty means some other node(s) are transmitting too and this transmission is failed because of collision.
                else:
                    collision = True

                if elapsedTime > seconds:
                    break
            
            q.queue.clear()
            channelBusy = False
            lock.release()
            semaphore.acquire()
            if collision:
                failedFrames += 1
            semaphore.release()

#Creating threads and starting them.
node1 = threading.Thread(target = runALOHAnode)
node1.daemon = True
node1.start()

node2 = threading.Thread(target = runALOHAnode)
node2.daemon = True
node2.start()

node3 = threading.Thread(target = runALOHAnode)
node3.daemon = True
node3.start()

node4 = threading.Thread(target = runALOHAnode)
node4.daemon = True
node4.start()

node5 = threading.Thread(target = runALOHAnode)
node5.daemon = True
node5.start()

node6 = threading.Thread(target = runALOHAnode)
node6.daemon = True
node6.start()

node7 = threading.Thread(target = runALOHAnode)
node7.daemon = True
node7.start()

node8 = threading.Thread(target = runALOHAnode)
node8.daemon = True
node8.start()

node9 = threading.Thread(target = runALOHAnode)
node9.daemon = True
node9.start()

node10 = threading.Thread(target = runALOHAnode)
node10.daemon = True
node10.start()

#wait for threads to run for a while.
print("Please wait...\n")
sleep(duration)

successfulFrames = transmissions - failedFrames

print("Transmited frames: " + str(transmissions))
print("Failed frames: " + str(failedFrames))
print("Successful frames: " + str(successfulFrames))
print("Throughput(kbps): " + str((successfulFrames)/duration))

sys.exit()
