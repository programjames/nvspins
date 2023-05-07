
import socket
import numpy as np
import matplotlib.pyplot as plt
# import M8195A as awg

awg_ip = "169.254.28.215"
port = 5025
awg=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

print("Connecting to AWG...")
awg.connect((awg_ip,port))
print("Connected!")


def wavelet(x):
    return np.exp(-x)

def send(wavelet, nv_freq, r):
    """
    wavelet - The ML learned wavelet to set the spins
    nv_freq - The frequency used for readout
    r - Number of readout waves ('r'epeat nv_freq r times)
    """

    nv_freq = int(nv_freq)
    wfml = int(64e9 * r / 128 / nv_freq) # waveform length (number of (x, y) pairs that describe the wave)
    wfml *= 128 # Has to be a multiple of 128 for protocol reasons
    sample_rate = wfml * nv_freq // r

    x = np.linspace(0, r, wfml)
    y1 = wavelet(x)
    y2 = np.sin(2*np.pi*x)
    v = np.amax(abs(np.r_[y1, y2]))
    
    def to_data(y):
        y = (y * 127 / v).astype(np.int64) # format as int between +/- 127
        return ",".join(map(str, y))

    command(f":INIT:IMM")
    command(f":SOUR:FREQ:RAST {sample_rate}")
    command(f":ABOR")
    command(f":TRAC1:DEL:ALL")

    

    # Send new data
    command(f":TRAC1:DEF:WONL 1,{10*wfml},0")
    command(f":TRAC1:DATA 1,0,{to_data(y1)}")
    command(f":TRAC1:DATA 1,{3*wfml},{to_data(y2)}")
    command(f":VOLT1 {v:3.3f}")
    command(f":OUTP1 ON")
    command(f":INIT:IMM")

def command(s):
    awg.sendall(str.encode(s + "\n"))

send(wavelet, 1e6, 3)

awg.close()


