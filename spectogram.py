import pyaudio
import struct
import numpy as np
import time
import os
import sys
from constants import RATE, INPUT_FRAMES_PER_BLOCK

rows, cols = os.popen('stty size', 'r').read().split()

rows = int(rows)
cols = int(cols)

def main():
    audio = pyaudio.PyAudio()
    try:
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=INPUT_FRAMES_PER_BLOCK
                           )

        #maximal = Amplitude()
        while True:
            data = stream.read(INPUT_FRAMES_PER_BLOCK)
            #amp = Amplitude.from_data(data)
            #if amp > maximal:
                # maximal = amp
            # amp.display(scale=100, mark=maximal)
            count = len(data) / 2
            x = struct.unpack("%dh" % count, data)
            #avg = sum(shorts) / count;
            # print(len(x))

            X = np.fft.fft(x)
            X = X[0:int(count / 2)]

            bins = cols
            chunks = np.zeros(bins)
            for i in range(0,bins):
                chunks[i] = sum([np.abs(a) for a in X[i*int(len(X)/bins):(i+1)*int(len(X)/bins)]])
                chunks[i] = 10 * np.log10(chunks[i])

            # sys.stdout.write('\x0C')
            os.system('clear')
            for i, chunk in enumerate(chunks):
                # print('%.1f\t\t' % chunk, end='')
                # sys.stdout.write('%.1f\t\t' % chunk)
                for j in range(int(chunk / 4)):
                    if 0 <= j < 5:
                        color = '\x1b[0;32;42m#'
                    elif 5 <= j < 10:
                        color = '\x1b[0;33;43m#'
                    else:
                        color = '\x1b[0;31;41m#'
                    print_there(rows - j, i*1, color)
            sys.stdout.flush()

            # time.sleep(0.001)

    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

def print_there(x, y, text):
     sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
     sys.stdout.flush()

if __name__ == "__main__":
    main()
