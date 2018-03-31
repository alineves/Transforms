import dcts.wave as wv
import idwt.codec as codec
import idwt.encoded as enc
import numpy as np

fs, audData = wv.open_wave("./waves/m0003022.WAV")

encoded = codec.encode(audData, fs, 0.02, 'db1', 2)

encoded.saveToFile('./result/m0003022.dwt')

newEncoded = enc.WaveEncoded.fromFile('./result/m0003022.dwt')

# rest = pywt.waverec(coeffs, 'db1')

# wv.save_wave("./result/m0003022.db1.2.wav", fs, rest, 16)

print("AAA ", newEncoded)