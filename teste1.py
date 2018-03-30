import dcts.wave as wv
import dcts.codec as codec
import dcts.encoded as enc
import numpy as np
import dcts.dct1 as dct1
import dcts.dct2 as dct2

fs, audData = wv.open_wave("./waves/m0003022.WAV")

encoded = codec.encode(audData, fs, 0.02, dct2, 0)

encoded.descartar(0)
encoded.saveToFile("./waves/m0003022.dct1")

decoded = codec.decodeFromEncoded(encoded, dct2)
wv.save_wave("./waves/m0003022-f1dct1.desc0.s0.wav", fs, decoded, 16)

newEncoded = enc.WaveEncoded.loadFromFile("./waves/m0003022.dct1")

decoded = codec.decodeFromEncoded(newEncoded, dct1)
wv.save_wave("./waves/m0003022-f2dct1.desc0.s0.wav", fs, decoded, 16)
