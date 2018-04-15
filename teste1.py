import dcts.wave as wv
import dcts.codec as codec
import dcts.encoded as enc
import numpy as np
import dcts.dct1 as dct1
import dcts.dct2 as dct2
import dcts.dct3 as dct3
import dcts.dct4 as dct4
import time

def current_milli_time():
    return int(round(time.time() * 1000))

fs, audData = wv.open_wave("./waves/f0001038.16k.WAV")

b = current_milli_time()
encoded = codec.encode(audData, fs, 0.02, dct2, 50)
a = current_milli_time()
print('Tempo de encode: ', a - b)

encoded.descartar(160)
encoded.saveToFile("./result/f0001038.desc160finais.16k.s50.dct2")

b = current_milli_time()
decoded = codec.decodeFromEncoded(encoded, dct2)
a = current_milli_time()
print('Tempo de decode: ', a - b)
wv.save_wave("./result/f0001038.16k-f1dct2.desc160finais.s50.wav", fs, decoded, 16)

# newEncoded = enc.WaveEncoded.loadFromFile("./result/f0001038.8k.dct2")

# newdecoded = codec.decodeFromEncoded(newEncoded, dct4)
# wv.save_wave("./result/f0001038.8k-f2dct2.desc80.s20.wav", fs, newdecoded, 16)
