import dcts.wave as wv
import dcts.codec as codec
import dcts.encoded as enc
import numpy as np
import dcts.dct1 as dct1
import pywt

fs, audData = wv.open_wave("./waves/m0003022.WAV")

coeffs = pywt.wavedec(audData, 'db1', level=2)

rest = pywt.waverec(coeffs, 'db1')

wv.save_wave("./result/m0003022.db1.2.wav", fs, rest, 16)

print("AAA ", coeffs)