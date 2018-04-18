import dcts.wave as wv
import dwt.codec as codec
import dwt.encoded_sorted_energy as enc
import numpy as np
import time

def current_milli_time():
    return int(round(time.time() * 1000))

fs, audData = wv.open_wave("./waves/f0001038.16k.WAV")

b = current_milli_time()
encoded = codec.encode(audData, fs, 0.9, 'db10', 9, sobreposicao=50)
a = current_milli_time()
print('Tempo de encode: ', a - b)
print("quantidadeQuadros", encoded.quantidadeQuadros())
encoded.setPorcentagemDescarte(0.8)

b = current_milli_time()
rest = codec.decode(encoded)
a = current_milli_time()
print('Tempo de decode: ', a - b)

encoded.saveToFile('./result/f0001038.16k.dwt')

wv.save_wave("./result/f0001038.16k.f2.q900ms.db10.dec9.remove80percent.s50.wav", fs, rest, 16)

newEncoded = enc.WaveEncoded.fromFile('./result/m0003018.dwt')
# rest = codec.decode(newEncoded)
# wv.save_wave("./result/m0003022.db1.2.wav", fs, rest, 16)

print("AAA ", newEncoded)