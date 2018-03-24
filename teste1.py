import dcts.wave as wv
import dcts.codec as codec
import dcts.encoded as enc
import numpy as np
import dcts.dct1 as dct1

fs, audData = wv.open_wave("./waves/dia.wav")

#audData = np.array([1, 2, 3, 4, 1, 2, 3, 4])
#fs = 400

print("Audio: ", audData)
print("Audio: ", len(audData))

# encodedData = wv.encodeDct1(audData, fs, 0.02)
encoded = codec.encode(audData, fs, 0.02, dct1)
print("TQ: ", fs * 0.02)
encoded.descartar(160)
encoded.saveToFile("./waves/dia.dct1")

newEncoded = enc.WaveEncoded.loadFromFile("./waves/dia.dct1")

# wv.descartar(encoded, fs, 0.02, 160)

# decoded = np.resize(wv.decodeDct1(encoded, fs, 0.02), len(audData))
# print("DECODED: ", decoded)
# print("DECODED: ", len(decoded))

wv.save_wave("./waves/f0001038_final.wav", fs, newAudio, 16)