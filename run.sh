#!/bin/bash

IFS=","
while read -a line; do
    filename=${line[0]}
    fs=${line[1]}
    sobreposicao=${line[2]}
    descartes=${line[3]}
    files=$(stat --printf="%s" waves/$filename)

    python encode.py waves/$filename $descartes $sobreposicao result/$filename.sdct1
    nf=result/$filename.s$sobreposicao.$descartes.wav
    python decode.py result/$filename.sdct1 $fs $nf

    dcts=$(stat --printf="%s" result/$filename.sdct1)
    peaq=$(peaq waves/$filename $nf)
    odg=$(echo "$peaq" | grep Difference | sed "s/.*: //g")
    di=$(echo "$peaq" | grep Index | sed "s/.*: //g")
    calc=$(bc <<< "scale = 10; ($files -$dcts) / $files")
    echo "$filename,$fs,$files,$sobreposicao,$descartes,$dcts,$odg,$di,$calc"
done <  teste.csv