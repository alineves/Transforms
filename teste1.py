import dcts.wave as wv
import dcts.codec as codec
import dcts.encoded as enc
import numpy as np
import dcts.dct1 as dct1

fs, audData = wv.open_wave("./waves/m0003022.WAV")

encoded = codec.encode(audData, fs, 0.02, dct1, 20)

encoded.descartar(200)
encoded.saveToFile("./waves/m0003022.sdct1")

decoded = codec.decodeFromEncoded(encoded, dct1)
wv.save_wave("./waves/m0003022-f1.200.s20.wav", fs, decoded, 16)

newEncoded = enc.WaveEncoded.loadFromFile("./waves/m0003022.sdct1")

decoded = codec.decodeFromEncoded(newEncoded, dct1)
wv.save_wave("./waves/m0003022-f2.200.s20.wav", fs, decoded, 16)
