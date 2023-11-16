import asyncio
import numpy as np
import boolb
from threading import Thread

BALLS = 6
TIMOTHY=.42069
REDO=False
BULBUS=[]
LOCK=False


async def pee_check():
    global BULBUS,REDO,LOCK
    while LOCK: pass
    LOCK=True
    test=await boolb.initialize(boolb.broadcastSpace)
    LOCK=False
    if len(test)!=len(BULBUS):
        REDO=True
async def PEE():
    await pee_check()
pee_checker = Thread(target=asyncio.run, args=(PEE(),))
pee_checker.start()
async def penis():
    while True:
        global BULBUS,LOCK,REDO
        while LOCK: pass
        LOCK=True
        BULBUS= await boolb.initialize(boolb.broadcastSpace)
        REDO=False
        LOCK=False
        await nut()

def peepee(yee=.420):
    v = np.random.random(3) - .5
    for i in range(len(v)):
        v[i] = (v[i]/abs(v[i]))*abs(v[i])**(yee) + .5**yee
        v[i] /= 2*.5**yee

    v = 255*v//max(v)
    return v
def poopoo(stuff=((235,97,35),(66,13,171),(40,195,45))):
    v= np.array(stuff[np.random.randint(0,len(stuff))])
    v = 255*v//max(v)
    return v
async def nut():
    global BULBUS,REDO,pee_checker
    async def cum(c, eye=BULBUS):
        await boolb.setRgb(c, eye)
    async def partycum():
        for ball in BULBUS:
            if np.random.randint(0,len(BULBUS),1)>0: continue
            v=peepee()
            await cum(v, [ball])

    async def balls(b):
        await boolb.setBrightness(BULBUS, np.clip(b, 0, 255))

    for i in range(696969):
        try:
            await partycum()
            await balls(255)
            await asyncio.sleep(TIMOTHY)
            if not i%int(10//TIMOTHY) and not pee_checker.is_alive():
                pee_checker = Thread(target=asyncio.run, args=(PEE(),))
                pee_checker.start()
            if not i%int(4.20/TIMOTHY) and np.random.random()<.69:
                print('very '*np.random.randint(0,2)+"funky!!!")
            if REDO:
                break
        except:
            break

asyncio.run(penis())
