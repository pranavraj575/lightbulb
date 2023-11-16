import pyaudio
import struct
import math
from collections import deque

FORMAT = pyaudio.paInt16
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 2
RATE = 44100
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)

def get_rms(block):
    # RMS amplitude is defined as the square root of the
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into
    # a string of 16-bit samples...

    # we will get one short out for each
    # two chars in the string.
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack(format, block)

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
        # sample is a signed short in +/- 32768.
        # normalize it to 1.0
        n = sample*SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt(sum_squares/count)

L = []

class TapTester(object):
    def __init__(self, alpha=.01, z=2.5, startup=10, record=30, restartprop=.3, tapbuff=3, loud=False):
        self.loud = loud
        self.pa = pyaudio.PyAudio()
        self.TOPPY = 0
        self.stream = self.open_mic_stream()
        self.mean = None
        self.var = None
        self.alpha = alpha
        self.z = z
        self.startup = startup
        self.start_count = 0
        self.record = deque(maxlen=record)
        self.restartprop = restartprop
        self.buff = deque(maxlen=tapbuff)
        self.wipe=False
    def stop(self):
        self.stream.close()

    def reset(self):
        self.mean = None
        self.var = None
        self.start_count = 0
        self.record = deque(maxlen=self.record.maxlen)
        self.buff = deque(maxlen=self.buff.maxlen)

    def find_input_device(self):
        device_index = None
        for i in range(self.pa.get_device_count()):
            devinfo = self.pa.get_device_info_by_index(i)
            if self.loud: print("Device %d: %s"%(i, devinfo["name"]))

            for keyword in ["mic", "input"]:
                if keyword in devinfo["name"].lower():
                    if self.loud: print("Found an input: device %d - %s"%(i, devinfo["name"]))
                    device_index = i
                    return device_index

        if self.loud and device_index == None:
            print("No preferred input found; using default input device.")

        return device_index

    def open_mic_stream(self):
        device_index = self.find_input_device()

        stream = self.pa.open(format=FORMAT,
                              channels=CHANNELS,
                              rate=RATE,
                              input=True,
                              input_device_index=device_index,
                              frames_per_buffer=INPUT_FRAMES_PER_BLOCK)

        return stream

    def tapDetected(self, tapped):
        self.buff.append(tapped)
        active=(len(self.buff)==self.buff.maxlen) and not any(list(self.buff)[1:]) and self.buff[0]
        if (len(self.buff)==self.buff.maxlen) and sum(self.buff)>1:
            self.wipe=True
        if active and self.wipe:
            active=False
            self.wipe=False
            self.buff=deque(maxlen=self.buff.maxlen)
        if self.start_count >= self.startup and active:
            self.TOPPY += 1
            if self.loud: print("Tap!")
            print(self.buff)
            self.record.append(True)
        else:
            self.record.append(False)

    def listen(self):
        try:
            block = self.stream.read(INPUT_FRAMES_PER_BLOCK)
        except IOError as e:
            print("bruh:", e)
            return
        global L  # DEBUG

        amplitude = (get_rms(block))
        if self.var != None:
            self.tapDetected(
                amplitude >= self.mean + self.z*self.var**.5
            )

        if self.mean == None:
            self.mean = amplitude
        elif self.var == None:
            self.var = (self.mean - amplitude)**2
        else:
            self.var = self.alpha*(self.mean - amplitude)**2 + (1 - self.alpha)*self.var
            self.mean = self.alpha*amplitude + (1 - self.alpha)*self.mean
        if self.loud: print('\r' + str(amplitude) + '             ', end='')
        if self.record:
            L.append((amplitude, self.mean, self.var, self.record[-1]))  # DEBUG

        if self.start_count <= self.startup:
            self.start_count += 1
        if len(self.record) > self.startup and sum(self.record)/len(self.record) > self.restartprop:
            self.reset()
            if self.loud:print("reset")
        return

if __name__ == "__main__":
    Z = 2.5
    tt = TapTester(loud=True, z=Z)
    for i in range(300):
        tt.listen()
    import matplotlib.pyplot as plt

    L2 = []
    for k in L:
        if None not in k:
            L2.append(k)
    L = L2
    amp=[k[0] for k in L]
    meanie = [k[1] for k in L]
    plt.plot(amp)
    plt.plot(meanie)
    plt.fill_between(range(len(L)), [k[1] - Z*k[2]**.5 for k in L], [k[1] + Z*k[2]**.5 for k in L], alpha=.2)
    plt.plot([k[3]*max(amp) for k in L])
    plt.legend(["amplitudes", "mean", "range", "clappin"])
    plt.show()
