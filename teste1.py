import dcts.wave as wv
import dcts.codec as codec
import dcts.encoded as enc
import numpy as np
import dcts.dct1 as dct1
import dcts.dct2 as dct2
import dcts.dct3 as dct3
import dcts.dct4 as dct4

fs, audData = wv.open_wave("./waves/f0001038.16k.WAV")

encoded = codec.encode(audData, fs, 0.02, dct2, 20)

encoded.descartar(160)
encoded.saveToFile("./result/f0001038.16k.dct4")

decoded = codec.decodeFromEncoded(encoded, dct4)
wv.save_wave("./result/f0001038.16k-f1dct4.desc160.s20.wav", fs, decoded, 16)

newEncoded = enc.WaveEncoded.loadFromFile("./result/f0001038.16k.dct4")

newdecoded = codec.decodeFromEncoded(newEncoded, dct4)
wv.save_wave("./result/f0001038.16k-f2dct4.desc160.s20.wav", fs, newdecoded, 16)
