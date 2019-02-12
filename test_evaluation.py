import dcts.wave as wv
import evaluation.evaluation as eval
import numpy as np

fsRef, ref = wv.open_wave("./waves/f0001038.16k.WAV")
fsTest, test = wv.open_wave("./result/f0001038.16k.q1s.db10.dec9.remove85percent.s0.wav")

srn_seg = eval.evaluate_snr_seg(ref, test, int(fsRef * 0.02), 0)

print(srn_seg)

snr_total = eval.evaluate_snr_total(ref, test)

print(snr_total)
