import asyncio
import numpy as np
import boolb
from threading import Thread
import sys

cums=sys.argv[1:]
try:
    v=np.array([int(cums[i]) for i in range(3)])
except:
    v=np.array((255,200,200))

BALLS = 6
REDO=False
BULBUS=[]
LOCK=False
trials=1
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
    for _ in range(trials):
        global BULBUS,LOCK,REDO
        while LOCK: pass
        LOCK=True
        BULBUS= await boolb.initialize(boolb.broadcastSpace)
        REDO=False
        LOCK=False
        await nut()

async def nut():
    global BULBUS,REDO,pee_checker
    async def cum(c, eye=BULBUS):
        await boolb.setRgb(c, eye)
    async def balls(b):
        await boolb.setBrightness(BULBUS, np.clip(b, 0, 255))
    for ball in BULBUS:
        await cum(v, [ball])
    await balls(255)


asyncio.run(penis())
