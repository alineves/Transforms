import dcts.wave as wv
import dcts.codec as codec
import dcts.encoded as enc
import numpy as np
import dcts.dct1 as dct1
import dcts.dct2 as dct2
import dcts.dct3 as dct3
import dcts.dct4 as dct4

fs, audData = wv.open_wave("./waves/m0003022.WAV")

encoded = codec.encode(audData, fs, 0.02, dct4, 0)

encoded.descartar(0)
encoded.saveToFile("./result/m0003022.dct4")

decoded = codec.decodeFromEncoded(encoded, dct4)
wv.save_wave("./result/m0003022-f1dct4.desc0.s0.wav", fs, decoded, 16)

newEncoded = enc.WaveEncoded.loadFromFile("./result/m0003022.dct4")

newdecoded = codec.decodeFromEncoded(newEncoded, dct4)
wv.save_wave("./result/m0003022-f2dct4.desc0.s0.wav", fs, newdecoded, 16)
