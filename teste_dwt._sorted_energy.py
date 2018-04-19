import dcts.wave as wv
import dwt.codec as codec
import dwt.encoded_sorted_energy as enc
import numpy as np
import time

def current_milli_time():
    return int(round(time.time() * 1000))

fs, audData = wv.open_wave("./waves/f0001038.16k.WAV")

b = current_milli_time()
encoded = codec.encode(audData, fs, 1, 'db10', 9, sobreposicao=0)
a = current_milli_time()
print('Tempo de encode: ', a - b)
print("quantidadeQuadros", encoded.quantidadeQuadros())
encoded.setPorcentagemDescarte(0.85)

b = current_milli_time()
rest = codec.decode(encoded)
a = current_milli_time()
print('Tempo de decode: ', a - b)

encoded.saveToFile('./result/f0001038.16k.q1s.db10.dec9.remove85percent.s0.dwt')

wv.save_wave("./result/f0001038.16k.q1s.db10.dec9.remove85percent.s0.wav", fs, rest, 16)

#newEncoded = enc.WaveEncoded.fromFile('./result/f0001038.16k..f2.q900ms.db10.dec9.remove85percent.s0.dwt')
# rest = codec.decode(newEncoded)
# wv.save_wave("./result/m0003022.db1.2.wav", fs, rest, 16)

#print("AAA ", newEncoded)