import dcts.wave as wv
import dcts.codec as codec
import dcts.encoded_sorted_energy as enc
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
encoded = codec.encodeEnergy(audData, fs, 0.02, dct2, sobreposicao=20)
a = current_milli_time()
print('Tempo de encode: ', a - b)

encoded.setPorcentagemDescarte(0.85)

b = current_milli_time()
rest = codec.decodeEnergy(encoded)
a = current_milli_time()
print('Tempo de decode: ', a - b)

encoded.saveToFile("./result/f0001038.16k.sorted.dct2")

wv.save_wave("./result/f0001038.8k.db12.dec9.remove85percent.s0.wav", fs, rest, 16)

# b = current_milli_time()
# decoded = codec.decodeFromEncoded(encoded, dct4)
# a = current_milli_time()
# print('Tempo de decode: ', a - b)
# wv.save_wave("./result/f0001038.16k-f1dct4.desc160.s20.wav", fs, decoded, 16)

# newEncoded = enc.WaveEncoded.loadFromFile("./result/f0001038.16k.dct4")

# newdecoded = codec.decodeFromEncoded(newEncoded, dct4)
# wv.save_wave("./result/f0001038.16k-f2dct4.desc160.s20.wav", fs, newdecoded, 16)
