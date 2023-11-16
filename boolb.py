from pywizlight import wizlight, PilotBuilder, discovery
import sys
broadcastSpace = "192.168.1.255" #Your lights' broadcast space

async def initialize(broadcastSpace):
    bulbs=[]
    unsortedIPs = []

    # Add all bulbs to an unsorted list
    bulbsUnsorted = await discovery.discover_lights(broadcast_space=broadcastSpace)
    # Sorts all the bulbs and appends them to a new list
    for x in bulbsUnsorted:
        unsortedIPs.append(x.ip)

    unsortedIPs = sorted(unsortedIPs)

    for x in unsortedIPs:
        for y in bulbsUnsorted:
            if x == y.ip: bulbs.append(y)
    return bulbs

async def changeColor(bulbs, color):
    for bulb in bulbs:
        await bulb.turn_on(PilotBuilder(rgb=(color)))

async def setBrightness(bulbs, newBrightness):
    newBrightness = int(newBrightness)
    for bulb in bulbs:
        await bulb.turn_on(PilotBuilder(brightness=newBrightness))

async def setScene(bulbs, scene):
    scene = int(scene)
    for bulb in bulbs:
        await bulb.turn_on(PilotBuilder(scene=scene))

async def setOff(bulbs):
    for bulb in bulbs:
        await bulb.turn_off()

async def setWhite(value, brightness, bulbs):
    brightness = int(brightness)
    newColor = PilotBuilder(cold_white=255)  # Defaults to cold white
    if value == "cold": newColor = PilotBuilder(cold_white=brightness)
    if value == "warm": newColor = PilotBuilder(warm_white=brightness)
    for bulb in bulbs:
        await bulb.turn_on(newColor)

async def setRgb(value, bulbs):
    await changeColor(bulbs, (int(value[0]), int(value[1]), int(value[2])))

sys.path.append('/bulbScript_functions')
sys.path.append('/user_functions')