from scipy.fftpack import dct
from scipy.io.wavfile import read
import numpy as np
import matplotlib.pyplot as plt
import wave

aaa = waves.open("./waves/m0001006.wav")
print("BLA", )


rate, audData = read("./testes/f0001038.wav")
print("r", rate)
print("TESTE", audData[0])

# scale to -1.0 -- 1.0
if audData.dtype == 'int16':
    nb_bits = 16 # -> 16-bit wav files
elif audData.dtype == 'int32':
    nb_bits = 32 # -> 32-bit wav files
max_nb_bit = float(2 ** (nb_bits - 1))
samples = audData / (max_nb_bit)
print("TESTE", samples)
print("max_nb_bit", max_nb_bit)

#time = np.arange(0, float(audData.shape[0]), 1) / rate

#plot amplitude (or loudness) over time
#plt.figure(1)
#plt.subplot(211)
#plt.plot(time, audData, linewidth=0.01, color='#000000')
#plt.xlabel('Time (s)')
#plt.ylabel('Amplitude')
#plt.show()
