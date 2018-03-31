import dcts.wave as wv
import idwt.codec as codec
import idwt.encoded as enc
import numpy as np

fs, audData = wv.open_wave("./waves/m0003022.WAV")

encoded = codec.encode(audData, fs, 0.02, 'db1', 4)

encoded.saveToFile('./result/m0003022.dwt')

rest = codec.decode(encoded)
wv.save_wave("./result/m0003022.db1.1.wav", fs, rest, 16)

newEncoded = enc.WaveEncoded.fromFile('./result/m0003022.dwt')
rest = codec.decode(newEncoded)
wv.save_wave("./result/m0003022.db1.2.wav", fs, rest, 16)

print("AAA ", newEncoded)