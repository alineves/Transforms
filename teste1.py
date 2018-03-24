import dcts.wave as wv
import dcts.codec as codec
import dcts.encoded as enc
import numpy as np
import dcts.dct1 as dct1

fs, audData = wv.open_wave("./waves/diadia.wav")

encoded = codec.encode(audData, fs, 0.02, dct1)

encoded.descartar(160)
encoded.saveToFile("./waves/diadia.dct1")

decoded = codec.decodeFromEncoded(encoded, fs, 0.02, dct1)
wv.save_wave("./waves/diadia-final1.wav", fs, decoded, 16)

newEncoded = enc.WaveEncoded.loadFromFile("./waves/diadia.dct1")

decoded = codec.decodeFromEncoded(newEncoded, fs, 0.02, dct1)
wv.save_wave("./waves/diadia-final2.wav", fs, decoded, 16)
