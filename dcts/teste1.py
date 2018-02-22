import wave as wv 
import numpy as np

fs, audData = wv.open_wave("./waves/f0001038.wav")

#audData = np.array([1, 2, 3, 4, 1, 2, 3, 4])
#fs = 400

print("Audio: ", audData)
print("Audio: ", len(audData))

encoded = wv.encodeDct1(audData, fs, 0.02)
print("ENCODED: ", encoded)
print("ENCODED: ", len(encoded))

# wv.descartar(encoded, fs, 0.02, 160)

decoded = np.resize(wv.decodeDct1(encoded, fs, 0.02), len(audData))
print("DECODED: ", decoded)
print("DECODED: ", len(decoded))

newAudio = np.rint(wv.desnormalize(decoded)).astype('int16')
wv.save_wave("./waves/f0001038_final.wav", fs, newAudio)