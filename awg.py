
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


def prev_int_mult_128(n):
  return np.max([int((n)/128)*128,128]) # multiples of 128



def gauss(x, **kwargs):
  mu = kwargs.get("mu",0)
  sigma = kwargs.get("sigma",1)
  ## default amplitude A generates bell curve with area = 1
  A = kwargs.get("A",1./(sigma*(2.*np.pi)**0.5)) 
  return A*np.exp(-(x-mu)**2/(2.*sigma**2))




def send_sine(f):


    f = int(f)
    wfml = int(65e9/f) # waveform length (number of (x, y) pairs that describe the wave)
    wfml = (wfml + 127) >> 7 << 7 # round up to next multiple of 128 for protocol reasons
    # sample_rate = f * wfml
    x = np.linspace(0, 3, wfml)
    # y=gauss(x,sigma=20e-9,mu=300e-9,A=200e-3)
    # y = np.cos(x)
    y = 1 / (1 + np.exp(x))
    v = np.amax(abs(y))
    
    data = (y * 127 / v).astype(np.int64) # 127 probably has a reason, but is magic to me.
    data = ",".join(map(str, data))
    period = 1e-6
    # Set sample rate and delete old wave.
    sample_rate = 65e9
    MAX_MEM_SIZE = 262144
    mem_size = prev_int_mult_128(int(period * sample_rate))
    mem_size = np.min([mem_size,MAX_MEM_SIZE])
    hypothetical_period = 1/sample_rate*mem_size
    rate_scaler = hypothetical_period/period
    sample_rate *= rate_scaler
    sample_rate = int(sample_rate)

    print("this is", sample_rate)

    command(":INIT:IMM")
    command(f":SOUR:FREQ:RAST:{sample_rate}")
    command(f":ABOR")
    command(f":TRAC1:DEL:ALL")

    

    # Send new data
    command(f":TRAC1:DEF 1,{wfml},0")
    command(f":TRAC1:DATA 1,0,{data}")
    command(f":VOLT1 {v:3.3f}")
    command(f":OUTP1 ON")
    command(f":INIT:IMM")
    plt.plot(x*1e9,y)
    plt.xlabel("time (ns)")
    plt.ylabel("voltage (V)")
    plt.show()
def command(s):
    awg.sendall(str.encode(s + "\n"))

send_sine(2e6)

awg.close()


