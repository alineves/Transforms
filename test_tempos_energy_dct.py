import dcts.wave as wv
import dcts.codec as codec
import dcts.encoded_sorted_energy as enc
import numpy as np
import dcts.dct1 as dct1
import dcts.dct2 as dct2
import dcts.dct3 as dct3
import dcts.dct4 as dct4
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
    encoded = codec.encodeEnergy(audData, fs, 0.02, dct2, sobreposicao=50)
    ae = current_milli_time()

    encoded.setPorcentagemDescarte(0.85)

    bd = current_milli_time()
    rest = codec.decodeEnergy(encoded)
    ad = current_milli_time()
    print(ae - be, ',', ad - bd)

