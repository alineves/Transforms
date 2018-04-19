import dcts.wave as wv
import dwt.codec as codec
import dwt.encoded_sorted_energy as enc
import numpy as np
import time

codec.addAlg(dct1)
codec.addAlg(dct2)
codec.addAlg(dct3)
codec.addAlg(dct4)

def current_milli_time():
    return int(round(time.time() * 1000))

print('Tempo Encode,Tempo Decode')
for i in range(50):
    fs, audData = wv.open_wave("./waves/f0001038.16k.WAV")

    be = current_milli_time()
    encoded = codec.encode(audData, fs, 1, 'db10', 9, sobreposicao=0)
    ae = current_milli_time()

    encoded.setPorcentagemDescarte(0.85)

    bd = current_milli_time()
    rest = codec.decode(encoded)
    ad = current_milli_time()
    print(ae - be, ',', ad - bd)

