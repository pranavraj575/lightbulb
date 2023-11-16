import asyncio
import numpy as np
from threading import Thread
from clap_back import *
import boolb
BULBUS=[]
tt=TapTester(loud=True)
async def penis():
    global BULBUS
    BULBUS=await boolb.initialize(boolb.broadcastSpace)
    await nut()
async def nut():
    async def cum(c,eye=BULBUS):
        await boolb.setRgb(c,eye)
    async def balls(b,eye=BULBUS):
        await boolb.setBrightness(eye,np.clip(b,0,255))
    async def rip(eye=BULBUS):
        await boolb.setOff(eye)
    on=True
    def pee():
        while True:
            tt.listen()
    poopy=Thread(target=pee,daemon=True)
    poopy.start()
    old=0
    while True:
        #await asyncio.sleep(1)

        if tt.TOPPY!=old:
            if on:
                v=np.random.randint(0, 255, 3)
                v=255*v//max(v)
                await cum(v)
                await balls(255)
            else:
                await rip()
            on=not on
            await asyncio.sleep(1)
            old=tt.TOPPY
        #await cum(np.random.randint(0,255,3))
        #await balls(np.random.randint(0,255,1))


asyncio.run(penis())